<template>
  <q-page class="index-page">
    <div class="trip_wrapper">
      <app-loader v-if="is_loading" />

      <q-input
        filled
        class="form_item"
        v-model="instagram_login"
        label="instagram login"
      />
      <q-input
        filled
        class="form_item"
        v-model="instagram_password"
        label="instagram password"
      />
      <q-btn
        color="white"
        text-color="black"
        label="Сохранить"
        @click="save_settings"
      />
    </div>
    <!-- <div class="logs_wrapper">
    </div> -->
  </q-page>
</template>

<script>
import { parse_ms } from "../helpers";

import { POST, GET, DELETE, PUT } from './../helpers'
import { Notify } from 'quasar'

export default {
  mounted() {
    this.load_settings();
  },

  data: () => ({
    is_loading: false,
    instagram_login: "",
    instagram_password: "",
  }),

  methods: {
    async load_settings() {
      this.is_loading = true;
      let settings = await GET('/settings');
      this.instagram_login = settings.instagram_login;
      this.instagram_password = settings.instagram_password;
      this.is_loading = false;
    },

    async save_settings() {
      let data = {
        instagram_login: this.instagram_login,
        instagram_password: this.instagram_password,
      }
      await POST('/settings', data);
      Notify.create('Настройки сохранены')
    },
  },
};
</script>

<style lang="scss">
.index-page {
  & > .trip_wrapper {
    height: calc(100vh - 60px);
    overflow-y: auto;

    .page_grid {
      height: calc(100vh - 60px);

      .q-table {
        .q-table__top,
        .q-table__bottom,
        thead > tr:first-child > th {
          background-color: $primary;
          color: $light;
        }

        & > thead > tr {
          &:first-child > th {
            top: 0;
          }

          & > th {
            position: sticky;
            z-index: 1;
          }
        }

        & > tbody > tr:hover {
          background-color: $accent;
          color: $light;
        }
      }
    }
  }
}
</style>
