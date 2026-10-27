
<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { getCurrentUser, logout } from "../services/api";
import PhotoUploader from "../components/PhotoUploader.vue";
import ModelViewer from "../components/ModelViewer.vue";
import UiIcon from "../components/UiIcon.vue";

const router = useRouter();

const user = ref(null);
const error = ref("");
const loading = ref(true);

// Адрес текущей 3D-модели
const modelUrl = ref("/models/my-avatar.glb");
const hasGeneratedModel = computed(() => modelUrl.value && modelUrl.value !== "/models/my-avatar.glb");

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
  window.dispatchEvent(new Event("texel:auth-changed"));
  router.push("/");
}

onMounted(loadProfile);
</script>

<template>
  <main class="profile-plain">
    <header class="profile-topline">
      <div class="profile-welcome">
        <p class="eyebrow">ЛИЧНЫЙ КАБИНЕТ</p>
        <h1>Привет{{ user?.username ? `, ${user.username}` : "" }}<span class="brand-dot">.</span></h1>
        <p class="profile-intro">Создай свой цифровой образ — всё начинается с фотографии.</p>
      </div>

      <div class="profile-account">
        <p v-if="loading" class="profile-message">Загружаем профиль…</p>
        <p v-else-if="error" class="form-error">{{ error }}</p>
        <template v-else-if="user">
          <span class="profile-user-icon" aria-hidden="true">✦</span>
          <div class="profile-account-details">
            <strong>{{ user.username }}</strong>
            <span>{{ user.email }}</span>
          </div>
          <span class="profile-plan">Бесплатный тариф</span>
        </template>
        <button class="profile-logout" type="button" @click="handleLogout">Выйти <UiIcon name="arrow" /></button>
      </div>
    </header>

    <div class="profile-workspace">
      <div class="profile-source-column">
        <section class="profile-upload" aria-labelledby="profile-upload-title">
          <header class="profile-section-heading">
            <span class="profile-step" aria-hidden="true">01</span>
            <div>
              <h2 id="profile-upload-title">Загрузи фотографию</h2>
              <p>Одно фото — твой будущий 3D-аватар.</p>
            </div>
          </header>
          <PhotoUploader @model-ready="handleModelReady" />
        </section>

        <aside class="profile-photo-tips" aria-labelledby="profile-tips-title">
          <h3 id="profile-tips-title">Для лучшего результата</h3>
          <ul>
            <li><UiIcon name="sun" /><span>Хорошее освещение</span></li>
            <li><UiIcon name="person" /><span>Лицо и фигура видны в кадре</span></li>
            <li><UiIcon name="frame" /><span>Без лишних предметов на фоне</span></li>
          </ul>
        </aside>
      </div>

      <section id="avatar" class="profile-model-section" aria-labelledby="profile-model-title">
        <header class="profile-section-heading profile-result-heading">
          <span class="profile-step" aria-hidden="true">02</span>
          <div>
            <h2 id="profile-model-title">Твой 3D-аватар</h2>
            <p>Вращай модель мышью и рассмотри её со всех сторон.</p>
          </div>
          <span class="profile-model-status" :class="{ 'is-generated': hasGeneratedModel }">{{ hasGeneratedModel ? "Модель готова" : "Модель-пример" }}</span>
        </header>

        <ModelViewer :model-url="modelUrl" />
        <a
          :href="modelUrl === '/models/my-avatar.glb' ? modelUrl : `http://127.0.0.1:8000/api/models/download/${modelUrl.split('/').pop().split('?')[0]}`"
          :download="modelUrl.split('/').pop().split('?')[0]"
          class="download-model-button"
        >
          <UiIcon name="download" />
          Скачать модель (.glb)
        </a>
        <aside v-if="hasGeneratedModel" class="model-upgrade" aria-labelledby="model-upgrade-title">
          <div class="model-upgrade-icon"><UiIcon name="lock" /></div>
          <div class="model-upgrade-copy">
            <span class="model-upgrade-badge">ПО ПОДПИСКЕ</span>
            <h3 id="model-upgrade-title">Хочешь цветную версию?</h3>
            <p>Цветная модель с текстурой доступна по платной подписке.</p>
          </div>
          <router-link :to="{ path: '/pricing', query: { from: 'avatar' } }" class="button button-primary model-upgrade-link">Посмотреть тарифы <UiIcon name="arrow" /></router-link>
        </aside>
      </section>
    </div>

    <footer class="profile-footer">
      <router-link to="/" class="profile-footer-brand">texel<span class="brand-dot">.</span></router-link>
      <span>Твой цифровой образ начинается здесь.</span>
    </footer>
  </main>
</template>

