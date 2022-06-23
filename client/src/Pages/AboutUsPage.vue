<template>
  <div class="container">
    <h1><B>About Page</B></h1>
    <p id="parProject">
      A Rules-Based recommendation system for antibiotic treatment.<br>
      The system uses elimination and ranking factors like:<br>
      AMR, kidney Function, DDI, Range coverage & pregnancy category.<br>
      Includes End to end automated pipeline relying on patient and bacterial properties.<br>
      Single Page web application with client-server architecture.<br>
      Based on REST API - using Swagger, Server Side – Flask framework, Client Side – Vue.js.<br>
    <p>
    <div class="aboutPage">
    <div>

      <b-card
        bg-variant="dark"
        text-variant="white"
        title="Gal Agasi"
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Project Manager
          <b-icon icon="person-circle" animation="throb" font-scale="1"></b-icon>
        </b-card-text>
        <b-button href="https://www.linkedin.com/in/gal-agasi-188284207/" variant="primary" target="_blank">Go To My Linkedin</b-button>
      </b-card>
    </div>
    <div>
      <b-card
        bg-variant="dark"
        text-variant="white"
        title="Guy Zaidman"
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Analysis & Design, QA
          <b-icon icon="person-circle" animation="throb" font-scale="1"></b-icon>
        </b-card-text>
        <b-button href="https://www.linkedin.com/in/guy-zaidman-51bb43154/" variant="primary" target="_blank">Go To My Linkedin</b-button>
      </b-card>
        <b-card
        bg-variant="dark"
        text-variant="white"
        title="Tomer Kelner"
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Backend Developer
          <b-icon icon="person-circle" animation="throb" font-scale="1"></b-icon>
        </b-card-text>
        <b-button href="https://www.linkedin.com/in/tomer-kelner-819938210/" variant="primary" target="_blank">Go To My Linkedin</b-button>
      </b-card>
      <b-card
        bg-variant="dark"
        text-variant="white"
        title="Tomer Varon"
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Frontend Developer
          <b-icon icon="person-circle" animation="throb" font-scale="1"></b-icon>
        </b-card-text>
        <b-button href="https://www.linkedin.com/in/tomer-varon-a9b79722a/" variant="primary" target="_blank">Go To My Linkedin</b-button>
      </b-card>
    </div>
  </div>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  name: 'AboutUsPage',
  data() {
    return {
    };
  },
  methods: {
  },
};
</script>

<style>
#parProject{
  margin-top:2%;
  font-size: 24px;
  margin-bottom: 7%;
}

.aboutPage{
  width:100%;
  padding-left: 8%;
  position: absolute;
  left: 0;
}
.mb-2{
  float: left;
  width: 20%;
  margin-right: 3%;
}
</style>
