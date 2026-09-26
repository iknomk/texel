<script setup>

import {
    ref,
    onMounted
} from "vue";

import {
    useRouter
} from "vue-router";

import PhotoUploader
    from "../components/PhotoUploader.vue";

import {
    isAuthenticated,
    getCurrentUser
} from "../services/api";


const router = useRouter();

const username = ref(null);


onMounted(async () => {

    if (!isAuthenticated()) {
        return;
    }

    try {

        const user =
            await getCurrentUser();

        username.value =
            user.username;

    } catch {

        username.value = null;

    }

});


// Переход к авторизации
function goToLogin() {

    router.push("/login");

}

</script>


<template>

    <div class="home">

        <section class="hero">

            <h1>
                Построение 3D-моделей
                по фотографиям
            </h1>

            <p>
                Загружайте фотографии объекта
                и подготавливайте их для
                последующего построения
                3D-модели.
            </p>


            <div v-if="!username">

                <button
                    class="primary-button"
                    @click="goToLogin"
                >
                    Начать работу
                </button>

            </div>


            <div v-else>

                <p class="welcome">
                    Добро пожаловать,
                    <strong>{{ username }}</strong>!
                </p>

            </div>

        </section>


        <!-- Загрузка фотографий -->

        <section
            v-if="username"
            class="upload-section"
        >

            <h2>
                Загрузка фотографии
            </h2>

            <PhotoUploader />

        </section>


        <section
            v-else
            class="info-section"
        >

            <h2>
                Как это работает?
            </h2>

            <div class="steps">

                <div class="step">

                    <span>1</span>

                    <h3>
                        Регистрация
                    </h3>

                    <p>
                        Создайте аккаунт
                        в системе.
                    </p>

                </div>


                <div class="step">

                    <span>2</span>

                    <h3>
                        Загрузка
                    </h3>

                    <p>
                        Загрузите фотографии
                        объекта.
                    </p>

                </div>


                <div class="step">

                    <span>3</span>

                    <h3>
                        3D-модель
                    </h3>

                    <p>
                        Фотографии будут
                        использоваться для
                        построения 3D-модели.
                    </p>

                </div>

            </div>

        </section>

    </div>

</template>