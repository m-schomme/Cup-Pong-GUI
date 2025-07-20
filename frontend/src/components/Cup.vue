<template>
  <div
    class="cup"
    :class="visible ? 'cup-filled' : 'cup-hollow'"
    @click="handleClick"
  >
    <span class="cup-label">{{ cupId }}</span>
  </div>
</template>

<script>
export default {
  name: 'Cup',
  props: {
    visible: {
      type: Boolean,
      default: true
    },
    cupId: {
      type: Number,
      required: true
    }
  },
  methods: {
    handleClick() {
      this.$emit('cup-clicked', this.cupId);
    }
  }
};
</script>

<style scoped>
.cup {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 6px;
  cursor: pointer;
  border: 3px solid darkred;
  transition: all 0.2s ease;
  position:relative; 
}

.cup-filled {
  background-color: red;
  border-style: solid;
}

.cup-hollow {
  background-color: transparent;
  border-style: dashed;
}

.cup-label {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1rem;
  color: white;
  pointer-events: none; 
}
</style>
