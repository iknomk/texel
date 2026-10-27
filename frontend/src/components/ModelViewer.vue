<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

const props = defineProps({
  modelUrl: {
    type: String,
    default:
      "/models/my-avatar.glb"
    }
});

const host = ref(null);
const loading = ref(true);
const error = ref("");

let scene;
let camera;
let renderer;
let controls;
let currentModel;
let resizeObserver;
let animationId;
let disposed = false;

function resize() {
  if (!host.value || !renderer || !camera) return;

  const width = host.value.clientWidth;
  const height = host.value.clientHeight;

  if (!width || !height) return;

  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function fitModel(model) {
  const bounds = new THREE.Box3().setFromObject(model);
  const size = bounds.getSize(new THREE.Vector3());
  const center = bounds.getCenter(new THREE.Vector3());

  model.position.sub(center);

  const maxSize = Math.max(size.x, size.y, size.z, 1);
  const distance = maxSize * 2.2;

  camera.position.set(distance * 0.25, distance * 0.15, distance);
  camera.near = 0.01;
  camera.far = maxSize * 100;
  camera.updateProjectionMatrix();

  controls.target.set(0, 0, 0);
  controls.minDistance = maxSize * 0.6;
  controls.maxDistance = maxSize * 8;
  controls.update();
}

function loadModel(url) {
  if (!scene || !url) return;

  loading.value = true;
  error.value = "";

  if (currentModel) {
    scene.remove(currentModel);
    currentModel = null;
  }

  new GLTFLoader().load(
    url,
    (gltf) => {
      if (disposed) return;

      currentModel = gltf.scene;
      scene.add(currentModel);
      fitModel(currentModel);
      loading.value = false;
    },
    undefined,
    (err) => {
      console.error("Ошибка загрузки 3D-модели:", err);
      loading.value = false;
      error.value =
        "Не удалось загрузить модель. Проверь интернет или путь к файлу.";
    }
  );
}

function animate() {
  if (disposed) return;

  animationId = requestAnimationFrame(animate);
  controls?.update();
  renderer?.render(scene, camera);
}

function toggleFullscreen() {
  if (!host.value) return;

  if (!document.fullscreenElement) {
    host.value.requestFullscreen?.().catch(() => {});
  } else {
    document.exitFullscreen?.();
  }
}

onMounted(() => {
  if (!host.value) return;

  scene = new THREE.Scene();
  scene.background = new THREE.Color("#100b12");

  camera = new THREE.PerspectiveCamera(38, 1, 0.01, 1000);
  camera.position.set(0, 1, 4);

  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  host.value.prepend(renderer.domElement);

  scene.add(new THREE.HemisphereLight(0xffffff, 0x372238, 2));

  const mainLight = new THREE.DirectionalLight(0xffffff, 3);
  mainLight.position.set(4, 6, 5);
  scene.add(mainLight);

  const pinkLight = new THREE.PointLight(0xff2c9c, 22, 20);
  pinkLight.position.set(-3, 2, 2);
  scene.add(pinkLight);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.07;
  controls.enablePan = true;

  resizeObserver = new ResizeObserver(resize);
  resizeObserver.observe(host.value);

  resize();
  animate();
  loadModel(props.modelUrl);
});

watch(
  () => props.modelUrl,
  (url) => loadModel(url)
);

onBeforeUnmount(() => {
  disposed = true;
  cancelAnimationFrame(animationId);
  resizeObserver?.disconnect();
  controls?.dispose();

  renderer?.dispose();
  renderer?.domElement?.remove();
});
</script>

<template>
  <section class="model-viewer">
    <div class="model-viewer-toolbar">
      <div>
        <p class="eyebrow">3D WORKSPACE</p>
        <h3>Просмотр модели</h3>
      </div>

      <button
        class="viewer-tool-button"
        type="button"
        @click="toggleFullscreen"
      >
        На весь экран ⛶
      </button>
    </div>

    <div ref="host" class="model-viewer-canvas">
      <div v-if="loading" class="viewer-overlay">
        <span class="viewer-spinner"></span>
        <p>Загружаем 3D-модель…</p>
      </div>

      <div v-else-if="error" class="viewer-overlay viewer-error">
        <p>{{ error }}</p>
        <small>Поддерживаются файлы GLB и glTF.</small>
      </div>
    </div>

    <p class="viewer-hint">
      Перетаскивай мышью, чтобы вращать модель.
      Колесо мыши — приблизить или отдалить.
    </p>
  </section>
</template>