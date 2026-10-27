
<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getCurrentUser, logout } from "../services/api";
import PhotoUploader from "../components/PhotoUploader.vue";
import ModelViewer from "../components/ModelViewer.vue";

const router = useRouter();

const user = ref(null);
const error = ref("");
const loading = ref(true);

// Адрес текущей 3D-модели
const modelUrl = ref("/models/my-avatar.glb");

function handleModelReady(url) {
  modelUrl.value = url;
}

async function loadProfile() {
  try {
    user.value = await getCurrentUser();
  } catch (err) {
    error.value = err.message || "Не удалось загрузить профиль";
  } finally {
    loading.value = false;
  }
}

function handleLogout() {
  logout();
  router.push("/");
}

onMounted(loadProfile);
</script>

<template>
  <main class="profile-plain">
    <!-- Заголовок профиля -->
    <div class="profile-topline">
      <div>
        <p class="eyebrow">ЛИЧНЫЙ КАБИНЕТ</p>
        <h1>Привет<span class="brand-dot">.</span></h1>
        <p class="profile-intro">
          Здесь начинается твой цифровой образ.
        </p>
      </div>

      <button
        class="button button-outline"
        type="button"
        @click="handleLogout"
      >
        Выйти из аккаунта ↗
      </button>
    </div>

    <!-- Состояние загрузки и ошибки профиля -->
    <p v-if="loading" class="profile-message">
      Загружаем профиль…
    </p>

    <p v-else-if="error" class="form-error">
      {{ error }}
    </p>

    <!-- Информация о пользователе -->
    <div v-else-if="user" class="profile-user">
      <span class="profile-user-icon">✦</span>

      <div>
        <strong>{{ user.username }}</strong>
        <span>{{ user.email }}</span>
      </div>
    </div>

    <!-- Загрузка фото и запуск генерации -->
    <section class="profile-upload">
      <h2>Создай свой 3D-аватар</h2>
      <p>
        Загрузи фотографию, чтобы создать трёхмерную модель.
      </p>

      <PhotoUploader @model-ready="handleModelReady" />
    </section>

    <!-- Единственный 3D-просмотрщик -->
    <section class="profile-model-section">
      <h2>Твой 3D-аватар</h2>
      <p class="profile-model-description">
        Здесь появится модель, созданная из твоей фотографии.
        Ты сможешь вращать её мышью и приближать колесом.
      </p>

      <ModelViewer :model-url="modelUrl" />
      <a
        v-if="modelUrl && modelUrl !== '/models/my-avatar.glb'"
        :href="`http://127.0.0.1:8000/api/models/download/${modelUrl.split('/').pop().split('?')[0]}`"
        class="download-model-button"
      >
        Скачать модель (.glb)
      </a>
    </section>
  </main>
</template>
