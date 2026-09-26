<script setup>

import {
    ref,
    onMounted
} from "vue";

import {
    useRouter
} from "vue-router";

import {
    getCurrentUser,
    logout,
    isAuthenticated
} from "../services/api";


const router = useRouter();


// Текущий пользователь
const username = ref(null);


// Проверяем авторизацию
async function loadUser() {

    if (!isAuthenticated()) {
        return;
    }

    try {

        const user =
            await getCurrentUser();

        username.value =
            user.username;

    } catch {

        logout();

        username.value = null;

    }
}


// Выход из аккаунта
function handleLogout() {

    logout();

    username.value = null;

    router.push("/login");
}


onMounted(() => {

    loadUser();

});

</script>


<template>

    <header class="navbar">

        <div class="navbar-container">

            <!-- Название проекта -->
            <router-link
                to="/"
                class="logo"
            >
                Texel 3D
            </router-link>


            <nav class="nav-links">

                <router-link to="/">
                    Главная
                </router-link>


                <template v-if="username">

                    <router-link to="/profile">
                        Профиль
                    </router-link>

                    <span class="username">
                        {{ username }}
                    </span>

                    <button
                        class="nav-button"
                        @click="handleLogout"
                    >
                        Выйти
                    </button>

                </template>


                <template v-else>

                    <router-link to="/login">
                        Войти
                    </router-link>

                    <router-link
                        to="/register"
                        class="register-link"
                    >
                        Регистрация
                    </router-link>

                </template>

            </nav>

        </div>

    </header>

</template>