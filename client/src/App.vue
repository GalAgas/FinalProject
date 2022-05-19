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
  overflow-y: hidden;
  overflow-x: hidden;
}

#app:before {
  content: '';
  display: block;
  height: 140%;
  width: 100%;
  position: absolute;
  background-repeat: no-repeat;
  background-size: cover;
  background-image: url('./assets/background.jpg');
  background-attachment: fixed;
  opacity: 0.4;
  z-index: -1;
}

#innerDiv{
  margin-top:5%;
  height: 100%;
  width: 100%;
}
</style>
