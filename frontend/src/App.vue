<template>
  <start-loader v-if="is_loading" />
  <mobile v-else-if="$q.screen.lt.md" />
  <desktop v-else />
</template>

<script>
import { defineAsyncComponent } from 'vue'

export default {
  components: {
    'start-loader': defineAsyncComponent(() => import('./components/start.vue')),
    desktop: defineAsyncComponent(() => import('./layouts/desktop.vue')),
    mobile: defineAsyncComponent(() => import('./layouts/mobile.vue')),
  },

  mounted () {
    this.is_loading = true
    this.is_loading = false
  },

  data: () => ({
    is_loading: false
  })
}
</script>
