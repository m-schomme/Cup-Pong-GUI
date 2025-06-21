<template>
  <div class="flex justify-content-center align-items-center h-screen p-3">
    <Card class="shadow-5 border-round-lg w-full max-w-50rem p-3">
      <template #title>
        <div class="text-center text-3xl font-bold text-teal-500">
          Game Play
        </div>
      </template>

      <template #content>
        
        <div class="flex lg:flex-row gap-4">
          <div class="w-fullflex items-center justify-center p-2 border-r">
            <div class = "col items-center">
                <img
                :src="monsterImage"
                :alt="playerName"
                class="max-w-full h-auto rounded-lg shadow-lg"
                style="max-height: 400px;"
                />
                <h2 class="text-2xl font-semibold mt-2">{{ playerName }}</h2>
            </div>
          </div>
          <Divider layout="vertical" />
          <div class="w-full  flex items-center justify-center p-2">
            <div class="w-full h-full bg-gray-100 rounded-lg border-dashed border-2 flex items-center justify-center text-lg text-gray-600">
              Cup Pong Game Goes Here
            </div>
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<script>
export default {
  name: 'GamePlay',
  props: {
    playerName: {
      type: String,
      default: 'Player 1'
    },
    monsterID: {
      type: Number,
      required: true
    }
  },
  computed: {
    monsterImage() {
      return `/src/assets/monsters/monster${this.monsterID}.png`;
    }
  }
};
</script>

