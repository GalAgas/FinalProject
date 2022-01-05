import Vue from 'vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import {
  FormGroupPlugin,
  FormPlugin,
  FormInputPlugin,
  ButtonPlugin,
  CardPlugin,
  NavbarPlugin,
  FormSelectPlugin,
  AlertPlugin,
  ToastPlugin,
  LayoutPlugin,
  InputGroupPlugin,
  TablePlugin,
  FormCheckboxPlugin,
  IconsPlugin,
  FormFilePlugin,
  ModalPlugin,
}
from 'bootstrap-vue';
import App from './App.vue';
import router from './router';

[
  FormGroupPlugin,
  FormPlugin,
  FormInputPlugin,
  ButtonPlugin,
  CardPlugin,
  NavbarPlugin,
  FormSelectPlugin,
  AlertPlugin,
  ToastPlugin,
  LayoutPlugin,
  InputGroupPlugin,
  TablePlugin,
  FormCheckboxPlugin,
  IconsPlugin,
  FormFilePlugin,
  ModalPlugin,
].forEach((x) => Vue.use(x));

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
