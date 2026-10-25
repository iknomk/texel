<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import { getCurrentUser, logout, isAuthenticated } from "../services/api";
const router = useRouter();
const username = ref("");
async function loadUser() {
  if (!isAuthenticated()) { username.value = ""; return; }
  try { const user = await getCurrentUser(); username.value = user.username; }
  catch { username.value = ""; }
}
function openAuth(type) { window.dispatchEvent(new CustomEvent("texel:open-auth", { detail: type })); }
function handleLogout() { logout(); username.value = ""; router.push("/"); }
onMounted(() => { loadUser(); window.addEventListener("texel:auth-changed", loadUser); });
onBeforeUnmount(() => window.removeEventListener("texel:auth-changed", loadUser));
</script>
<template>
  <header class="site-header">
    <div class="header-inner">
      <router-link to="/" class="brand"><span class="brand-mark">t</span> texel<span class="brand-dot">.</span></router-link>
      <nav class="header-nav">
        <a href="#how-it-works">Как это работает</a>
        <a href="#possibilities">Возможности</a>
        <template v-if="username">
          <router-link to="/profile" class="nav-profile">{{ username }}</router-link>
          <button class="button button-outline header-cta" @click="handleLogout">Выйти</button>
        </template>
        <template v-else>
          <button class="nav-login" @click="openAuth('login')">Войти</button>
          <button class="button button-primary header-cta" @click="openAuth('register')">Начать бесплатно <span>↗</span></button>
        </template>
      </nav>
      <button class="mobile-cta" @click="username ? router.push('/profile') : openAuth('register')">{{ username ? "Профиль" : "Начать" }}</button>
    </div>
  </header>
</template>
