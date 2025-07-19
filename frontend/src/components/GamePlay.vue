<template>
  <div class="gameplay-container">
    <Card class="gameplay-card" style="max-height: 86vh;">
      <template #title>
        <div class="gameplay-title">
          {{ winner ? 'WINNER' : 'GAME PLAY' }}
        </div>
      </template>

      <template #content>
        <div v-if="!winner" class="gameplay-content">
          <div class="player-info">
            <h2 class="turn-label">TURN:</h2>
            <div v-if="currentTurn==='player'" class="player-turn-container">
              <div class="avatar-wrapper">
                <img :src="monsterImage" loading="lazy" :alt="playerName + ' monster avatar'" class="monster-avatar" />
              <div v-if="timerActive" class="timer-overlay">
              <div class="timer-overlay-content">
                <i class="pi pi-clock" style="margin-right: 0.25rem;"></i>
                {{ timerValue }}s
              </div>
            </div>
            <h2 class="player-name">{{ playerName }}</h2>  
            <Button @click="shoot" class="p-button-secondary" style="margin-right:0.5em; margin-top:0.5em;">
              Shoot
            </Button>
            <Button icon="pi pi-clock" @click="timer" class="p-button-secondary"> </Button>
            </div>
          </div>

          <div v-if ="currentTurn==='robot'">
            <img src="/src/assets/monsters/robot.png" loading="lazy" alt="Robot monster avatar" class="monster-avatar" />
            <h2 class="player-name">Robot</h2>
            <div class="monster-btn-placeholder"></div>
          </div>
          </div>
          <Divider layout="vertical" />
          <div class="canvas-container">
            <div ref="gameCanvas" class="game-canvas"></div>
          </div>
        </div>
        <div v-else class="text-center">
          <div v-if="winner === 'player'">
            <img
              :src="monsterImage"
              loading="lazy"
              :alt="playerName + ' monster avatar'"
              class="monster-avatar winner-avatar"
            />
            <h3 class="winner-name">{{ playerName }}</h3>
            <p>Congratulations!</p>
          </div>

          <div v-else-if="winner === 'robot'">
            <img
              src="/src/assets/monsters/robot.png" 
              loading="lazy"
              alt="Robot avatar"
              class="monster-avatar"
            />
            <h3 class="winner-name">Robot</h3>
            <p>Ha ha you lost.</p>
          </div>
        </div>
        <div class="actions">
          <Button  icon="pi pi-refresh" @click="restartGame" class="p-button-secondary" ></Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script>
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import api from '../api';

