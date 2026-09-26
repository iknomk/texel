<script setup>

import {
    ref
} from "vue";

import {
    useRouter
} from "vue-router";

import {
    login
} from "../services/api";


const router = useRouter();


const username = ref("");
const password = ref("");

const error = ref("");
const loading = ref(false);


async function handleLogin() {

    error.value = "";

    loading.value = true;

    try {

        await login(
            username.value,
            password.value
        );

        // После успешного входа
        // открываем профиль
        router.push("/profile");

    } catch (err) {

        error.value =
            err.message;

    } finally {

        loading.value = false;

    }

}

</script>


<template>

    <div class="auth-page">

        <div class="auth-card">

            <h1>
                Вход
            </h1>

            <p class="auth-description">
                Войдите в свой аккаунт
            </p>


            <form
                @submit.prevent="handleLogin"
            >

                <label>
                    Имя пользователя
                </label>

                <input
                    v-model="username"
                    type="text"
                    placeholder="Введите username"
                    required
                />


                <label>
                    Пароль
                </label>

                <input
                    v-model="password"
                    type="password"
                    placeholder="Введите пароль"
                    required
                />


                <p
                    v-if="error"
                    class="error-message"
                >
                    {{ error }}
                </p>


                <button
                    class="primary-button full-width"
                    type="submit"
                    :disabled="loading"
                >

                    {{
                        loading
                            ? "Вход..."
                            : "Войти"
                    }}

                </button>

            </form>


            <p class="auth-footer">

                Нет аккаунта?

                <router-link to="/register">
                    Зарегистрироваться
                </router-link>

            </p>

        </div>

    </div>

</template>