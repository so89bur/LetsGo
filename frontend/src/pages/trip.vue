<template>
  <q-page class="trip-page">
    <q-card class="page_card">
      <q-toolbar class="bg-primary text-white">
        {{ is_new ? 'Добавление новой поездки' : 'Редактирование поездки' }}
      </q-toolbar>
      <q-dialog v-model="is_showed_form_for_attach_blogger">
        <q-card style="width: 550px">
          <q-card-section class="row items-center q-pb-none">
            <div class="text-h6">Привязка блогера</div>
            <q-space />
            <q-btn
              icon="fas fa-times"
              flat
              round
              dense
              v-close-popup
            />
          </q-card-section>

          <q-card-section>
            <q-select
              filled
              v-model="selected_blogger"
              :options="bloggers"
              label="Выеберите блогера"
              emit-value
              map-options
            />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              flat
              label="Отмена"
              color="primary"
              v-close-popup
            />
            <q-btn
              flat
              label="Добавить"
              color="primary"
              v-on:click="attach_bloger(selected_blogger)"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>
      <q-form class="half_page first q-gutter-md ">
        <template
          v-for="item in items"
          :key="item.name"
        >
          <q-input
            v-if="['text', 'textarea', 'number'].includes(item.type)"
            filled
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
          class="page_grid"
          hide-bottom
          :loading="is_loading"
          :rows="object ? object.Bloggers : []"
          :columns="columns"
          :pagination="pagination"
          row-key="name"
        >
          <template #no-data>
            <app-empty-info />
          </template>

          <template #header="props">
            <q-tr :props="props">
              <q-th />
              <q-th />
              <q-th
                v-for="col in props.cols"
                :key="col.name"
                :props="props"
              >
                {{ col.label }}
              </q-th>
            </q-tr>
          </template>

          <template #body="props">
            <q-tr :props="props">
              <q-td>
                <q-btn
                  round
                  flat
                  color="primary"
                  title="Исключить блогера из поездки"
                  icon="fas fa-trash"
                  v-on:click="detach_bloger(props.row.id)"
                />
              </q-td>
              <q-td>
                <q-checkbox
                  v-model="props.row.verify"
                  size="lg"
                />
              </q-td>
              <q-td
                v-for="col in columns"
                :key="col.name"
                :props="props"
                class="cursor-pointer"
                @click="handler_table_row_click(props.row)"
              >
                {{ props.row[col.name] }}
              </q-td>
            </q-tr>
          </template>

          <template #top>
            <div class="row full-width">
              <div class="table_title q-pa-sm">Блогеры</div>
              <q-space />
              <q-btn
                round
                flat
                color="primary"
                title="Добавить нового блогера"
                icon="fas fa-plus-circle"
                v-on:click="show_form_for_attach_blogger"
              />
            </div>
          </template>
        </q-table>
      </div>
    </q-card>
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
    this.$store.dispatch('bloggers/get_items')
    this.prepare_items()
  },

  data: () => ({
    is_loading: false,
    selected_blogger: null,
    is_showed_form_for_attach_blogger: false,
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
    ]
  }),

  watch: {
    id () {
      this.prepare_items()
    },
  },

  computed: {
    id () {
      return this.$route.params.id
    },

    is_new () {
      return this.id == 'new'
    },

    bloggers () {
      return this.$store.getters['bloggers/get_items'].map(item => ({
        label: item.username,
        value: item.id,
      }))
    }
  },

  methods: {
    handler_table_row_click (row) {
      window.open(`https://www.instagram.com/${row.username}`, '_blank')
    },

    show_form_for_attach_blogger () {
      this.is_showed_form_for_attach_blogger = true
    },

    async attach_bloger (blogger_id) {
      this.is_loading = true
      await this.$store.dispatch('trips/attach_blogger', {
        trip_id: this.id,
        blogger_id: blogger_id
      })
      this.is_showed_form_for_attach_blogger = false
      this.selected_blogger = null
      setTimeout(async () => {
        await this.$store.dispatch('trips/update_item', this.id)
        this.prepare_items()
        this.is_loading = false
      }, 500)
    },

    async detach_bloger (blogger_id) {
      this.is_loading = true
      await this.$store.dispatch('trips/detach_blogger', {
        trip_id: this.id,
        blogger_id: blogger_id
      })
      setTimeout(async () => {
        await this.$store.dispatch('trips/update_item', this.id)
        this.prepare_items()
        this.is_loading = false
      }, 500)
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

  & > .page_card {
    width: 1000px;
    height: calc(100vh - 150px);
    position: relative;
    margin: 16px auto;
  }

  .half_page {
    overflow-y: auto;
    height: calc(50%);

    & > .page_grid {
      padding: 16px;
      height: 100%;
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
      background-color: rgba($color: $accent, $alpha: 0.2);
    }
  }
}
</style>
