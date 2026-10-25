<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getCurrentUser, logout } from "../services/api";
import PhotoUploader from "../components/PhotoUploader.vue";

const router = useRouter();
const user = ref(null);
const error = ref("");
const loading = ref(true);

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
        @click="handleLogout"
      >
        Выйти из аккаунта ↗
      </button>
    </div>

    <p v-if="loading" class="profile-message">
      Загружаем профиль…
    </p>

    <p v-else-if="error" class="form-error">
      {{ error }}
    </p>

    <div v-else-if="user" class="profile-user">
      <span class="profile-user-icon">✦</span>
      <div>
        <strong>{{ user.username }}</strong>
        <span>{{ user.email }}</span>
      </div>
    </div>

    <section class="profile-upload">
      <h2>Загрузи фотографию</h2>
      <p>
        Выбери фото, с которого начнётся создание твоего 3D-аватара.
      </p>

      <PhotoUploader />
    </section>
  </main>
</template>