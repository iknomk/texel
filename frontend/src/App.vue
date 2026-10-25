<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import NavBar from "./components/NavBar.vue";
import { login, register, isAuthenticated } from "./services/api";

const router = useRouter();
const modal = ref("");
const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

function openAuth(type) {
  modal.value = type;
  username.value = "";
  email.value = "";
  password.value = "";
  error.value = "";
}
function closeAuth() { modal.value = ""; error.value = ""; }
function handleOpenEvent(event) { openAuth(event.detail || "login"); }
function handleKey(event) { if (event.key === "Escape") closeAuth(); }
onMounted(() => {
  window.addEventListener("texel:open-auth", handleOpenEvent);
  window.addEventListener("keydown", handleKey);
  if (["/login", "/register"].includes(router.currentRoute.value.path)) {
    openAuth(router.currentRoute.value.path === "/register" ? "register" : "login");
    router.replace("/");
  }
});
onBeforeUnmount(() => {
  window.removeEventListener("texel:open-auth", handleOpenEvent);
  window.removeEventListener("keydown", handleKey);
});
async function submitAuth() {
  error.value = "";
  loading.value = true;
  try {
    if (modal.value === "register") {
      await register(username.value.trim(), email.value.trim(), password.value);
      // Автоматически не авторизуем: пользователь входит обычным способом.
      modal.value = "login";
      password.value = "";
      error.value = "";
      alert("Аккаунт создан. Теперь войдите в него.");
    } else {
      await login(username.value.trim(), password.value);
      closeAuth();
      await router.push("/profile");
      window.dispatchEvent(new Event("texel:auth-changed"));
    }
  } catch (err) {
    error.value = err.message || "Не удалось выполнить запрос";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="app-shell">
    <NavBar />
    <router-view />
    <Transition name="modal">
      <div v-if="modal" class="modal-backdrop" @click.self="closeAuth">
        <section class="auth-modal" role="dialog" aria-modal="true" :aria-label="modal === 'login' ? 'Вход' : 'Регистрация'">
          <button class="modal-close" aria-label="Закрыть" @click="closeAuth">×</button>
          <a class="brand modal-brand" href="/" @click.prevent="closeAuth"><span class="brand-mark">t</span> texel<span class="brand-dot">.</span></a>
          <p class="eyebrow">ТВОЯ ЦИФРОВАЯ ВЕРСИЯ</p>
          <h2>{{ modal === "login" ? "С возвращением" : "Создай аккаунт" }}</h2>
          <p class="modal-subtitle">{{ modal === "login" ? "Войди, чтобы продолжить создание аватара." : "Зарегистрируйся и создай своего 3D-аватара." }}</p>
          <form class="auth-form" @submit.prevent="submitAuth">
            <label>Имя пользователя
              <input v-model="username" autocomplete="username" placeholder="Например, alex" minlength="3" required />
            </label>
            <label v-if="modal === 'register'">Электронная почта
              <input v-model="email" type="email" autocomplete="email" placeholder="you@example.com" required />
            </label>
            <label>Пароль
              <input v-model="password" type="password" :autocomplete="modal === 'login' ? 'current-password' : 'new-password'" placeholder="Не менее 8 символов" :minlength="modal === 'register' ? 8 : 1" required />
            </label>
            <p v-if="error" class="form-error">{{ error }}</p>
            <button class="button button-primary button-wide" type="submit" :disabled="loading">{{ loading ? "Подождите…" : modal === "login" ? "Войти в аккаунт" : "Создать аккаунт" }}</button>
          </form>
          <p class="auth-switch">{{ modal === "login" ? "Ещё нет аккаунта?" : "Уже зарегистрирован?" }}
            <button @click="openAuth(modal === 'login' ? 'register' : 'login')">{{ modal === "login" ? "Регистрация" : "Войти" }}</button>
          </p>
        </section>
      </div>
    </Transition>
  </div>
</template>
