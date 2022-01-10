import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '../Pages/HomePage.vue';
import AboutUsPage from '../Pages/AboutUsPage.vue';
import NotFoundPage from '../Pages/NotFoundPage.vue';
import RecInputPage from '../Pages/RecInputPage.vue';
import ResultPage from '../Pages/ResultPage.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
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
      path: '/ResultPage',
      name: 'ResultPage',
      component: ResultPage,
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
