<template>
  <div class="container">
    <h1><B>About Page</B></h1>
    <p id="parProject">
      Single Page web application with client-server architecture.<br>
      Based on REST API - using Swagger, Server Side – Flask framework, Client Side – Vue.js.<br>
      Includes End to end automated DEMO pipeline development<br>
      (algorithmoc modules still in research)  easy to use GUI.
    <p>
    <h1><B>About Us</B></h1>
    <br>
    <div class="aboutPage">
    <div>
      <b-card
        title="Gal Agasi"
        img-src="https://picsum.photos/600/300/?image=25"
        img-alt="Image"
        img-top
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Project Manager
        </b-card-text>
        <b-button href="#" variant="primary">Go To My Linkedin</b-button>
      </b-card>
    </div>
    <div>
      <b-card
        title="Guy Zaidman"
        img-src="https://picsum.photos/600/300/?image=25"
        img-alt="Image"
        img-top
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          The Future Husband of the Project Manager
        </b-card-text>
        <b-button href="#" variant="primary">Go To My Linkedin</b-button>
      </b-card>
            <b-card
        title="Tomer Kelner"
        img-src="https://picsum.photos/600/300/?image=25"
        img-alt="Image"
        img-top
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Backend Developer
        </b-card-text>
        <b-button href="https://www.linkedin.com/in/tomer-kelner-819938210/" variant="primary">Go To My Linkedin</b-button>
      </b-card>
            <b-card
        title="Tomer Varon"
        img-src="https://picsum.photos/600/300/?image=25"
        img-alt="Image"
        img-top
        tag="article"
        class="mb-2"
      >
        <b-card-text>
          Frontend Developer and excellent in Vue
        </b-card-text>
        <b-button href="https://www.linkedin.com/in/tomer-varon-a9b79722a/" variant="primary">Go To My Linkedin</b-button>
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
