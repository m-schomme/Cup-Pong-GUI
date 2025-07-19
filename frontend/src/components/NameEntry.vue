<template>
<div class="fixed top-0 left-0 w-screen h-screen flex justify-content-center items-center px-3 pt-6 overflow-hidden"  style="margin:0 !important;">
    <Card class="shadow-5 border-round-lg  p-4 max-w-full overflow-hidden" style="max-height: 80vh; overflow-y: auto;">
        <template #header>
            <div class="flex justify-content-center">
                <img 
                  alt="Cup Pong Logo" 
                  src="/src/assets/cupponglogo.jpg" 
                  class="border-circle shadow-3 object-contain" 
                  style="width: 100%; max-width:300px;  height: auto;"
                />
            </div>
        </template>

        <template #title>
            <div class="text-center font-bold" style="font-family: 'Archivo Narrow', sans-serif; font-size:3rem; color:coral">
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
            <div class="flex justify-content-center gap-2 mt-2">
                <Button label="Submit" @click="submitForm" class=" p-button-rounded shadow-2 px-2 " />
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
    html, body {
        margin: 0;
        padding: 0;
        height: 100%;
        overscroll-behavior:none;
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
