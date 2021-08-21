<template>
  <q-page class="index-page">
    <div class="trip_wrapper">
      <app-loader v-if="is_loading" />
      <q-table
        v-else
        class="page_grid"
        hide-bottom
        :rows="rows"
        :columns="columns"
        :pagination="pagination"
        row-key="name"
      >
        <template #no-data>
          <app-empty-info />
        </template>
      </q-table>
    </div>
    <!-- <div class="logs_wrapper">
    </div> -->
  </q-page>
</template>

<script>
import { parse_ms } from "../helpers";

export default {
  mounted() {
    this.update_data();
  },

  data: () => ({
    is_loading: false,
    pagination: {
      sortBy: "name",
      rowsPerPage: 20,
    },
    columns: [
      {
        name: "name",
        label: "Хештег",
        sortable: true,
        field: "name",
      },
      {
        name: "trips_count",
        label: "Указан в путешествиях",
        sortable: true,
        field: "trips_count",
      },
      {
        name: "posts_count",
        label: "Указан в постах",
        sortable: true,
        field: "posts_count",
      },
    ],
  }),

  computed: {
    rows() {
      return this.$store.getters["hashtags/get_items"];
    },
  },

  methods: {
    get_random_list() {
      let count = Math.round(Math.random() * 20);
      return Array.from(Array(count).keys());
    },

    async update_data() {
      this.is_loading = true;
      await this.$store.dispatch("hashtags/get_items");
      this.is_loading = false;
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
