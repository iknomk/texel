# Texel — запуск локально

Нужны Python 3.10+ и Node.js 20+ (подойдут и более новые совместимые версии). Запускай backend и frontend в двух отдельных терминалах.

## 1. Backend

```bash
cd backend
python -m venv .venv
```

Активируй окружение:
- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Затем установи зависимости и запусти API:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Проверь в браузере: `http://127.0.0.1:8000/api/health` — ожидается `{"status":"ok"}`. Документация API: `http://127.0.0.1:8000/docs`.

## 2. Frontend

Во втором терминале, из корневой папки проекта:

```bash
cd frontend
npm ci
npm run dev
```

Открой адрес, который Vite напечатает в терминале (обычно `http://localhost:5173`).

## 3. Проверка сценария

1. Зарегистрируй пользователя.
2. Войди под созданной учётной записью.
3. Открой главную страницу и загрузи JPG или PNG.
4. Проверь, что ответ содержит `status: uploaded` и имя файла. Файл появится в `backend/uploads/`.

На этом этапе приложение только сохраняет фото — генерация 3D-модели ещё не подключена. Не используй эти настройки как production-конфигурацию: секрет JWT сейчас задан в коде и его нужно вынести в переменные окружения до публикации приложения.
