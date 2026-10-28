<script setup>
import { ref, onBeforeUnmount } from "vue";
import { generateModel } from "../services/api";

const emit = defineEmits(["model-ready"]);
const MAX_FILE_BYTES = 10 * 1024 * 1024;

const selectedFile = ref(null);
const loading = ref(false);
const progress = ref(0);
let progressTimer;

function stopProgress() {
  clearInterval(progressTimer);
  progressTimer = undefined;
}

function startProgress() {
  stopProgress();
  progress.value = 0;
  const startedAt = Date.now();
  // the api returns a final file, not inference steps. this is explicitly an
  // estimate: keep space for completion until the real request succeeds.
  progressTimer = setInterval(() => {
    const elapsed = Date.now() - startedAt;
    progress.value = Math.min(95, Math.round(95 * (1 - Math.exp(-elapsed / 45000))));
  }, 300);
}

onBeforeUnmount(stopProgress);
const error = ref("");
const result = ref(null);
const isDragging = ref(false);
const fileInput = ref(null);

function setFile(file) {
  if (!file || loading.value) return;

  let validationError = "";
  if (!/\.(jpe?g|png|webp)$/i.test(file.name) || !["image/jpeg", "image/jpg", "image/png", "image/webp"].includes(file.type)) {
    validationError = "Выберите фотографию в формате JPG, PNG или WEBP.";
  } else if (!file.size) {
    validationError = "Файл пустой. Выберите другую фотографию.";
  } else if (file.size > MAX_FILE_BYTES) {
    validationError = "Фотография слишком большая. Максимальный размер — 10 МБ.";
  }
  if (validationError) {
    error.value = validationError;
    selectedFile.value = null;
    result.value = null;
    return;
  }

  selectedFile.value = file;
  error.value = "";
  result.value = null;
}

function handleFileSelect(event) {
  setFile(event.target.files?.[0]);

  // позволяет выбрать тот же файл повторно
  event.target.value = "";
}

function handleDragOver() {
  isDragging.value = true;
}

function handleDragLeave(event) {
  if (!event.currentTarget.contains(event.relatedTarget)) {
    isDragging.value = false;
  }
}

function handleDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer?.files?.[0];
  setFile(file);
}

async function handleUpload() {
  if (loading.value) return;
  if (!selectedFile.value) {
    error.value = "Сначала выберите фотографию.";
    return;
  }

  loading.value = true;
  error.value = "";
  result.value = null;
  startProgress();

  try {
    result.value = await generateModel(selectedFile.value);
    stopProgress();
    progress.value = 100;
    emit("model-ready", result.value.url);
    // let the completed bar be visible before restoring the action button.
    await new Promise(resolve => setTimeout(resolve, 400));
  } catch (err) {
    error.value = err.message || "Не удалось создать 3D-модель.";
  } finally {
    stopProgress();
    loading.value = false;
  }
}
</script>

<template>
  <div class="uploader">
    <input
      ref="fileInput"
      class="photo-file-input"
      type="file"
      accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
      :disabled="loading"
      @change="handleFileSelect"
    />

    <div
      class="photo-dropzone"
      :class="{ 'photo-dropzone-active': isDragging }"
      @dragenter.prevent="handleDragOver"
      @dragover.prevent="handleDragOver"
      @dragleave.prevent="handleDragLeave"
      @drop.prevent="handleDrop"
    >
      <div class="dropzone-icon" aria-hidden="true">
        <svg
          viewBox="0 0 24 24"
          width="34"
          height="34"
          fill="none"
          stroke="currentColor"
          stroke-width="1.6"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M12 16V4" />
          <path d="m7 9 5-5 5 5" />
          <path d="M4 16v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3" />
        </svg>
      </div>

      <h3 class="dropzone-title">
        Перетащи фотографию сюда
      </h3>

      <p class="dropzone-description">
        или выбери файл на своём устройстве
      </p>

      <button
        type="button"
        class="button button-primary button-upload"
        :disabled="loading"
        @click="fileInput?.click()"
      >
        Выбрать фотографию
      </button>

      <p class="dropzone-hint">
        JPG, PNG и WEBP · до 10 МБ<br />Разрешение — до 20 мегапикселей
      </p>
    </div>

    <div v-if="selectedFile" class="selected-file">
      <span aria-hidden="true">✦</span>
      <div class="selected-file-info">
        <strong>{{ selectedFile.name }}</strong>
        <span>{{ (selectedFile.size / 1024 / 1024).toFixed(2) }} МБ</span>
      </div>
      <button
        type="button"
        class="remove-selected-file"
        aria-label="Убрать выбранную фотографию"
        :disabled="loading"
        @click="selectedFile = null; result = null; error = ''"
      >
        ×
      </button>
    </div>

    <button
      type="button"
      class="button button-primary generation-button"
      @click="handleUpload"
      :disabled="!selectedFile || loading"
      :aria-busy="loading"
    >
      <span v-if="loading" class="generation-button-progress" :style="{ width: `${progress}%` }" aria-hidden="true"></span>
      <span class="generation-button-label">
        {{ loading ? (progress === 100 ? "Модель готова · 100%" : `Создаём 3D-модель… ≈ ${progress}%`) : "Создать 3D-аватар" }}
      </span>
    </button>
    <p v-if="loading && progress < 100" class="generation-progress-note" role="status">Примерный прогресс. Время зависит от очереди генератора.</p>

    <p v-if="error" class="error-message">
      {{ error }}
    </p>

    <div v-if="result" class="success-box">
      <h3>3D-модель готова</h3>
    </div>
  </div>
</template>
