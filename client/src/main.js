import Vue from 'vue'
import App from './App.vue'

import './assets/styles/index.css';
import router from './router'

Vue.config.productionTip = false

import { library } from '@fortawesome/fontawesome-svg-core';
import { faBookmark, faBuilding, faCalendar, faEye, faFilePdf, faFlag, faSave, faTrashAlt } from '@fortawesome/free-regular-svg-icons';
import { faBook, faPlus, faSyncAlt, faTags, faTrashRestoreAlt, faUserGraduate } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faFilePdf, faBuilding, faUserGraduate, faTags, faBookmark, faFlag, faCalendar, faBook, faEye, faPlus, faSave, faTrashAlt, faTrashRestoreAlt, faSyncAlt);

Vue.component('font-awesome-icon', FontAwesomeIcon);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
