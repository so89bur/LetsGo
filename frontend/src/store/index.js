import { store } from "quasar/wrappers";
import { createStore } from "vuex";

import trips from "./modules/trips";
import bloggers from "./modules/bloggers";
import hashtags from "./modules/hashtags";

import { POST, GET, PUT, init_helpers } from "./../helpers";

const ALLOW_FOR_PREPARE = [];

const state_generator = () => ({
  notifications: [],
});

const Store = createStore({
  modules: {
    trips,
    bloggers,
    hashtags,
  },

  state: state_generator(),

  mutations: {
    reset(state) {
      const initial = state_generator();
      Object.keys(initial).forEach((key) => {
        state[key] = initial[key];
      });
    },

    show_error(state, error) {
      console.log(error);
      state.notifications.push({
        id: new Date().toString(),
        active: true,
        label: error,
        type: "error",
      });
    },

    show_info(state, info) {
      state.notifications.push({
        id: new Date().toString(),
        active: true,
        label: info,
        type: "info",
      });
    },

    hide_notification(state, index) {
      state.notifications.splice(index, 1);
    },

    prepare(state, info) {
      Object.keys(info).forEach((prop) => {
        if (
          Object.keys(state).includes(prop) &&
          ALLOW_FOR_PREPARE.includes(prop)
        )
          state[prop] = info[prop];
      });
    },
  },

  getters: {
    get_notifications(state) {
      return state.notifications;
    },
  },

  actions: {
    reset_all({ commit }) {
      commit("reset");
    },

    init({ state, dispatch }) {
      init_helpers();
    },

    async prepare_app(cxt) {
      let data = await GET("prepare");
      if (data.success) cxt.commit("prepare", data.result);
      else cxt.commit("show_error", "Не удалось подготовить приложение");
    },
  },

  strict: process.env.DEBUGGING,
});

export default store(function (/* { ssrContext } */) {
  return Store;
});

export const store_obj = Store;
