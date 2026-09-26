<script setup>

import {
    ref
} from "vue";

import {
    uploadPhoto
} from "../services/api";


const selectedFile = ref(null);

const loading = ref(false);

const error = ref("");

const result = ref(null);


// Пользователь выбрал файл
function handleFileSelect(event) {

    const file =
        event.target.files[0];

    if (!file) {
        return;
    }

    // Проверяем, что это изображение
    if (!file.type.startsWith("image/")) {

        error.value =
            "Можно загружать только изображения";

        selectedFile.value = null;

        return;

    }

    selectedFile.value = file;

    error.value = "";

    result.value = null;

}


// Отправляем файл на FastAPI
async function handleUpload() {

    if (!selectedFile.value) {

        error.value =
            "Сначала выберите фотографию";

        return;

    }


    loading.value = true;

    error.value = "";

    result.value = null;


    try {

        result.value =
            await uploadPhoto(
                selectedFile.value
            );

    } catch (err) {

        error.value =
            err.message;

    } finally {

        loading.value = false;

    }

}

</script>


<template>

    <div class="uploader">

        <div class="file-input">

            <input
                id="photo"
                type="file"
                accept="image/*"
                @change="handleFileSelect"
            />

            <label for="photo">
                Выбрать фотографию
            </label>

        </div>


        <div
            v-if="selectedFile"
            class="selected-file"
        >

            Выбран файл:

            <strong>
                {{ selectedFile.name }}
            </strong>

        </div>


        <button
            class="primary-button"
            @click="handleUpload"
            :disabled="
                !selectedFile || loading
            "
        >

            {{
                loading
                    ? "Загрузка..."
                    : "Загрузить фотографию"
            }}

        </button>


        <p
            v-if="error"
            class="error-message"
        >
            {{ error }}
        </p>


        <div
            v-if="result"
            class="success-box"
        >

            <h3>
                Фотография загружена
            </h3>

            <p>
                Имя файла:
            </p>

            <code>
                {{ result.filename }}
            </code>

            <p>
                Статус:
                {{ result.status }}
            </p>

        </div>

    </div>

</template>