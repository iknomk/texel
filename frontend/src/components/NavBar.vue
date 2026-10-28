<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { getCurrentUser, isAuthenticated } from "../services/api";
const username = ref("");
async function loadUser() {
  if (!isAuthenticated()) { username.value = ""; return; }
  try { const user = await getCurrentUser(); username.value = user.username; }
  catch { username.value = ""; }
}
function openAuth(type) { window.dispatchEvent(new CustomEvent("texel:open-auth", { detail: type })); }
onMounted(() => { loadUser(); window.addEventListener("texel:auth-changed", loadUser); });
onBeforeUnmount(() => window.removeEventListener("texel:auth-changed", loadUser));
</script>
<template>
  <header class="site-header">
    <div class="header-inner">
      <router-link to="/" class="brand"><span class="brand-mark">t</span> texel<span class="brand-dot">.</span></router-link>
      <nav class="header-nav">
        <router-link to="/#how-it-works">Как это работает</router-link>
        <router-link to="/#possibilities">Возможности</router-link>
        <router-link to="/pricing" class="nav-pricing" active-class="nav-pricing-active">Тарифы</router-link>
        <template v-if="username">
          <router-link to="/profile" class="header-profile-link" :aria-label="`Личный кабинет: ${username}`" title="Личный кабинет">
            <span class="profile-user-icon" aria-hidden="true">✦</span>
          </router-link>
        </template>
        <template v-else>
          <button class="nav-login" @click="openAuth('login')">Войти</button>
          <button class="button button-primary header-cta" @click="openAuth('register')">Начать бесплатно <span class="button-icon">↗</span></button>
        </template>
      </nav>
    </div>
  </header>
</template>
