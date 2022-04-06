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
  FormRadioPlugin,
  FormTagsPlugin,
} from 'bootstrap-vue';
import Vuelidate from 'vuelidate';
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
  FormRadioPlugin,
  FormTagsPlugin,
].forEach((x) => Vue.use(x));
Vue.use(Vuelidate);

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
