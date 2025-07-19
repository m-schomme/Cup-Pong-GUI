<template>
  <div class="surface-100 min-h-screen p-0">
    <div class="flex justify-content-center" >
      <Card class="shadow-5 border-round-lg w-full max-w-4xl mt-1 p-2 "style="max-height: 86.5vh;">
        <template #title>
          <div 
            class="monster-title-container" :class="{ 'monster-title--shrunk': selectedMonster }">
            <b class="monster-title" style="margin: 0; padding: 0;">PICK YOUR MONSTER</b>
          </div>
        </template>

        <template #content>
            <div class="flex flex-wrap gap-4 w-full justify-content-center">
                <Card 
                    v-for="monster in monsters" 
                    :key="monster.id"
                    @click="selectMonster(monster.id)"
                    class="monster-card flex flex-column cursor-pointer transition-all border-round-lg shadow-3 p-3 justify-content-between"
                    :class="[
                      selectedMonster === monster.id 
                      ? 'border-primary border-2 shadow-10 scale-120' 
                      : (selectedMonster ? 'monster-card--shrunk' : '')
                    ]"
                    style="width: 14em; height: 16.5em;"
                >
                    <template #content>
                        <!-- <img :src="monster.src" :alt="monster.name" class=" justify-content-center w-10rem h-10rem border-round-lg mb-3 block" /> -->
                         <div class="monster-image-container">
                            <img 
                              :src="monster.src" 
                              :alt="monster.name" 
                              class="monster-image"
                              loading="lazy"
                            />
                          </div>
                    </template>
                    <template #footer>
                        <div class=" text-center font-semibold text-lg block mt-auto" >{{ monster.name }}</div>
                    </template>
                </Card>
            </div>
            <div v-if="selectedMonster" class=" text-center text-sm text-green-600 font-bold p-0" style="margin-bottom:0px !important; padding-bottom:0 !important;" >
                <Button label="Let's Play" @click="emit('monsterSelected', selectedMonster)" class="monster-btn" />
            </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<style scoped>
    .surface-100 {
      margin: 0 !important;
      padding: 0 !important;
    }
    ::v-deep(.p-card-content) {
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    padding: 0 !important;
    }

    ::v-deep(.p-card-title) {
    padding-top: 0 !important;
    padding-bottom: 0.4rem !important;
    margin: 0 !important;
    line-height: 1.1;
    }
    ::v-deep(.p-card-footer) {
    padding: 0 !important;
    margin-top: auto;
    align-content: flex-end !important;
    }
    ::v-deep(.p-card) {
    padding-top:0 !important;
    }
    .monster-title-container {
      margin: 0 !important;
      padding: 0.22em 0 !important; /* adjust as needed */
      text-align: center;
      padding: 0 !important;
      font-family: 'Archivo Narrow', sans-serif;
      color: #20B2AA;
      font-size: clamp(2rem, 6vw, 5rem);
      font-weight: bold;
      line-height: 1.1;
    }
    .monster-title--shrunk {
      transform: scale(0.55);
      opacity: 0.5;
      filter: blur(1px);
      transition: transform 0.3s, opacity 0.3s, filter 0.3s;
    }
    .monster-title {
      font-family: 'Archivo Narrow', sans-serif;
      color: #20B2AA;
      font-size: clamp(1.75rem, 5.5vw, 4.5rem);
    }
    .monster-card {
      width: 100%;
      max-width: 14.5rem;
      min-width: 10rem;
      height: 16.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 0 !important;
      margin:0rem;
    }

    .monster-image-container {
      width: 100%;
      height: 13rem; /* or use clamp(7rem, 20vw, 12rem) for more flexibility */
      display: flex;
      align-items: center;
      justify-content: center;
      flex: 1 1 auto;
      padding: 0;
      margin: 0;
    }

    .monster-image {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      border-radius: 0rem;
      padding: 0;
      margin: 0;
    }
    .monster-card--shrunk {
      transform: scale(0.85);
      opacity: 0.5;
      filter: blur(1px);
      transition: transform 0.3s, opacity 0.3s, filter 0.3s;
      z-index: 0;
    }
    .scale-120 {
      transform: scale(1.08);
      z-index: 1;
      transition: transform 0.3s;
    }
    .monster-btn {
      padding: 0.10rem 0.5rem !important; /* smaller padding */
      font-size: 1rem !important;       /* smaller font */
      min-width: unset !important;
      min-height: unset !important;
      margin-top: 0.5rem !important;
      margin-bottom: 0 !important;
      box-sizing: border-box;
    }
</style>


<script setup>
    import { ref } from 'vue';
    import Card from 'primevue/card';
    import Button from 'primevue/button';
    import { onMounted } from 'vue';

    const props = defineProps({
    playerName: String
    });

    onMounted(() => {
      window.scrollTo(0, 0);
    });

    const emit = defineEmits(['monsterSelected']);
    const selectedMonster = ref(null);

    function selectMonster(id) {
        selectedMonster.value = id;
    }
   
    const monsters = [
    { id: 1, name: 'Bob', src: '/src/assets/monsters/monster1.png' },
    { id: 2, name: 'Sam', src: '/src/assets/monsters/monster2.png' },
    { id: 3, name: 'Pookie', src: '/src/assets/monsters/monster3.png' },
    { id: 4, name: 'Nutter', src: '/src/assets/monsters/monster4.png' },
    { id: 5, name: 'Johnston', src: '/src/assets/monsters/monster5.png' },
    { id: 6, name: 'M1k3', src: '/src/assets/monsters/monster6.png' },
    { id: 7, name: 'Schubert', src: '/src/assets/monsters/monster7.png' },
    { id: 8, name: 'Tarter', src: '/src/assets/monsters/monster8.png' },
    ];

</script>
