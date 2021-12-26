import Vue from 'vue';
import Router from 'vue-router';
import Ping from '../components/Ping.vue';
import HomePage from '../Pages/HomePage.vue';
import AboutUsPage from '../Pages/AboutUsPage.vue';
import NotFoundPage from '../Pages/NotFoundPage.vue';
import RecInputPage from '../Pages/RecInputPage.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/AboutUs',
      name: 'AboutUsPage',
      component: AboutUsPage,
    },
    {
      path: '/RecInput',
      name: 'RecInputPage',
      component: RecInputPage,
    },
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '*',
      name: 'NotFoundPage',
      component: NotFoundPage,
    },
  ],
});
