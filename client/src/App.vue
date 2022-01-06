<template>
  <div id="app">
    <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css?family=Abril Fatface|Exo"/>
    <NavBar/>
    <div id="innerDiv">
      <router-view/>
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  name: 'App',
  components: {
    NavBar,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-family: "Exo";
  font-weight: bold;
}

#app:before {
  content: ' ';
  display: block;
  width: 100%;
  height: 100%;
  position: absolute;
  background-repeat: no-repeat;
  background-size: cover;
  background-image: url('./assets/background.jpg');
  opacity: 0.4;
  z-index: -1;
}

#innerDiv{
  margin-top:5%;
}
</style>
