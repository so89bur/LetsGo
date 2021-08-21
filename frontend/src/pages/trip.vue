<template>
  <q-page class="trip-page">
    <q-form class="half_page q-gutter-md ">
      <template
        v-for="item in items"
        :key="item.name"
      >
        <q-input
          v-if="['string', 'number'].includes(item.type)"
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
    <div class="half_page">
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
        label: 'Название',
        sortable: true,
        field: 'username'
      },
      {
        name: 'full_name',
        label: 'Дата',
        sortable: true,
        field: 'full_name'
      },
      {
        name: 'followers',
        label: 'Число подписчиков',
        field: 'followers'
      },
      {
        name: 'count_likes',
        label: 'Число лайков',
        field: 'count_likes'
      },
      {
        name: 'count_comments',
        label: 'Число комментариев',
        field: 'count_comments'
      },
      {
        name: 'count_posts',
        label: 'Число постов',
        field: 'count_posts'
      },
      {
        name: 'er',
        label: 'ER',
        field: 'er'
      },
      {
        name: 'public',
        label: 'Доступен',
        field: 'public'
      },
      {
        name: 'verify',
        label: 'Потвержден',
        field: 'verify'
      },
      {
        name: 'Posts',
        label: 'Посты',
        format: val => `${val ? val.length : 0}`,
        field: 'Posts'
      },
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
    prepare_items () {
      this.items.splice(0, this.items.length)
      this.object = this.$store.getters['trips/get_item'](this.id)
      if (this.object)
        Object.keys(item).forEach(prop_name => {
          if (Object.keys(ALLOW_PROPS).includes(prop_name)) {
            let type = typeof item[prop_name]
            if (type == 'string')
              this.items.push({
                name: prop_name,
                value: item[prop_name],
                label: ALLOW_PROPS[prop_name],
                type: 'string'
              })
            else if (type == 'number')
              this.items.push({
                name: prop_name,
                value: item[prop_name],
                label: ALLOW_PROPS[prop_name],
                type: 'number'
              })
            else if (type == 'object')
              if (Array.isArray(item[prop_name]))
                this.items.push({
                  name: prop_name,
                  value: item[prop_name],
                  label: ALLOW_PROPS[prop_name],
                  type: 'list'
                })
              else
                this.items.push({
                  name: prop_name,
                  value: item[prop_name],
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
    height: calc(calc(100vh - 72px) / 2);
  }

  .q-form {
    width: 1000px;
    margin: 0 auto;
    display: flex;

    .form_item {
      width: 300px;
    }
  }
}
</style>
