import Vue from 'vue'

//Register components
//import Visualization from './components/Visualization.vue';

import App from './App'
import vuetify from './plugins/vuetify';
Vue.config.productionTip = false
new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
