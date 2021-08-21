<template>
  <q-page class="trip-page">
    <q-form class="half_page first q-gutter-md ">
      <template
        v-for="item in items"
        :key="item.name"
      >
        <q-input
          v-if="['text', 'textarea', 'number'].includes(item.type)"
          filled
          disable
          class="form_item"
          v-model="item.value"
          :type="item.type"
          :label="item.label"
        />
      </template>
    </q-form>
    <q-separator />
    <div class="half_page second">
      <q-table
        title="Блогеры"
        class="page_grid"
        hide-bottom
        :rows="object ? object.Bloggers : []"
        :columns="columns"
        :pagination="pagination"
        row-key="name"
        v-on:row-click="handler_table_row_click"
      >
        <template #no-data>
          <app-empty-info />
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
const ALLOW_PROPS = {
  name: 'Название',
  date: 'Дата',
  invitation_text: 'Текст приглашения',
  Bloggers: 'Блогеры',
  Posts: 'Посты',
  Hashtags: 'Хештеги',
  Route: 'Прикрепленный маршрут',
}

export default {
  mounted () {
    this.prepare_items()
  },

  data: () => ({
    is_loading: false,
    items: [],
    object: {},
    pagination: {
      sortBy: 'name',
      rowsPerPage: 20
    },
    columns: [
      {
        name: 'username',
        label: 'Имя пользователя',
        sortable: true,
        field: 'username'
      },
      {
        name: 'full_name',
        label: 'Полное имя',
        sortable: true,
        field: 'full_name'
      },
      {
        name: 'followers',
        label: 'Число подписчиков',
        sortable: true,
        field: 'followers'
      },
      {
        name: 'is_business_account',
        label: 'Бизнес-аккаунт',
        format: val => val ? 'Да' : 'Нет',
        field: 'followers'
      },
      // {
      //   name: 'count_likes',
      //   label: 'Число лайков',
      //   field: 'count_likes'
      // },
      // {
      //   name: 'count_comments',
      //   label: 'Число комментариев',
      //   field: 'count_comments'
      // },
      // {
      //   name: 'count_posts',
      //   label: 'Число постов',
      //   field: 'count_posts'
      // },
      // {
      //   name: 'er',
      //   label: 'ER',
      //   field: 'er'
      // },
      // {
      //   name: 'public',
      //   label: 'Доступен',
      //   field: 'public'
      // },
      // {
      //   name: 'verify',
      //   label: 'Потвержден',
      //   field: 'verify'
      // },
      // {
      //   name: 'Posts',
      //   label: 'Посты',
      //   format: val => `${val ? val.length : 0}`,
      //   field: 'Posts'
      // },
    ]
  }),

  watch: {
    id () {
      this.prepare_items()
    }
  },

  computed: {
    id () {
      return this.$route.params.id
    },
  },

  methods: {
    handler_table_row_click (event, row, index) {
      window.open(`https://www.instagram.com/${row.username}`, '_blank')
    },

    prepare_items () {
      this.items.splice(0, this.items.length)
      this.object = this.$store.getters['trips/get_item'](this.id)
      if (this.object)
        Object.keys(this.object).forEach(prop_name => {
          if (Object.keys(ALLOW_PROPS).includes(prop_name)) {
            let type = typeof this.object[prop_name]
            if (type == 'string')
              this.items.push({
                name: prop_name,
                value: this.object[prop_name],
                label: ALLOW_PROPS[prop_name],
                type: prop_name == 'invitation_text' ? 'textarea' : 'text'
              })
            else if (type == 'number')
              this.items.push({
                name: prop_name,
                value: this.object[prop_name],
                label: ALLOW_PROPS[prop_name],
                type: 'number'
              })
            else if (type == 'object')
              if (Array.isArray(this.object[prop_name]))
                this.items.push({
                  name: prop_name,
                  value: this.object[prop_name],
                  label: ALLOW_PROPS[prop_name],
                  type: 'list'
                })
              else
                this.items.push({
                  name: prop_name,
                  value: this.object[prop_name],
                  label: ALLOW_PROPS[prop_name],
                  type: 'object'
                })
          }
        })
    },
  }
}
</script>

<style lang="scss">
.trip-page {
  display: flex;
  flex-direction: column;

  .half_page {
    overflow-y: auto;

    &.first {
      height: calc(calc(calc(100vh - 72px) / 2) - 200px);
    }

    &.second {
      height: calc(calc(calc(100vh - 72px) / 2) + 200px);
    }

    & > .page_grid {
      height: calc(calc(calc(100vh - 72px) / 2) + 200px);
    }
  }

  .q-form {
    width: 1000px;
    margin: 0 auto;
    display: flex;

    .form_item {
      width: 300px;
    }
  }

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
</style>
