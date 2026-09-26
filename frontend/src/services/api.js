// Адрес нашего FastAPI backend
const API_URL = "http://127.0.0.1:8000";


// =========================
// РЕГИСТРАЦИЯ
// =========================

export async function register(username, email, password) {
    const response = await fetch(
        `${API_URL}/api/auth/register`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                email,
                password
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Ошибка регистрации"
        );
    }

    return data;
}


// =========================
// ВХОД
// =========================

export async function login(username, password) {
    const response = await fetch(
        `${API_URL}/api/auth/login`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                password
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Ошибка входа"
        );
    }

    // Сохраняем JWT-токен
    localStorage.setItem(
        "token",
        data.access_token
    );

    return data;
}


// =========================
// ПОЛУЧЕНИЕ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ
// =========================

export async function getCurrentUser() {

    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("Пользователь не авторизован");
    }

    const response = await fetch(
        `${API_URL}/api/auth/me`,
        {
            method: "GET",

            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Ошибка получения профиля"
        );
    }

    return data;
}


// =========================
// ЗАГРУЗКА ФОТОГРАФИИ
// =========================

export async function uploadPhoto(file) {

    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("Необходимо войти в аккаунт");
    }

    // FormData нужен для отправки файла
    const formData = new FormData();

    formData.append(
        "file",
        file
    );

    const response = await fetch(
        `${API_URL}/api/models`,
        {
            method: "POST",

            headers: {
                Authorization: `Bearer ${token}`
            },

            body: formData
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Ошибка загрузки фотографии"
        );
    }

    return data;
}


// =========================
// ВЫХОД
// =========================

export function logout() {

    // Удаляем JWT
    localStorage.removeItem("token");
}


// =========================
// ПРОВЕРКА АВТОРИЗАЦИИ
// =========================

export function isAuthenticated() {

    return Boolean(
        localStorage.getItem("token")
    );
}