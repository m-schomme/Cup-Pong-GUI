<template>
  <div class="surface-100 min-h-full p-3">
    <div class="flex justify-content-center">
      <Card class="shadow-5 border-round-lg w-full max-w-40rem p-4">
        <template #title>
          <div class="text-center  font-bold" style="font-family: 'Archivo Narrow', sans-serif; color: #20B2AA; font-size: 90px;">
            <b>PICK YOUR MONSTER</b>
          </div>
        </template>

        <template #content>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 w-full justify-items-center content-center">
                <Card 
                    v-for="monster in monsters" 
                    :key="monster.id"
                    @click="selectMonster(monster.id)"
                    class=" flex cursor-pointer transition-all border-round-lg shadow-3 p-3 justify-items-center justify-content-center "
                    style = "width: 22%;"
                    :class="selectedMonster === monster.id ? 'border-primary border-3 shadow-10 scale-120' : ''"
                >
                    <template #title>
                        <img :src="monster.src" :alt="monster.name" class=" justify-content-center w-10rem h-10rem border-round-lg mb-3 block" />
                    </template>
                    <template #footer>
                        <div class="text-center font-semibold text-lg block">{{ monster.name }}</div>
                    </template>
                </Card>
            </div>
            <div v-if="selectedMonster" class="mt-5 text-center text-xl text-green-600 font-bold">
                <Button label="Let's Play" />
            </div>
        </template>
      </Card>
    </div>
  </div>
</template>

<style scoped>
    ::v-deep(.p-card-content) {
    padding: 0 !important;
    }

    ::v-deep(.p-card-title) {
    padding: 0 !important;
    }
    ::v-deep(.p-card-footer) {
    padding: 0 !important;
    }
    ::v-deep(.p-card) {
    padding-top:0 !important;
    }
</style>


<script setup>
    import { ref } from 'vue';
    import Card from 'primevue/card';
    import Button from 'primevue/button';

    const props = defineProps({
    playerName: String
    });

    const emit = defineEmits(['monsterSelected']);
    const selectedMonster = ref(null);

    function selectMonster(id) {
        selectedMonster.value = id;
    }
    // Your 8 monsters:
    const monsters = [
    { id: 1, name: 'Bob', src: '/src/assets/monsters/monster1.png' },
    { id: 2, name: 'Sam', src: '/src/assets/monsters/monster2.png' },
    { id: 3, name: 'Pookie', src: '/src/assets/monsters/monster3.png' },
    { id: 4, name: 'Monster 4', src: '/src/assets/monsters/monster4.png' },
    { id: 5, name: 'Monster 5', src: '/src/assets/monsters/monster5.png' },
    { id: 6, name: 'Monster 6', src: '/src/assets/monsters/monster6.png' },
    { id: 7, name: 'Monster 7', src: '/src/assets/monsters/monster7.png' },
    { id: 8, name: 'Monster 8', src: '/src/assets/monsters/monster8.png' },
    ];

</script>
