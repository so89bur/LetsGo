<template>
  <div
    v-once
    class="empty__wrapper"
  >
    <div class="empty__info">
      <q-icon
        class="empty__icon"
        name="fas fa-info-circle"
      />
      <div class="empty__label">
        {{ text }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: 'Здесь пока пусто'
    }
  }
}
</script>

<style lang="scss">
.empty__wrapper {
  width: 100%;
  height: 100%;
  position: relative;

  & > .empty__info {
    position: absolute;
    left: calc(50% - 100px);
    top: calc(50% - 60px);
    width: 200px;
    height: 120px;
    background-color: $primary;

    border-radius: 16px;
    & > .empty__icon {
      margin-top: 15px;
      height: 60px;
      width: 100%;
      line-height: 60px;
      font-size: 50px;
      text-align: center;
      color: $light;
    }

    & > .empty__label {
      font-size: 16px;
      line-height: 20px;
      text-align: center;
      color: $light;
    }
  }
}
</style>
