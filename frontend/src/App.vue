<template>
  <div class="surface-100 min-h-screen">
    <NameEntry v-if="step === 'name'" @nameSubmitted="handleNameSubmitted" />
    <MonsterSelect v-if="step === 'monster'" :playerName="playerName" @monsterSelected="handleMonsterSelected" />
    <GamePlay v-if="step === 'game'" :playerName="playerName" :monsterID="selectedMonster" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import NameEntry from './components/NameEntry.vue';
import MonsterSelect from './components/MonsterSelect.vue';
import GamePlay from './components/GamePlay.vue';

const step = ref('name');
const playerName = ref('');
const selectedMonster = ref(null);

function handleNameSubmitted(name) {
  playerName.value = name;
  step.value = 'monster';
}

function handleMonsterSelected(monsterID) {
  selectedMonster.value = monsterID;
  step.value = 'game';
}
</script>
