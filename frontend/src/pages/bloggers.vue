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
        name: "username",
        label: "Аккаунт Instagram",
        sortable: true,
        field: "username",
      },
      {
        name: "full_name",
        label: "Имя",
        sortable: true,
        field: "full_name",
      },
      {
        name: "count_likes",
        label: "Лайки",
        sortable: true,
        field: "count_likes",
      },
      {
        name: "count_comments",
        label: "Комментарии",
        sortable: true,
        field: "count_comments",
      },
      {
        name: "count_posts",
        label: "Посты",
        sortable: true,
        field: "count_posts",
      },
      {
        name: "followers",
        label: "Подписчики",
        sortable: true,
        field: "followers",
      },
      {
        name: "er",
        label: "ER",
        sortable: true,
        field: "er",
      },
      {
        name: "is_business_account",
        label: "Бизнес аккаунт",
        sortable: true,
        field: "is_business_account",
        format: (val) => `${val ? "Да" : "Нет"}`,
      },
      {
        name: "verify",
        label: "Подтвержденный",
        sortable: true,
        field: "verify",
        format: (val) => `${val ? "Да" : "Нет"}`,
      },
    ],
  }),

  computed: {
    rows() {
      return this.$store.getters["bloggers/get_items"];
    },
  },

  methods: {
    get_random_list() {
      let count = Math.round(Math.random() * 20);
      return Array.from(Array(count).keys());
    },

    async update_data() {
      this.is_loading = true;
      await this.$store.dispatch("bloggers/get_items");
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