export default {
  name: 'GamePlay',
  props: {
    playerName: { type: String, default: 'Player 1' },
    monsterID: { type: Number, required: true }
  },
  data() {
    return {
      cupState: [],
      cupMeshesPlayer: [],
      cupMeshesRobot: [],
      currentTurn: 'player',
      playerShots: 2,
      winner:null,
      timerActive: false,
      timerValue: 20,
      timerInterval: null,
    }
  },
  computed: {
    monsterImage() {
      return `/src/assets/monsters/monster${this.monsterID}.png`;
    }
  },
  mounted() {
    this.initThree();
    window.addEventListener('resize', this.handleResize);
    this.startGame();
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    if (this.renderer) {
      this.renderer.dispose();
    }
  },
  methods: {
    async startGame() {
      try {
        const response = await api.post('/start-game');
        console.log(response.data);
        this.cupState = response.data.state;
        this.updateCups();
      } catch (error) {
        console.error("Error starting game:", error);
      }
    },

    async shoot() {
      try {
        const response = await api.post('/shoot');
        console.log(response.data);
        this.cupState = response.data.state;

        if (response.data.hit !==null) {
          const targetCup = this.cupMeshesPlayer[response.data.hit];
          const targetX = targetCup.position.x;
          const targetZ = targetCup.position.z;
          this.animateShot(targetX, targetZ);


        setTimeout(() => {
          this.updateCups();
        }, 750);

        setTimeout(() => {
          this.playerShots -=1;
          if (this.playerShots >0){
          } else {
            this.currentTurn = 'robot';
            this.robotTurn();
          }
        }, 1700);

        } else{
          this.updateCups();
          setTimeout(() => {
            this.currentTurn = 'robot';
            this.robotTurn();
          }, 1000);
        }
      } catch (error) {
        console.error("Error shooting:", error);
      }
    },
    async timer() {
      if (this.timerActive) return;
      this.timerActive = true;
      this.timerValue = 20;
      this.timerInterval = setInterval(() => {
        if (this.timerValue > 0) {
          this.timerValue--;
        } else {
          this.timerActive = false;
          clearInterval(this.timerInterval);
        }
      }, 1000);
    },
    async robotTurn() {
      try {
        const response = await api.post('/robot-turn');
        console.log(response.data);
        const hits = response.data.hits;

        // Animate each robot shot sequentially
        for (let i = 0; i < hits.length; i++) {
          const hitIndex = hits[i];
          const targetCup = this.cupMeshesRobot[hitIndex];
          const targetX = targetCup.position.x;
          const targetZ = targetCup.position.z;

          await new Promise(resolve => setTimeout(resolve, 400));
          await this.animateRobotShot(targetX, targetZ);

          // Hide the cup immediately after the shot
          this.cupMeshesRobot[hitIndex].visible = false;
          // Optionally update cupState if needed
          // this.cupState[hitIndex + this.cupMeshesPlayer.length] = false;
        }

        // Update full state after robot finishes
        this.cupState = response.data.state;
        this.updateCups();

        setTimeout(() => {
          this.playerShots = 2;  // Reset player shots for next round
          this.currentTurn = 'player';
        }, 700);
      } catch (error) {
        console.error("Error in robot turn:", error);
      }
    },
    animateRobotShot(targetX, targetZ) {
      return new Promise((resolve) => {
        const startX = 0;
        const startY = 0.3;
        const startZ = -10;

        const endX = targetX;
        const endY = 0.14;
        const endZ = targetZ;

        const duration = 600; // ms
        const startTime = performance.now();

        const animateFrame = (now) => {
          const elapsed = now - startTime;
          const t = Math.min(elapsed / duration, 1);

          // Simple parabolic arc
          this.ball.position.x = startX + (endX - startX) * t;
          this.ball.position.z = startZ + (endZ - startZ) * t;
          this.ball.position.y = startY + 12 * t * (1 - t);

          if (t < 1) {
            requestAnimationFrame(animateFrame);
          } else {
            this.ball.position.set(endX, endY, endZ);
            setTimeout(() => {
              this.resetBall();
              resolve();  // Resolve after ball resets
            }, 400);
          }
        };

      requestAnimationFrame(animateFrame);
      });
    },

    initThree() {
      const width = this.$refs.gameCanvas.clientWidth;
      const height = this.$refs.gameCanvas.clientHeight;

      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0xf5f5f5);

      this.camera = new THREE.PerspectiveCamera(65, width / height, 0.1, 100);
      this.camera.position.set(0, 10, 15);

      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(width, height);
      this.$refs.gameCanvas.appendChild(this.renderer.domElement);

      this.controls = new OrbitControls(this.camera, this.renderer.domElement);
      this.controls.update();

      // Lighting
      const ambientLight = new THREE.AmbientLight(0xffffff, 1);
      this.scene.add(ambientLight);
      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(10, 10, 10);
      this.scene.add(directionalLight);

      // Table
      const tableGeometry = new THREE.BoxGeometry(10, 0.5, 20);
      const tableMaterial = new THREE.MeshPhongMaterial({ color: 0xf5f5f5 });
      const table = new THREE.Mesh(tableGeometry, tableMaterial);
      table.position.y = -0.25;
      this.scene.add(table);

      // Center line
      const lineMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const centerLine = new THREE.Mesh(
        new THREE.BoxGeometry(0.05, 0.01, 20),
        lineMaterial
      );
      centerLine.position.y = 0.135;
      centerLine.position.x = 0;
      centerLine.position.z = 0;
      this.scene.add(centerLine);

      // Side lines
      const sideLineLeft = new THREE.Mesh(
        new THREE.BoxGeometry(10, 0.01, 0.05),
        lineMaterial
      );
      sideLineLeft.position.y = 0.135;
      sideLineLeft.position.x = 0;
      sideLineLeft.position.z = -10;
      this.scene.add(sideLineLeft);

      const sideLineRight = sideLineLeft.clone();
      sideLineRight.position.z = 10;
      this.scene.add(sideLineRight);

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
          this.scene.add(cup);
          this.cupMeshesPlayer.push(cup);

          // Add bottom disk
          const bottomGeometry = new THREE.CircleGeometry(0.45, 32);
          const bottomMaterial = cupMaterial.clone();
          const bottom = new THREE.Mesh(bottomGeometry, bottomMaterial);
          bottom.rotation.x = -Math.PI / 2;
          bottom.position.set(cup.position.x, cup.position.y, cup.position.z);
          this.scene.add(bottom);
        }
      }

      // Second set of cups
      for (let row = 0; row < rows; row++) {
        for (let i = 0; i <= row; i++) {
          const cup = new THREE.Mesh(cupGeometry, cup2Material);
          cup.position.x = (i - row / 2) * 2;
          cup.position.y = 0.14;
          cup.position.z = 5 + row * 2;
          this.scene.add(cup);

          // Add bottom disk
          const bottomGeometry = new THREE.CircleGeometry(0.45, 32);
          const bottomMaterial = cup2Material.clone();
          const bottom = new THREE.Mesh(bottomGeometry, bottomMaterial);
          bottom.rotation.x = -Math.PI / 2;
          bottom.position.set(cup.position.x, cup.position.y, cup.position.z);
          this.scene.add(bottom);
          this.cupMeshesRobot.push(cup);
        }
      }

      // Ball
      const ballGeometry = new THREE.SphereGeometry(0.3, 32, 32);
      const ballMaterial = new THREE.MeshPhongMaterial({ color: 0xFAF9F6 });
      this.ball = new THREE.Mesh(ballGeometry, ballMaterial);
      this.ball.position.set(0, 0, 11);
      this.scene.add(this.ball);


      this.animate();
    },
    animate() {
      this.renderer.render(this.scene, this.camera);
      requestAnimationFrame(this.animate);
    },
    animateShot(targetX, targetZ) {
      const startX = 0;
      const startY = 0.3;
      const startZ = 0;

      const endX = targetX;
      const endY = 0.14; // Cup height
      const endZ = targetZ;

      const duration = 500; // ms
      const startTime = performance.now();

      const animateFrame = (now) => {
        const elapsed = now - startTime;
        const t = Math.min(elapsed / duration, 1); // Normalize 0 → 1

        // Simple parabolic arc (you can tweak this for realism)
        this.ball.position.x = startX + (endX - startX) * t;
        this.ball.position.z = startZ + (endZ - startZ) * t;
        this.ball.position.y = startY + 12 * t * (1 - t); // increased arc peak

        if (t < 1) {
          requestAnimationFrame(animateFrame);
        } else {
          this.ball.position.set(endX, endY, endZ);
          setTimeout(() => {
            this.resetBall();
          }, 100);
        }
      };

      requestAnimationFrame(animateFrame);
    },
    resetBall() {
      this.ball.position.set(0, 0, 11);
    },
    handleResize() {
      if (!this.$refs.gameCanvas) return;
      const width = this.$refs.gameCanvas.clientWidth;
      const height = this.$refs.gameCanvas.clientHeight;
      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(width, height);
    },
    updateCups() {
      for (let i = 0; i < this.cupMeshesPlayer.length; i++) {
        if (this.cupState[i] === false) {
          this.cupMeshesPlayer[i].visible = false;  
        } else {
          this.cupMeshesPlayer[i].visible = true;   
        }
      }

      for (let i = 0; i < this.cupMeshesRobot.length; i++) {
        if (this.cupState[i + this.cupMeshesPlayer.length] === false) {
          this.cupMeshesRobot[i].visible = false;
        } else {
          this.cupMeshesRobot[i].visible = true;
        }
      }

      this.gameOver();
    },
    restartGame() {
      window.location.reload();
      this.winner = null;
    },
    gameOver() {
      if (this.cupMeshesPlayer.every(cup => !cup.visible)) {
        this.winner = 'player';
      } else if (this.cupMeshesRobot.every(cup => !cup.visible)) {
        this.winner = 'robot';
      }
    }
  }
};
</script>

