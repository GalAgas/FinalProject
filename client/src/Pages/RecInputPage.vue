<template>
  <div class="container">
    <h1>  in RecInputPage </h1>
    <b-form-input
    id="input-small"
    size="lg"
    v-model="PatientID"
    placeholder="Enter Patient ID">
    </b-form-input>
    <br/>
    <b-form-file
      v-model="file1"
      :state="Boolean(file1)"
      placeholder="Choose a file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>
    <br/>
    <b-button
    size="lg"
    pill variant="info"
    v-on:click="handleClick">
    Large Button
    </b-button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RecInputPage',
  data() {
    return {
      file1: null,
      PatientID: '',
      msg:'',
    };
  },
  methods: {
    handleClick() {
      var bodyFormData = new FormData();
      bodyFormData.append('id',this.PatientID);
      bodyFormData.append('ngs_file',this.file1);
      const config = {
        headers: { 'content-type': 'multipart/form-data' }
    }
      console.log('in handle click');
      const path = 'http://localhost:5000/check';
      axios.post(path,bodyFormData,config)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
