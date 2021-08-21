import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : createWebHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.MODE === 'ssr' ? void 0 : process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach((to, from, next) => {
    if (!process.env.SERVER) {
      let title = null
      let title_type = typeof to.meta.title
      if (title_type == 'string')
        title = to.meta.title
      else if (title_type == 'function')
        title = to.meta.title(to)
      if (typeof title == 'string')
        document.title = title
      else
        document.title = "Let's go"
    }
    next()
  })

  return Router
})
