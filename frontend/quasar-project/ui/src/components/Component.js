import { h } from 'vue'
import { QBadge } from 'quasar'

export default {
  name: 'home',

  setup () {
    return () => h(QBadge, {
      class: 'home',
      label: 'home'
    })
  }
}
