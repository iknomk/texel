// адрес fastapi backend
const API_URL = "http://127.0.0.1:8000";


// регистрация

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


// вход

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

    // сохраняем jwt-токен
    localStorage.setItem(
        "token",
        data.access_token
    );

    return data;
}


// получение текущего пользователя

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


// загрузка фотографии

export async function uploadPhoto(file) {

    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("Необходимо войти в аккаунт");
    }

    // formdata нужен для отправки файла
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


// выход

export function logout() {

    // удаляем jwt
    localStorage.removeItem("token");
}


// проверка авторизации

export function isAuthenticated() {

    return Boolean(
        localStorage.getItem("token")
    );
}


// загрузка готовой 3d-модели (.glb) на сервер

export async function upload3DModel(file) {
    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("Сначала войдите в аккаунт");
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        `${API_URL}/api/models/result`,
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
        throw new Error(data.detail || "Ошибка загрузки модели");
    }

    return data;
}


// создание 3d-модели из фотографии
export async function generateModel(file) {
    const token = localStorage.getItem("token");

    if (!token) {
        throw new Error("Сначала войдите в аккаунт");
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
        `${API_URL}/api/models/generate`,
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
            data.detail || "Не удалось создать 3D-модель"
        );
    }

    // превращаем относительный путь backend в полный url
    return {
        ...data,
        url: `${API_URL}${data.url}`
    };
}