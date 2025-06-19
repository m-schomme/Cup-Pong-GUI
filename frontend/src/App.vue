<template>
  <div class="surface-100 min-h-screen">
    <NameEntry v-if="step === 'name'" @nameSubmitted="handleNameSubmitted" />
    <MonsterSelect v-if="step === 'monster'" :playerName="playerName" @monsterSelected="handleMonsterSelected" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import NameEntry from './components/NameEntry.vue';
import MonsterSelect from './components/MonsterSelect.vue';

const step = ref('name');
const playerName = ref('');
const selectedMonster = ref(null);

function handleNameSubmitted(name) {
  playerName.value = name;
  step.value = 'monster';
}

function handleMonsterSelected(monsterId) {
  selectedMonster.value = monsterId;
  console.log('Monster selected:', monsterId);
  // You can now move to game logic or next step
}
</script>
