<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="q-pa-md">
        <q-toolbar-title
          class="cursor-pointer"
          v-on:click="$router.push('/trips')"
        >
          Let's go
        </q-toolbar-title>
        <template
          v-for="(item, index) in menu"
          :key="index"
        >
          <q-btn
            stretch
            flat
            :label="item.label"
            :class="`menu_item ${item.name == $route.name ? 'active' : ''}`"
            v-on:click="$router.push(`/${item.name}`)"
          />
          <q-separator
            v-if="index < menu.length - 1"
            dark
            vertical
          />
        </template>
        <!-- <q-btn
          v-if="$route.name == 'index'"
          label="Добавить"
          color="secondary"
          no-caps
        /> -->
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
    menu () {
      return [
        { label: 'Поездки', name: 'trips' },
        { label: 'Маршруты', name: 'routes' },
        { label: 'Блогеры', name: 'bloggers' },
        { label: 'Посты', name: 'posts' },
      ]
    },

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

<style lang="scss">
.menu_item.active {
  background-color: $accent;
  color: $light;
}
</style>