<style scoped>
.profile-plain { max-width: 1380px; padding: 48px 36px 0; }
.profile-topline { align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 24px; margin-bottom: 38px; }
.profile-welcome { min-width: 0; }
.profile-topline .eyebrow { margin: 0 0 10px; }
.profile-topline h1 { font-size: clamp(32px, 3.5vw, 46px); line-height: 1.2; letter-spacing: -1.5px; overflow-wrap: anywhere; }
.profile-intro { margin: 12px 0 0; font-size: 12px; }
.profile-account { display: flex; align-items: center; flex-wrap: wrap; gap: 14px; min-width: 0; }
.profile-account .profile-user-icon { flex-shrink: 0; font-size: 16px; }
.profile-account-details { min-width: 0; max-width: 220px; }
.profile-account-details strong { display: block; font-size: 12px; overflow-wrap: anywhere; }
.profile-account-details > span { display: block; margin-top: 5px; color: #a99eab; font-size: 11px; overflow-wrap: anywhere; }
.profile-plan { padding: 7px 11px; border: 1px solid #3c303f; border-radius: 7px; color: #baadbe; font-size: 9px; white-space: nowrap; }
.profile-logout { display: inline-flex; align-items: center; gap: 7px; padding: 7px 0 7px 16px; border: 0; border-left: 1px solid #302731; background: transparent; color: #c4b7c9; font-size: 11px; white-space: nowrap; }
.profile-logout:hover { color: #ff77be; }
.profile-logout .ui-icon { width: 13px; height: 13px; }
.profile-message { margin: 0; }
.profile-workspace { display: grid; grid-template-columns: minmax(310px, .85fr) minmax(0, 1.45fr); align-items: start; gap: 28px; }
.profile-source-column { min-width: 0; }
.profile-upload { max-width: none; margin: 0; padding: 24px; background: #100d12; }
.profile-section-heading { display: flex; align-items: flex-start; gap: 13px; margin: 0 0 24px; }
.profile-step { display: grid; place-items: center; flex: 0 0 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #ff65b6, #e81784); color: #240a18; font-size: 12px; font-weight: 800; }
.profile-section-heading > div { flex: 1; min-width: 0; }
.profile-section-heading h2 { margin: 0; font-family: 'Manrope', sans-serif; font-size: 17px; font-weight: 800; line-height: 1.5; }
.profile-section-heading p { margin: 5px 0 0; color: #a99eab; font-size: 11px; line-height: 1.7; }
.profile-upload :deep(.photo-dropzone) { min-height: 255px; padding: 24px 16px; }
.profile-upload :deep(.dropzone-title) { font-size: 14px; }
.profile-upload :deep(.dropzone-description) { font-size: 11px; }
.profile-upload :deep(.dropzone-hint) { font-size: 9px; }
.profile-upload :deep(.success-box) { padding: 12px 14px; }
.profile-upload :deep(.success-box h3) { margin: 0; }
.profile-photo-tips { margin: 24px 8px 0; color: #b8adbe; }
.profile-photo-tips h3 { margin: 0 0 16px; font-size: 12px; font-weight: 700; }
.profile-photo-tips ul { display: grid; gap: 14px; margin: 0; padding: 0; list-style: none; }
.profile-photo-tips li { display: flex; align-items: center; gap: 13px; font-size: 11px; line-height: 1.7; }
.profile-photo-tips .ui-icon { width: 19px; height: 19px; color: #d4c7d8; }
.profile-model-section { min-width: 0; margin-top: 0; }
.profile-result-heading { display: grid; grid-template-columns: 32px minmax(0, 1fr) auto; align-items: start; margin: 0 0 20px; }
.profile-model-status { display: inline-flex; align-items: center; flex-shrink: 0; gap: 7px; margin-top: 8px; color: #a99eab; font-size: 10px; white-space: nowrap; }
.profile-model-status::before { content: ''; width: 7px; height: 7px; border-radius: 50%; background: #817684; }
.profile-model-status.is-generated { color: #c9e8d4; }
.profile-model-status.is-generated::before { background: #43c87e; }
.profile-model-section .model-upgrade { display: grid; grid-template-columns: 46px minmax(0, 1fr) auto; gap: 16px; padding: 20px; }
.profile-model-section .model-upgrade-link { width: auto; }
.profile-footer { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-top: 42px; padding: 22px 0; border-top: 1px solid #241c27; color: #817684; font-size: 9px; }
.profile-footer-brand { color: #f8f5f8; font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; letter-spacing: -.8px; }
@media (max-width: 1100px) {
  .profile-plain { padding: 40px 24px 0; }
  .profile-workspace { gap: 22px; }
  .profile-upload { padding: 20px; }
  .profile-model-section .model-upgrade { grid-template-columns: 46px minmax(0, 1fr); }
  .profile-model-section .model-upgrade-link { grid-column: 2; justify-self: start; }
  .profile-result-heading { grid-template-columns: 32px minmax(0, 1fr); }
  .profile-model-status { grid-column: 2; margin: -5px 0 0; }
}
@media (max-width: 900px) {
  .profile-plain { max-width: 780px; padding-top: 34px; }
  .profile-topline { flex-direction: column; align-items: flex-start; margin-bottom: 30px; }
  .profile-workspace { grid-template-columns: minmax(0, 1fr); gap: 32px; }
  .profile-photo-tips ul { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
  .profile-photo-tips li { align-items: flex-start; }
  .profile-result-heading { grid-template-columns: 32px minmax(0, 1fr) auto; }
  .profile-model-status { grid-column: auto; margin: 8px 0 0; }
  .profile-model-section .model-upgrade { grid-template-columns: 46px minmax(0, 1fr) auto; }
  .profile-model-section .model-upgrade-link { grid-column: auto; }
}
@media (max-width: 600px) {
  .profile-plain { padding: 30px 20px 0; }
  .profile-account { gap: 12px; width: 100%; }
  .profile-account-details { flex: 1; max-width: none; }
  .profile-plan { order: 1; margin-left: 54px; }
  .profile-logout { border-left: 0; padding-left: 0; }
  .profile-upload { padding: 20px 16px; }
  .profile-photo-tips ul { grid-template-columns: 1fr; gap: 10px; }
  .profile-section-heading h2 { font-size: 16px; }
  .profile-result-heading { grid-template-columns: 32px minmax(0, 1fr); }
  .profile-model-status { grid-column: 2; margin: -5px 0 0; }
  .profile-model-section .model-upgrade { grid-template-columns: 40px minmax(0, 1fr); padding: 18px; gap: 14px; }
  .profile-model-section .model-upgrade-icon { width: 40px; height: 40px; }
  .profile-model-section .model-upgrade-link { grid-column: 1 / -1; width: 100%; }
  .profile-footer { align-items: flex-start; }
  .profile-footer > span { max-width: 170px; text-align: right; line-height: 1.8; }
}
</style>
