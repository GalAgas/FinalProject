<template>
  <div class="container">
    <h1><B> GPS</B></h1>
    <h1><B> Antibiotic Treatment Recommendation System</B> </h1>
    <br>
    <br>
    <br>
    <br>
    <b-button variant="primary" :to="{ name: 'RecInputPage'}" class="ReccBtn" id="btn">
    Start Recommendation Process </b-button>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
    };
  },
  methods: {
  },
};
</script>

<style>
.ReccBtn {
  box-shadow: inset 0px 1px 0px 0px #42b983;
  background: #454545!important;;
  background-color: #42b983;
  border-radius: 10px;
  border: 2px solid #454545;
  display: inline-block;
  cursor: pointer;
  color: #ffffff;
  font-family: "Exo";
  font-size: 20px;
  font-weight: bold;
  padding: 10px 25px;
  text-decoration: none;
  text-shadow: 0px 1px 0px #269146;
  display: block;
  margin-top: 2%;
  width: 35%;
  margin-left: 35%;
}
.ReccBtn:hover {
  background: linear-gradient(to bottom, #2ca55a 5%, #339b6f 100%);
  background-color: #42b983;
}
.searchBtn:active {
  position: relative;
  top: 1px;
}
#btn {
  transition: all 0.1s ease;
}
#btn:hover {
  transform: scale(1.2);
}
</style>
