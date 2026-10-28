<script setup>
const openAuth = (type = "register") => window.dispatchEvent(new CustomEvent("texel:open-auth", { detail: type }));
</script>

<template>
  <div class="landing-page">
    <section class="hero-section">
      <div class="hero-glow"></div>
      <div class="hero-copy">
        <div class="eyebrow"><span class="live-dot"></span> ТВОЯ ЛИЧНОСТЬ. НОВОЕ ИЗМЕРЕНИЕ.</div>
        <h1>Загрузи фото.<br />Получи <span>свою 3D-версию.</span></h1>
        <p class="hero-description">Преврати себя в уникального цифрового персонажа. Твой стиль, твоя энергия — в объёмном формате.</p>
        <div class="hero-actions">
          <button class="button button-primary hero-button" @click="openAuth('register')">Создать свой аватар <span class="button-icon">↗</span></button>
          <a class="text-link" href="#how-it-works"><span class="play-icon">▶</span> Как это работает</a>
        </div>
        <div class="hero-proof"><div class="proof-avatars"><span>✦</span><span>◉</span><span>✧</span></div><p><strong>Твоя цифровая история</strong><br /><span>начинается здесь</span></p></div>
      </div>
      <div class="hero-art">
        <div class="art-orbit orbit-one"></div><div class="art-orbit orbit-two"></div>
        <div class="art-label label-top"><span class="label-dot"></span> YOUR DIGITAL SELF</div>
        <img src="/assets/avatar-hero.png" alt="Мультяшный 3D-аватар в розовых наушниках" class="hero-avatar" />
        <div class="floating-chip chip-top"><span>✦</span> 3D CHARACTER</div>
        <div class="floating-chip chip-bottom"><span class="pink-dot"></span> MADE TO BE YOU</div>
        <div class="art-spark spark-one">✳</div><div class="art-spark spark-two">✦</div>
      </div>
      <div class="hero-bottom-note"><span>01 / 03</span><span class="note-line"></span><span>ЛИСТАЙ, ЧТОБЫ УЗНАТЬ БОЛЬШЕ</span></div>
    </section>

    <section id="how-it-works" class="steps-section content-section">
      <div class="section-heading">
        <p class="eyebrow">ПРОСТО. БЫСТРО. ПО-ТВОЕМУ.</p>
        <h2>Три шага до <span>нового себя</span></h2>
        <p>Никаких сложных настроек. Только ты и немного цифровой магии.</p>
      </div>
      <div class="steps-grid">
        <article class="step-card"><div class="step-top"><span class="step-number">01</span><span class="step-icon">↥</span></div><h3>Загрузи фото</h3><p>Выбери фотографию, на которой хорошо видно твоё лицо. Это отправная точка твоего аватара.</p><div class="step-decoration deco-upload">▧</div></article>
        <article class="step-card featured-step"><div class="step-top"><span class="step-number">02</span><span class="step-icon">✧</span></div><h3>Создай персонажа</h3><p>Мы готовим основу твоего цифрового образа — объёмного, выразительного и неповторимого.</p><div class="step-decoration deco-star">✳</div></article>
        <article class="step-card"><div class="step-top"><span class="step-number">03</span><span class="step-icon">◈</span></div><h3>Забери свой 3D</h3><p>Рассматривай результат со всех сторон и используй свою модель в цифровом мире.</p><div class="step-decoration deco-cube">◇</div></article>
      </div>
    </section>

    <section id="possibilities" class="feature-section content-section">
      <div class="feature-visual"><img src="/assets/avatar-vr.png" alt="3D-аватар в виртуальной реальности" /><div class="visual-glow"></div><span class="visual-tag">IMAGINE IT. BECOME IT.</span></div>
      <div class="feature-copy"><p class="eyebrow">БОЛЬШЕ, ЧЕМ ФОТО</p><h2>Твой образ.<br /><span>Твоё измерение.</span></h2><p>Texel — пространство, где привычный снимок становится началом цифрового персонажа. Создай образ, который отражает именно тебя.</p><ul class="feature-list"><li><span>✓</span><div><strong>Твой уникальный стиль</strong><small>Персонаж, вдохновлённый твоим образом.</small></div></li><li><span>✓</span><div><strong>Объём со всех сторон</strong><small>3D-модель, которую можно рассматривать и вращать.</small></div></li><li><span>✓</span><div><strong>Всё начинается с одного фото</strong><small>Простой путь от изображения к цифровому миру.</small></div></li></ul><button class="button button-primary" @click="openAuth('register')">Попробовать Texel <span class="button-icon">↗</span></button></div>
    </section>

    <section class="closing-section"><div class="closing-decoration">✳</div><p class="eyebrow">ТВОЙ ЦИФРОВОЙ АВАТАР ЖДЁТ</p><h2>Готов увидеть себя<br /><span>по-новому?</span></h2><button class="button button-primary hero-button" @click="openAuth('register')">Начать бесплатно <span class="button-icon">↗</span></button><p class="closing-caption">Твоя следующая версия начинается с тебя.</p></section>
    <footer class="site-footer"><router-link to="/" class="brand"><span class="brand-mark">t</span> texel<span class="brand-dot">.</span></router-link><span>ТВОЙ ОБРАЗ В НОВОМ ИЗМЕРЕНИИ</span><span>© 2026 TEXEL</span></footer>
  </div>
</template>
