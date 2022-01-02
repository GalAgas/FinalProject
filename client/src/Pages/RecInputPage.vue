<template>
  <div class="container">
    <h1> Recommendation Inputs Page </h1>
    <h1> Please enter patient ID & NGS csv file </h1>
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
    Submit
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
      msg: '',
    };
  },
  methods: {
    handleClick() {
      const bodyFormData = new FormData();
      bodyFormData.append('id', this.PatientID);
      bodyFormData.append('gene_correlation_file', this.file1);
      const config = {
        headers: { 'content-type': 'multipart/form-data' },
      };
      // console.log('in handle click');
      const path = 'http://localhost:5000/generate';
      axios.post(path, bodyFormData, config)
        .then((res) => {
          this.msg = res.data;
          this.$router.push({ name: 'ResultPage', params: { res: res.data } });
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
};
</script>
