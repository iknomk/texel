"""Validate photo uploads before allocating inference memory or GPU quota."""

from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError


MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
FORMATS_BY_EXTENSION = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
FORMATS_BY_MIME = {"image/jpeg": "JPEG", "image/jpg": "JPEG", "image/png": "PNG", "image/webp": "WEBP"}


def save_validated_photo(upload: UploadFile, destination: Path):
    extension_format = FORMATS_BY_EXTENSION.get(Path(upload.filename or "").suffix.lower())
    mime_format = FORMATS_BY_MIME.get((upload.content_type or "").lower())
    if not extension_format or mime_format != extension_format:
        raise HTTPException(400, "Выберите фотографию в формате JPG, PNG или WEBP.")
    try:
        size = 0
        with destination.open("wb") as target:
            while chunk := upload.file.read(64 * 1024):
                size += len(chunk)
                if size > MAX_FILE_BYTES:
                    raise HTTPException(413, "Фотография слишком большая. Максимальный размер — 10 МБ.")
                target.write(chunk)
        if not size:
            raise HTTPException(400, "Файл пустой. Выберите другую фотографию.")
        with Image.open(destination) as image:
            if image.format != extension_format:
                raise HTTPException(400, "Содержимое фотографии не соответствует расширению файла. Выберите исходный JPG, PNG или WEBP.")
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise HTTPException(413, "Разрешение фотографии слишком большое. Максимум — 20 мегапикселей, например 5000 × 4000 пикселей.")
            image.verify()
        # decode only after the pixel limit has been checked, to catch damaged
        # image data before the background-removal model is started.
        with Image.open(destination) as image:
            image.load()
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(400, "Не удалось прочитать фотографию. Файл повреждён или не является изображением.") from exc
    except Image.DecompressionBombError as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(413, "Разрешение фотографии слишком большое. Максимум — 20 мегапикселей.") from exc
    except Exception:
        destination.unlink(missing_ok=True)
        raise
