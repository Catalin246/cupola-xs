import { boot } from 'quasar/wrappers'
import VuePlugin from 'quasar-ui-cupola'

export default boot(({ app }) => {
  app.use(VuePlugin)
})
