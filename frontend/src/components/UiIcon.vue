<script setup>
defineProps({ name: { type: String, required: true } });
</script>

<template>
  <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
    <template v-if="name === 'download'">
      <path d="M12 3v12m-5-5 5 5 5-5M4 16v4h16v-4" />
    </template>
    <template v-else-if="name === 'lock'">
      <rect x="5" y="10" width="14" height="11" rx="3" />
      <path d="M8 10V7a4 4 0 0 1 8 0v3m-4 5v2" />
    </template>
    <template v-else-if="name === 'arrow'">
      <path d="M6 18 18 6M6 6h12v12" />
    </template>
    <template v-else-if="name === 'arrow-left'">
      <path d="M19 12H5m7-7-7 7 7 7" />
    </template>
    <template v-else-if="name === 'check'">
      <path d="m5 12 4 4L19 6" />
    </template>
    <template v-else-if="name === 'sun'">
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5" />
    </template>
    <template v-else-if="name === 'person'">
      <circle cx="12" cy="7" r="4" />
      <path d="M4 22v-3a8 8 0 0 1 16 0v3" />
    </template>
    <template v-else-if="name === 'frame'">
      <path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5" />
    </template>
    <template v-else-if="name === 'globe-lock'">
      <path d="M12 21a9 9 0 1 1 9-10M3 12h13M5 6h14M5 18h6M12 3c-4 4-4 14 0 18m0-18c2 2 3 5 3 8" />
      <rect x="15" y="16" width="7" height="6" rx="1.5" />
      <path d="M17 16v-2a1.5 1.5 0 0 1 3 0v2" />
    </template>
    <path v-else-if="name === 'close'" d="m6 6 12 12M6 18 18 6" />
  </svg>
</template>