<style scoped>
.gameplay-container {
  min-height: 85vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f5;
  border-radius: 1rem;
}
.gameplay-card {
  width: 100%;
  max-width: 1100px;
  min-height: 600px;
  padding: 2rem;
  border-radius: 1rem;
  margin: 0;
  padding-top:0;
  padding-bottom:0;
}
.gameplay-title {
  text-align: center;
  font-family: 'Archivo Narrow', sans-serif;
  color: #20B2AA;
  font-size: clamp(1.5rem, 5vw, 4.5rem);
  margin:0;
  padding: 0;
}
.gameplay-content {
  display: flex;
  flex-direction: row;
  gap: 2rem;
  align-items: stretch;
  justify-content: center;
  flex-wrap: wrap;
}
.player-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 220px;
  max-width: 400px;
  min-height: 420px;
  flex: 1 1 220px;
  padding:0;
  margin:0;

}
.turn-label {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #0d9488;
}
.monster-avatar {
  width: 250px;
  height: 300px;
  object-fit: contain;
  display: block;
  /* max-width: 100%; */
  /* max-height: 300px; */
  border-radius: 1rem;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  margin: 1rem 0;
  padding: 1rem;
}
.player-name {
  font-size: 1.5rem;
  font-weight: 600;
  color: #334155;
  padding:0;
  margin:0;
}
.winner-name {
  font-size: 2rem;
  font-weight: 600;
  color: #24921f;
  padding:0;
  margin:0;
}
.canvas-container {
  flex: 2 1 400px;
  min-width: 320px;
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.game-canvas {
  width: 100%;
  height: 38vw;
  max-width: 500px;
  max-height: 450px;
  min-height: 320px;
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}
.monster-btn-placeholder {
  width: 120px;
  height: 25px;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.avatar-wrapper {
  position: relative;
  display: inline-block;
}

.timer-overlay {
  position: absolute;
  top: 1.5rem;
  right: 0.5rem;
  background: #ffffffdd;
  border-radius: 0.5rem;
  padding: 0.25rem 0.5rem;
}

.timer-overlay-content {
  font-size: 1.2rem;
  font-weight: 600;
  color: #fc1a1a;
  display: flex;
  align-items: center;
}

</style>
