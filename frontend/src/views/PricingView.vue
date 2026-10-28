<script setup>
import { ref, computed, onBeforeUnmount } from "vue";
import { useRoute } from "vue-router";
import UiIcon from "../components/UiIcon.vue";

const route = useRoute();
const fromAvatar = computed(() => route.query.from === "avatar");
const plans = [
  { name: "Лайт", price: "299", description: "Для первых цветных аватаров", models: 5 },
  { name: "Плюс", price: "599", description: "Для новых образов и экспериментов", models: 20, popular: true },
  { name: "Про", price: "999", description: "Для тех, кто создаёт больше", models: 50 },
];
const paymentDialog = ref(null);
let previousOverflow = "";
let purchaseButton;
let isOpen = false;

function openPayment(event) {
  if (isOpen) return;
  purchaseButton = event.currentTarget;
  previousOverflow = document.body.style.overflow;
  document.body.style.overflow = "hidden";
  isOpen = true;
  paymentDialog.value.showModal();
}

function closePayment() {
  paymentDialog.value?.close();
}

function restorePage() {
  if (!isOpen) return;
  document.body.style.overflow = previousOverflow;
  isOpen = false;
  purchaseButton?.focus();
}

onBeforeUnmount(() => {
  closePayment();
  restorePage();
});
</script>

<template>
  <main class="pricing-page">
    <router-link v-if="!fromAvatar" to="/" class="pricing-home-link"><UiIcon name="arrow-left" />На главную</router-link>
    <div class="pricing-heading">
      <p class="eyebrow">БОЛЬШЕ ВОЗМОЖНОСТЕЙ</p>
      <h1>Добавь цвет своему образу<span class="brand-dot">.</span></h1>
      <p>Выбери подписку для создания цветных 3D-аватаров с текстурой.</p>
    </div>

    <section class="pricing-grid" aria-label="Тарифы подписки">
      <article v-for="plan in plans" :key="plan.name" class="pricing-card" :class="{ 'pricing-card-popular': plan.popular }">
        <span v-if="plan.popular" class="pricing-popular-label">ПОПУЛЯРНЫЙ</span>
        <h2>{{ plan.name }}</h2>
        <p class="pricing-price"><strong>{{ plan.price }} ₽</strong><span>/ месяц</span></p>
        <p class="pricing-description">{{ plan.description }}</p>
        <ul class="pricing-features">
          <li><UiIcon name="check" /><span>{{ plan.models }} цветных моделей в месяц</span></li>
          <li><UiIcon name="check" /><span>Простые цвета и текстура</span></li>
          <li><UiIcon name="check" /><span>Скачивание в GLB</span></li>
        </ul>
        <button type="button" class="button pricing-purchase" :class="plan.popular ? 'button-primary' : 'button-outline'" @click="openPayment">Купить {{ plan.name }}</button>
      </article>
    </section>

    <p class="pricing-free-note">Базовая модель без текстуры доступна бесплатно.</p>
    <router-link v-if="fromAvatar" to="/profile#avatar" class="pricing-back-link">← Вернуться к своему аватару</router-link>

    <dialog ref="paymentDialog" class="payment-dialog" aria-labelledby="payment-title" aria-describedby="payment-description" @click.self="closePayment" @close="restorePage">
      <section class="payment-panel" @click.stop>
        <button class="payment-close" type="button" aria-label="Закрыть" @click="closePayment"><UiIcon name="close" /></button>
        <div class="icon-tile payment-symbol"><UiIcon name="globe-lock" /></div>
        <h2 id="payment-title">Функция оплаты недоступна в вашей стране</h2>
        <p id="payment-description">Сейчас оформить подписку не получится. Ты можешь продолжить пользоваться бесплатной версией.</p>
        <button class="button button-primary payment-confirm" type="button" autofocus @click="closePayment">Понятно</button>
      </section>
    </dialog>
  </main>
</template>

<style scoped>
.pricing-page {
  position: relative;
  max-width: 1240px;
  min-height: calc(100vh - 82px);
  margin: 0 auto;
  padding: 76px 34px 64px;
}

.pricing-home-link {
  position: absolute;
  top: 22px;
  left: 34px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  color: #a99eab;
  font-size: 11px;
}

.pricing-home-link:hover {
  color: #ff77be;
}

.pricing-home-link .ui-icon {
  width: 17px;
  height: 17px;
}

.pricing-heading {
  text-align: center;
}

.pricing-heading .eyebrow {
  margin-bottom: 18px;
}

.pricing-heading h1 {
  margin: 0;
  font-family: 'Space Grotesk', 'Manrope', sans-serif;
  font-size: clamp(32px, 4vw, 48px);
  line-height: 1.15;
  letter-spacing: -1.8px;
}

.pricing-heading > p:last-child {
  margin: 18px auto 0;
  color: #a99eab;
  font-size: 14px;
  line-height: 1.8;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
  max-width: 1060px;
  margin: 58px auto 0;
}

