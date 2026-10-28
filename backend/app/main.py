from pathlib import Path
from uuid import uuid4
import shutil

import bcrypt

from .image_processing import prepare_foreground
from .generation_errors import describe_generation_error
from .image_validation import save_validated_photo

from fastapi.responses import FileResponse


from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import BaseModel, EmailStr

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from jose import jwt, JWTError

from fastapi.staticfiles import StaticFiles
from gradio_client import Client, handle_file


# настройки

app = FastAPI(
    title="3D Model Generator API",
    description="Backend для построения 3D-моделей по фотографиям",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# хранение сгенерированных моделей

MODELS_DIR = Path("generated_models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/generated_models",
    StaticFiles(directory=str(MODELS_DIR)),
    name="generated_models"
)

# база данных

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# пароли и jwt

SECRET_KEY = "my-secret-key-change-this"
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Создает bcrypt-хеш пароля.
    bcrypt поддерживает максимум 72 байта пароля.
    """

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise HTTPException(
            status_code=400,
            detail="Пароль не должен быть длиннее 72 байт"
        )

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed.decode("utf-8")


def verify_password(
    password: str,
    password_hash: str
) -> bool:

    password_bytes = password.encode("utf-8")
    hash_bytes = password_hash.encode("utf-8")

    try:
        return bcrypt.checkpw(
            password_bytes,
            hash_bytes
        )
    except ValueError:
        return False


def create_access_token(user_id: int) -> str:

    data = {
        "sub": str(user_id)
    }

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# схемы

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


# авторизация

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Недействительный токен"
            )

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Недействительный токен"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не найден"
        )

    return user


# регистрация

@app.post("/api/auth/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    # проверяем username

    existing_user = db.query(User).filter(
        User.username == data.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким username уже существует"
        )

    # проверяем email

    existing_email = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )

    # хешируем пароль

    password_hash = hash_password(data.password)

    # создаем пользователя

    user = User(
        username=data.username,
        email=data.email,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Регистрация успешна",
        "user_id": user.id,
        "username": user.username,
        "email": user.email
    }


# вход

@app.post(
    "/api/auth/login",
    response_model=LoginResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Неверный username или пароль"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Неверный username или пароль"
        )

    # создаем jwt

    token = create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# профиль текущего пользователя

@app.get("/api/auth/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }


# загрузка фотографии

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(
    exist_ok=True
)


@app.post("/api/models")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    # получаем расширение

    file_extension = Path(
        file.filename
    ).suffix.lower()

    # создаем уникальное имя

    new_filename = (
        f"{uuid4()}{file_extension}"
    )

    # полный путь

    file_path = UPLOAD_DIR / new_filename

    # сохраняем файл

    save_validated_photo(file, file_path)

    return {
        "filename": new_filename,
        "status": "uploaded"
    }


# проверка api

@app.get("/api/health")
def health_check():

    return {
        "status": "ok"
    }

# генерация 3d-модели из фото

def preprocess_image(source_path: Path) -> Path:
    """
    Удаляет фон, сохраняет естественные цвета и детали человека.
    Возвращает путь к PNG с прозрачным фоном для генерации 3D.
    """
    output_path = UPLOAD_DIR / f"{uuid4()}_processed.png"
    prepare_foreground(source_path, output_path)

    print(f"Подготовленное изображение сохранено: {output_path}")

    return output_path

@app.post("/api/models/generate")
def generate_3d_model(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    temp_path = None
    processed_path = None

    try:
        # временно сохраняем входное фото
        temp_path = UPLOAD_DIR / f"{uuid4()}_{Path(file.filename or 'photo.png').name}"

        save_validated_photo(file, temp_path)

        processed_path = preprocess_image(temp_path)

        # вызываем hunyuan3d на стороне hugging face
        client = Client(
            "tencent/Hunyuan3D-2",
            httpx_kwargs={
                "timeout": 600
            }
        )

        print("Доступные API Hunyuan3D:")
        print(client.view_api())


        job = client.submit(
            caption=None,
            image=handle_file(str(processed_path)),
            mv_image_front=None,
            mv_image_back=None,
            mv_image_left=None,
            mv_image_right=None,
            steps=30,
            guidance_scale=5,
            seed=1234,
            octree_resolution=256,
            check_box_rembg=True,
            num_chunks=8000,
            randomize_seed=True,
            api_name="/shape_generation"
        )

        print("Hunyuan3D: создаём модель...")
        result = job.result()
        print("HUNYUAN RESULT:", repr(result))


        # получаем путь к модели из ответа hunyuan3d
        if not result or not result[0]:
            raise RuntimeError("Генератор не вернул файл модели")

        mesh_result = result[0]

        if isinstance(mesh_result, dict):
            source_value = mesh_result.get("value")
        else:
            source_value = mesh_result

        if not source_value:
            raise RuntimeError(
                f"В ответе Hunyuan3D отсутствует путь к модели: {mesh_result!r}"
            )

        source_path = Path(str(source_value))

        if not source_path.is_file():
            raise RuntimeError(
                f"Файл модели не найден: {source_path}"
            )

        model_name = f"{uuid4()}.glb"
        destination = MODELS_DIR / model_name
        shutil.copy2(source_path, destination)

        print(f"Модель сохранена: {destination}")

        return {
            "status": "success",
            "filename": model_name,
            "url": f"/generated_models/{model_name}"
        }

    except HTTPException:
        raise
    except Exception as exc:
        import traceback

        traceback.print_exc()

        status_code, detail = describe_generation_error(exc)
        raise HTTPException(status_code=status_code, detail=detail) from exc

    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()


@app.get("/api/models/download/{filename}")
def download_model(filename: str):
    # не разрешаем передавать пути к чужим файлам
    safe_filename = Path(filename).name

    if safe_filename != filename or not safe_filename.endswith(".glb"):
        raise HTTPException(
            status_code=400,
            detail="Некорректное имя файла"
        )

    model_path = MODELS_DIR / safe_filename

    if not model_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Модель не найдена"
        )

    return FileResponse(
        path=model_path,
        media_type="model/gltf-binary",
        filename=safe_filename
    )
