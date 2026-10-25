<script setup>
import { ref } from "vue";
import { uploadPhoto } from "../services/api";

const selectedFile = ref(null);
const loading = ref(false);
const error = ref("");
const result = ref(null);
const isDragging = ref(false);
const fileInput = ref(null);

function setFile(file) {
  if (!file) return;

  if (!file.type.startsWith("image/")) {
    error.value = "Можно загружать только изображения.";
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

  // Позволяет выбрать тот же файл повторно
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
  if (!selectedFile.value) {
    error.value = "Сначала выберите фотографию.";
    return;
  }

  loading.value = true;
  error.value = "";
  result.value = null;

  try {
    result.value = await uploadPhoto(selectedFile.value);
  } catch (err) {
    error.value = err.message || "Не удалось загрузить фотографию.";
  } finally {
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
      accept="image/*"
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
        class="file-picker-button"
        @click="fileInput?.click()"
      >
        Выбрать фотографию
      </button>

      <p class="dropzone-hint">
        Поддерживаются изображения JPG, PNG и WEBP
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
        @click="selectedFile = null; result = null; error = ''"
      >
        ×
      </button>
    </div>

    <button
      type="button"
      class="primary-button"
      @click="handleUpload"
      :disabled="!selectedFile || loading"
    >
      {{ loading ? "Загрузка..." : "Загрузить фотографию" }}
    </button>

    <p v-if="error" class="error-message">
      {{ error }}
    </p>

    <div v-if="result" class="success-box">
      <h3>Фотография загружена</h3>
      <p>Имя файла:</p>
      <code>{{ result.filename }}</code>
      <p>Статус: {{ result.status }}</p>
    </div>
  </div>
</template>