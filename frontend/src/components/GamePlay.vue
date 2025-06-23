<template>
  <div class="flex justify-content-center align-items-center h-screen p-3">
    <Card class="shadow-5 border-round-lg w-full  p-3">
      <template #title>
        <div class="text-center text-3xl font-bold text-teal-500">
          Game Play
        </div>
      </template>

      <template #content>
         <div class="flex flex-row ">
          <div class="flex flex-col justify-center items-center p-4 border-r-2">
            <div class="col items-center" style="width:30%;">
              <h2 class="text-2xl font-semibold mt-2">Turn:</h2>
              <img :src="monsterImage" :alt="playerName" class="max-w-full h-auto rounded-lg shadow-lg" style="max-height: 300px;" />
              <h2 class="text-2xl font-semibold mt-2">{{ playerName }}</h2>
            </div>
          </div>
          <Divider layout="vertical" />
          <div class="flex justify-center items-center p-4" style="width:500px; height: 500px;">
            <div ref="gameCanvas" class="w-full h-full "></div>
          </div>

        </div>
      </template>
    </Card>
  </div>
</template>

<script>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

export default {
  name: 'GamePlay',
  props: {
    playerName: { type: String, default: 'Player 1' },
    monsterID: { type: Number, required: true }
  },
  computed: {
    monsterImage() {
      return `/src/assets/monsters/monster${this.monsterID}.png`;
    }
  },
  mounted() {
    this.initThree();
  },
  methods: {
    initThree() {
      const width = this.$refs.gameCanvas.clientWidth;
      const height = this.$refs.gameCanvas.clientHeight;

      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0xf5f5f5);

      const camera = new THREE.PerspectiveCamera(65, width / height, 0.1, 100);
      camera.position.set(20, 10, 15);

      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(width, height);
      this.$refs.gameCanvas.appendChild(renderer.domElement);

      const controls = new OrbitControls(camera, renderer.domElement);
      camera.position.set(0, 10, 15);
      controls.update();

      // Lighting
      const ambientLight = new THREE.AmbientLight(0xffffff, 1);
      scene.add(ambientLight);
      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(10, 10, 10);
      scene.add(directionalLight);

      // Table
      const tableGeometry = new THREE.BoxGeometry(10, 0.5, 20);
      const tableMaterial = new THREE.MeshPhongMaterial({ color: 0xf5f5f5 });
      const table = new THREE.Mesh(tableGeometry, tableMaterial);
      table.position.y = -0.25;
      scene.add(table);

      // Cups using LatheGeometry
      const points = [
        new THREE.Vector2(0.45, 0),
        new THREE.Vector2(0.6, 0),
        new THREE.Vector2(0.8, 1.7),
        new THREE.Vector2(0.6, 1.65),
        new THREE.Vector2(0.6, 0)
      ];

      const cupGeometry = new THREE.LatheGeometry(points, 64);
      const cupMaterial = new THREE.MeshPhongMaterial({ color: 0xff2c2c, side: THREE.DoubleSide });
      const cup2Material = new THREE.MeshPhongMaterial({ color: 0xfa8072, side: THREE.DoubleSide });

      // First set of cups
      const rows = 3;
      for (let row = 0; row < rows; row++) {
        const cupsInRow = rows - row;
        for (let i = 0; i < cupsInRow; i++) {
          const cup = new THREE.Mesh(cupGeometry, cupMaterial);
          cup.position.x = (i - (cupsInRow - 1) / 2) * 2;
          cup.position.y = 0.14;
          cup.position.z = -8 + row * 2;
          scene.add(cup);
        }
      }

      // Second set of cups
      for (let row = 0; row < rows; row++) {
        for (let i = 0; i <= row; i++) {
          const cup = new THREE.Mesh(cupGeometry, cup2Material);
          cup.position.x = (i - row / 2) * 2;
          cup.position.y = 0.14;
          cup.position.z = 5 + row * 2;
          scene.add(cup);
        }
      }

      // Ball
      const ballGeometry = new THREE.SphereGeometry(0.3, 32, 32);
      const ballMaterial = new THREE.MeshPhongMaterial({ color: 0xFAF9F6 });
      const ball = new THREE.Mesh(ballGeometry, ballMaterial);
      ball.position.set(0, 0.3, 0);
      scene.add(ball);

      window.addEventListener('resize', () => {
        camera.aspect = this.$refs.gameCanvas.clientWidth / this.$refs.gameCanvas.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(this.$refs.gameCanvas.clientWidth, this.$refs.gameCanvas.clientHeight);
      });

      function animate() {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
      }
      animate();
    }
  }
};
</script>
