import { boot } from 'quasar/wrappers'

export default boot(({ app, store }) => {
  store.dispatch('init')

  const requireComponent = require.context(
    './../controllers',
    true,
    /\w+\.vue$/
  )

  requireComponent.keys().forEach((file_name) => {
    const component_config = requireComponent(file_name)
    const component_name = file_name
      .split('/')
      .pop()
      .replace(/\.\w+$/, '')
      .replace('_', '-')
    app.component('app-' + component_name, component_config.default)
  })
})
