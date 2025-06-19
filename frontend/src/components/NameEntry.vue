<template>
<div class="flex justify-content-center align-items-center h-full p-3">
    <Card class="shadow-5 border-round-lg w-full max-w-40rem p-3">
        <template #header>
            <div class="flex justify-content-center">
                <img 
                  alt="Cup Pong Logo" 
                  src="/src/assets/cupponglogo.jpg" 
                  class="border-circle shadow-3" 
                  style="width: 300px; height: 300px;"
                />
            </div>
        </template>

        <template #title>
            <div class="text-center text-4xl font-bold text-primary" style="font-family: 'Montserrat', sans-serif;">
                CUP PONG CHALLENGE
            </div>
        </template>

        <template #subtitle>
            <div class="text-center text-2xl text-color-secondary" style="font-family: 'Archivo Narrow', sans-serif;">
                Can you beat the robot?
            </div>
        </template>

        <template #content>
            <div class="flex flex-col align-items-center gap-2">
                <p class="text-center text-md text-color">
                    Enter your name to begin the ultimate challenge!
                </p>

                <div class="w-full flex flex-column gap-2">
                    <!-- <label for="playerName" class="font-semibold">Player Name:</label> -->
                    <InputText id="playerName" v-model="playerName" placeholder="Enter Name" class="w-full text-lg p-3 border-round-md shadow-1" />
                    <div v-if="nameError" class="text-red-500 font-semibold">{{ nameError }}</div>
                </div>
            </div>
            <div class="flex justify-content-center gap-2 mt-3">
                <Button label="Submit" @click="submitForm" class=" p-button-rounded shadow-2 px-5" />
            </div>
        </template>
    </Card>
  </div>
</template>
<style scoped>
    .card-container {
        max-height: 90vh;
        overflow-y: auto;
    }
</style>

<script setup>
import { ref } from 'vue';
import Card from 'primevue/card';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import { defineEmits } from 'vue';
// import cupPongLogo from '@/assets/cupponglogo.jpg';

const emit = defineEmits(['nameSubmitted']);
const playerName = ref('');
const nameError = ref('');

function submitForm() {
  if (!playerName.value.trim()) {
    nameError.value = 'Name is required';
  } else {
    nameError.value = '';
    console.log("Submitted:", playerName.value);
    emit('nameSubmitted', playerName.value);
    // Move forward to next game screen here
  }
}
</script>
