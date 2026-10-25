<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "../services/api";

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function handleRegister() {
  error.value = "";
  loading.value = true;
  try {
    await register(username.value.trim(), email.value.trim(), password.value);
    router.push("/login");
  } catch (err) {
    error.value = err.message || "Не удалось зарегистрироваться";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>Регистрация</h1>
      <p class="auth-description">Создайте аккаунт Texel</p>
      <form @submit.prevent="handleRegister">
        <label for="username">Имя пользователя</label>
        <input id="username" v-model="username" type="text" autocomplete="username" minlength="3" maxlength="50" required />

        <label for="email">Электронная почта</label>
        <input id="email" v-model="email" type="email" autocomplete="email" required />

        <label for="password">Пароль</label>
        <input id="password" v-model="password" type="password" autocomplete="new-password" minlength="8" required />

        <p v-if="error" class="error-message">{{ error }}</p>
        <button class="primary-button full-width" type="submit" :disabled="loading">
          {{ loading ? "Создание аккаунта..." : "Зарегистрироваться" }}
        </button>
      </form>
      <p class="auth-footer">Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
    </div>
  </div>
</template>