.pricing-card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  padding: 30px 24px 24px;
  border: 1px solid #302731;
  border-radius: 12px;
  background: #100d12;
}

.pricing-card-popular {
  border-color: #ff2997;
  box-shadow: 0 0 0 1px rgba(255, 41, 151, .2), 0 12px 48px rgba(255, 41, 151, .05);
}

.pricing-popular-label {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 6px 16px;
  border-radius: 20px;
  background: #ff2997;
  color: #160810;
  font-size: 9px;
  font-weight: 800;
  letter-spacing: .5px;
  white-space: nowrap;
}

.pricing-card h2 {
  margin: 0 0 8px;
  font-size: 23px;
  font-weight: 800;
}

.pricing-price {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 9px;
  margin: 0;
}

.pricing-price strong {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.3;
  letter-spacing: -1px;
}

.pricing-price span {
  color: #b9aebc;
  font-size: 13px;
}

.pricing-description {
  min-height: 42px;
  margin: 12px 0 22px;
  color: #b9aebc;
  font-size: 12px;
  line-height: 1.7;
}

.pricing-features {
  display: grid;
  gap: 16px;
  margin: 0 0 32px;
  padding: 24px 0 0;
  border-top: 1px solid #302731;
  list-style: none;
}

.pricing-features li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 12px;
  line-height: 1.65;
  color: #e0d6e3;
}

.pricing-features .ui-icon {
  flex: 0 0 18px;
  color: #ff2997;
}

.pricing-purchase {
  width: 100%;
  min-height: 45px;
  margin-top: auto;
}

.pricing-purchase.button-outline {
  border-color: #b9adbe;
}

.pricing-purchase.button-outline:hover {
  background: #20151e;
  border-color: #ff65b6;
}

.pricing-free-note {
  margin: 28px 0 0;
  text-align: center;
  color: #a99eab;
  font-size: 12px;
  line-height: 1.8;
}

.pricing-back-link {
  display: block;
  width: fit-content;
  margin: 22px auto 0;
  color: #d9cadb;
  font-size: 12px;
}

.pricing-back-link:hover {
  color: #ff65b6;
}

.payment-dialog {
  width: min(440px, calc(100vw - 32px));
  max-height: calc(100dvh - 32px);
  padding: 0;
  border: 1px solid #6c294e;
  border-radius: 14px;
  background: #100d12;
  color: #f8f5f8;
  box-shadow: 0 25px 100px #000a;
}

.payment-dialog::backdrop {
  background: rgba(3, 2, 5, .78);
  backdrop-filter: blur(7px);
}

.payment-panel {
  position: relative;
  padding: 36px 32px 28px;
  text-align: center;
}

.payment-close {
  position: absolute;
  top: 12px;
  right: 12px;
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  padding: 6px;
  border: 0;
  border-radius: 6px;
  background: transparent;
  color: #a99eab;
}

.payment-close:hover {
  background: #251520;
  color: #fff;
}

.payment-symbol {
  width: 60px;
  height: 60px;
  margin: 0 auto 22px;
  border-radius: 14px;
}

.payment-symbol .ui-icon {
  width: 34px;
  height: 34px;
}

.payment-panel h2 {
  max-width: 330px;
  margin: 0 auto;
  font-size: 24px;
  line-height: 1.3;
  font-weight: 800;
  letter-spacing: -.5px;
}

.payment-panel p {
  margin: 18px 0 24px;
  font-size: 12px;
  line-height: 1.9;
  color: #b9adbe;
}

.payment-confirm {
  width: 100%;
  min-height: 44px;
}

@media (max-width: 900px) {
  .pricing-page {
    padding: 64px 24px 48px;
  }

  .pricing-home-link {
    left: 24px;
    top: 16px;
  }

  .pricing-grid {
    gap: 14px;
  }

  .pricing-card {
    padding: 28px 18px 20px;
  }
}

@media (max-width: 700px) {
  .pricing-page {
    padding: 48px 20px;
  }

  .pricing-home-link {
    left: 20px;
    top: 8px;
  }

  .pricing-heading h1 {
    letter-spacing: -1px;
  }

  .pricing-heading > p:last-child {
    max-width: 360px;
    font-size: 12px;
  }

  .pricing-grid {
    grid-template-columns: 1fr;
    max-width: 420px;
    gap: 28px;
    margin-top: 42px;
  }

  .pricing-card {
    padding: 28px 24px 24px;
  }

  .pricing-description {
    min-height: 0;
  }

  .pricing-free-note {
    max-width: 280px;
    margin-left: auto;
    margin-right: auto;
  }
}

@media (max-width: 380px) {
  .payment-panel {
    padding: 34px 22px 24px;
  }

  .payment-panel h2 {
    font-size: 21px;
  }
}
</style>
