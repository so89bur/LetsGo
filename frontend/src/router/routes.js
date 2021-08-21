
const routes = [
  {
    path: '/',
    component: () => import('pages/index.vue'),
    name: 'index',
    meta: {
      title: 'Поездки'
    }
  },

  {
    path: '/trips/:id',
    component: () => import('pages/trip.vue'),
    name: 'trip',
    meta: {
      title: (route) => {
        return route.params.id
      }
    }
  },

  {
    path: '/:catchAll(.*)*',
    redirect: '/'
  }
]

export default routes
