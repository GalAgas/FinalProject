<template>
  <div class="container">
    <h1> Recommendation Inputs Page </h1>
    <h1> Please enter patient ID & NGS csv file </h1>

    <b-form-input
      id="input-small"
      size="lg"
      v-model="PatientID"
      :state="validateID"
      placeholder="Enter Patient ID">
    </b-form-input>
    <br/>

    <b-form-invalid-feedback :state="validateID">
      Patient ID must be a number.
    </b-form-invalid-feedback>

    <br/>
    <br/>

    <b-form-file
      accept=".csv"
      v-model="csvFile"
      required
      :state="validateCSV"
      placeholder="Choose the require Gene Correlation file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>

    <br/>

    <b-form-invalid-feedback :state="validateCSV">
      Gene Correlation input must be a .csv file.
    </b-form-invalid-feedback>

    <br/>
    <b-form-file
      accept=".txt"
      v-model="txtFile"
      :state="validateTXT"
      placeholder="Choose the require txt file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>
    <br/>

    <b-form-invalid-feedback :state="validateTXT">
      Contigs input must be a .txt file.
    </b-form-invalid-feedback>

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
      csvFile: null,
      txtFile: null,
      PatientID: null,
      msg: '',
    };
  },
  computed: {
    validateID() {
      // if (this.PatientID) {
      //   // console.log(this.PatientID);
      //   const intRegex = /^\d+$/;
      //   console.log(intRegex.test(this.PatientID));
      //   // return Number(this.PatientID);
      //   // return Number.isNaN(this.PatientID);
      //   return intRegex.test(this.PatientID);
      // }
      // console.log(this.PatientID);
      const intRegex = /^\d+$/;
      // console.log(this.PatientID && intRegex.test(this.PatientID));
      if (this.PatientID && intRegex.test(this.PatientID)) {
        return true;
      }
      return false;
      // return this.PatientID && intRegex.test(this.PatientID);
    },
    validateCSV() {
      // if (this.csvFile) {
      //   console.log(this.csvFile.type);
      //   console.log(this.csvFile.name);
      // }
      return this.csvFile && this.csvFile.type.endsWith('.ms-excel');
    },
    validateTXT() {
      // if (this.txtFile) {
      //   console.log(this.txtFile.type);
      //   console.log(this.txtFile.name);
      // }
      return this.txtFile && this.txtFile.type.startsWith('text/');
    },
  },
  methods: {
    handleClick() {
      const bodyFormData = new FormData();
      bodyFormData.append('id', this.PatientID);
      bodyFormData.append('gene_correlation_csv', this.csvFile);
      bodyFormData.append('gene_correlation_txt', this.txtFile);
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
          console.log(error.response.data);
        });
    },
  },
};
</script>
