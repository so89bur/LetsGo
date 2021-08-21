<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="q-pa-md">
        <q-toolbar-title class="text-center">
          {{ title }}
        </q-toolbar-title>
        <q-btn
          v-if="$route.name == 'index'"
          label="Добавить"
          color="secondary"
          no-caps
        />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  data: () => ({

  }),

  computed: {
    title () {
      let title = null
      let title_type = typeof this.$route.meta.title
      if (title_type == 'string')
        title = this.$route.meta.title
      else if (title_type == 'function')
        title = this.$route.meta.title(this.$route)
      if (typeof title == 'string')
        return title
      else
        return "Let's go"
    }
  }
}
</script>
