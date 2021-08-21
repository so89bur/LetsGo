import { POST, GET, DELETE, PUT } from './../../helpers'

const state_generator = () => ({
  items: {},
  info: {
    total: 0
  },
})

export default {
  state: state_generator(),

  getters: {
    get_item: state => id => {
      return state.items[id]
    },

    get_items (state) {
      return Object.values(state.items).sort((a, b) => {
        let a_id = parseInt(a.id)
        let b_id = parseInt(b.id)
        if (a_id < b_id) return -1
        if (a_id > b_id) return 1
        return 0
      })
    },
  },

  mutations: {
    reset (state) {
      const initial = state_generator()
      Object.keys(initial).forEach(key => { state[key] = initial[key] })
    },

    set_item (state, info) {
      state.items[info.id] = info
    },

    set_info (state, info) {
      if (info) {
        let allow_props = Object.keys(state.info)
        Object.keys(info).forEach(prop => {
          if (allow_props.includes(prop))
            state.info[prop] = info[prop]
        })
      }
    },
  },

  actions: {
    async new (cxt, info) {
      let data = await POST('/trip', info)
      if (data.success)
        cxt.commit('show_info', 'Место успешно добавлено', { root: true })
      else
        cxt.commit('show_error', 'Не удалось добавить место', { root: true })
      resolve()
    },

    async get_items (cxt, info) {
      info = info ? info : {}
      let data = await GET('/places', {
        start: info.start || 0,
        limit: info.limit || 20,
        order_by: info.order_by || 'id',
        order_type: info.order_type || 'asc',
        filter_prop: info.filter_prop || null,
        filter_value: info.filter_value || null,
      })
      if (data.success) {
        cxt.commit('set_info', data)
        if (Array.isArray(data.result))
          data.result.forEach(item => {
            cxt.commit('set_item', item)
          })
      } else {
        let err_msg = 'Не удалось получить список мест'
        cxt.commit('show_error', err_msg, { root: true })
      }
    },

    async delete (cxt, trip_id) {
      let data = await DELETE(`/place/${trip_id}`)
      if (data.success)
        cxt.commit('show_info', 'Место успешно удалено', { root: true })
      else
        cxt.commit('show_error', 'Не удалось удалить место', { root: true })
    },

    async update (cxt, info) {
      let data = await PUT(`/place/${info.id}`, info)
      if (data.success)
        cxt.commit('show_info', 'Место успешно изменено', { root: true })
      else
        cxt.commit('show_error', 'Не удалось изменить место', { root: true })
    },
  },

  namespaced: true,
}
