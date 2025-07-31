<template>
  <div class="gameplay-container">
    <Card class="gameplay-card" style="max-height: 85.8vh; width: 88vw;">
      <template #title>
        <div class="gameplay-title">
          {{ winner ? 'WINNER' : 'GAME PLAY' }}
        </div>
      </template>

      <template v-slot:content>
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
            <Button icon="pi pi-caret-right" @click="timer" style="margin-top:1em; background-color:green;"></Button>
            </div>
          </div>

          <div v-if ="currentTurn==='robot'">
            <img src="/src/assets/monsters/robot.png" loading="lazy" alt="Robot monster avatar" class="monster-avatar" />
            <h2 class="player-name">Robot</h2>
            <div class="monster-btn-placeholder"></div>
          </div>
          </div>
          

            <div >
              
              <div class="cups-grid">
                <p style="font-size: 2.5rem; padding:0rem; margin:0">&#x1F916;</p>
                <div class="cup-row" v-for="(row, rowIndex) in 3" :key="'robot-row-' + rowIndex">
                  <Cup
                    v-for="i in 3 - rowIndex"
                    :key="'robot-' + (robotCupStart + robotIndex(rowIndex, i))"
                    :cupId="robotCupStart + robotIndex(rowIndex, i)"
                    :visible="cupVisibility[robotCupStart + robotIndex(rowIndex, i)]"
                    @cup-clicked="handleCupClick"
                  />
                </div>
              </div>
              <br/>
              <br/>
              <div class="cups-grid">
                <div class="cup-row" v-for="(row, rowIndex) in 3" :key="'player-row-' + rowIndex">
                  <Cup
                    v-for="i in rowIndex + 1"
                    :key="'player-' + (playerCupStart + playerIndex(rowIndex, i))"
                    :cupId="playerCupStart + playerIndex(rowIndex, i)"
                    :visible="cupVisibility[playerCupStart + playerIndex(rowIndex, i)]"
                    @cup-clicked="handleCupClick"
                  />
                </div>
                <p style="font-size: 2.5rem; padding:0rem; margin:0">&#x1F47E;</p>
              </div>
            </div>

            
        </div>

        <div v-else class="text-center">
          <div v-if="winner === 'player'">
            <img
              :src="monsterImage"
              loading="lazy"
              :alt="playerName + ' monster avatar'"
              class="monster-avatar winner-avatar"
              style="justify-self:center !important;"
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
              style="justify-self:center !important;"
            />
            <h3 class="winner-name">Robot</h3>
            <p>Ha ha you lost.</p>
          </div>
        </div>
        <div class="actions gap-2"  style="margin: 0.3em; padding: 1em !important; position:relative; top: -2rem; left: 1rem;">
          <Button icon="pi pi-refresh" @click="restartGame" class="p-button-secondary" ></Button>
        </div>
      </template>
    </Card>
  </div>
</template>

<script>
import api from '../api';
import Cup from './Cup.vue'; 
import axios from 'axios';


export default {
  name: 'GamePlay',
  components:{
    Cup
  },
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
      timerValue: 10,
      timerInterval: null,
      cupVisibility: Array(12).fill(true),
      robotCupStart:0,
      playerCupStart:6,
    }
  },
  computed: {
    monsterImage() {
      return `/src/assets/monsters/monster${this.monsterID}.png`;
    }
  },
  mounted() {
    
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
        this.currentTurn = 'player';
        console.log(this.currentTurn);
        this.winner = null;
        //const response = await api.post('/start-game');
        //console.log(response.data);
        //this.cupState = response.data.state;
        this.updateCups();
      } catch (error) {
        console.error("Error starting game:", error);
      }
    },

    async timer() {
      console.log('Timer button clicked');
      clearInterval(this.timerInterval);
      this.timerActive = true;
      this.timerValue = 3;
      this.timerInterval = setInterval(() => {
        if (this.timerValue > 0) {
          this.timerValue--;
        } else {
          this.timerActive = false;
          clearInterval(this.timerInterval);
          this.currentTurn = 'robot';
          this.robotTurn();
        }
      }, 1000);

    },
    async robotTurn() {
      try {
        await api.post('/robot-turn');
        this.currentTurn = 'player';
        console.log("Player's turn again");
      } catch (error) {
        console.error("Error in robot turn:", error);
      }
    },
    async dropCup(cupId) {
      try {
        await api.post('/drop-cup', { cup_id: cupId });
        console.log(`Dropped ${cupId}`);
      } catch (err) {
        console.error('Failed to drop cup:', err);
      }
    },
    robotIndex(row, col) {
      // row: 0 = 3 cups, 1 = 2 cups, 2 = 1 cup
      return (row * 3) - (row * (row - 1)) / 2 + (col - 1);
    },
    playerIndex(row, col) {
      // row: 0 = 1 cup, 1 = 2 cups, 2 = 3 cups
      return (row * (row + 1)) / 2 + (col - 1);
    },
    handleCupClick(id) {
      this.cupVisibility[id] = false;
      this.dropCup(id); // Pi trigger
      this.gameOver();
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
    async restartGame() {
      window.location.reload();
      this.winner = null;
      try {
        await api.post('/reset-cups');
        console.log('cups reset');
      } catch (err) {
        console.error('failed to reset cups');
      }
    },
    gameOver() {
      const robotCupsGone = this.cupVisibility.slice(0, 6).every(v => !v);
      const playerCupsGone = this.cupVisibility.slice(6).every(v => !v);
      if (playerCupsGone) {
        this.winner = 'robot';
      } else if(robotCupsGone) {
        this.winner = 'player';
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
  align-items: flex-start;      /* Top align */
  justify-content: space-between; /* Push to ends */
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
.cups-grid {
  width: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-right: 2rem;
}

.cup-row {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

</style>
