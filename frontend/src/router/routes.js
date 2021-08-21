
const routes = [
  {
    path: '/trips',
    component: () => import('pages/trips.vue'),
    name: 'trips',
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
    path: '/routes',
    component: () => import('pages/routes.vue'),
    name: 'routes',
    meta: {
      title: 'Маршруты'
    }
  },

  {
    path: '/bloggers',
    component: () => import('pages/bloggers.vue'),
    name: 'bloggers',
    meta: {
      title: 'Блогеры'
    }
  },

  {
    path: '/hashtags',
    component: () => import('pages/hashtags.vue'),
    name: 'hashtags',
    meta: {
      title: 'Хештеги'
    }
  },

  {
    path: '/posts',
    component: () => import('pages/posts.vue'),
    name: 'posts',
    meta: {
      title: 'Посты'
    }
  },

  // {
  //   path: '/:catchAll(.*)*',
  //   redirect: '/trips'
  // }
]

export default routes
