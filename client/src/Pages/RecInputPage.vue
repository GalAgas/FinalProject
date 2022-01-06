<template>
  <div>
    <h1> Recommendation Inputs Page </h1>
    <h1> Please enter patient ID & NGS csv file </h1>
    <b-form @submit.prevent="onRegister" @reset.prevent="onReset">
      <b-form-group>
        <b-form-input
          id="input-small1"
          size="lg"
          v-model="$v.form.PatientID.$model"
          :state="validateState('PatientID')"
          placeholder="Enter Patient ID">
        </b-form-input>
        <b-form-invalid-feedback v-if="!$v.form.PatientID.required">
          Patient ID is required.
        </b-form-invalid-feedback>
        <b-form-invalid-feedback v-if="!$v.form.PatientID.integer">
          Patient ID must contain only digits
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group>
        <b-form-file
        accept=".csv"
        v-model="csvFile"
        required
        :state="validateCSV"
        placeholder="Choose the require Gene Correlation file or drop it here..."
        drop-placeholder="Drop file here..."
        ></b-form-file>
        <b-form-invalid-feedback :state="validateCSV">
        Gene Correlation input must be a .csv file.
        </b-form-invalid-feedback>
      </b-form-group>
      <b-form-group>
        <b-form-file
        accept=".txt"
        v-model="txtFile"
        required
        :state="validateTXT"
        placeholder="Choose the require txt file or drop it here..."
        drop-placeholder="Drop file here..."
        ></b-form-file>
        <b-form-invalid-feedback :state="validateTXT">
        Contigs input must be a .txt file.
        </b-form-invalid-feedback>
      </b-form-group>
        <b-button
          size="lg"
          pill variant="info"
          v-on:click="handleClick">
          Submit
        </b-button>
    </b-form>
  </div>
  <!--div class="container">
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

  </div-->
</template>

<script>
import axios from 'axios';
import {
  required,
  integer,
} from 'vuelidate/lib/validators';

export default {
  name: 'RecInputPage',
  data() {
    return {
      form: {
        PatientID: null,
      },
      csvFile: null,
      txtFile: null,
      msg: '',
      popUp: '',
    };
    // return {
    //   csvFile: null,
    //   txtFile: null,
    //   PatientID: null,
    //   msg: '',
    //   popUp: '',
    // };
  },
  validations: {
    form: {
      PatientID: {
        required,
        integer,
      },
    },
  },
  computed: {
  //   validateID() {
  //     // if (this.PatientID) {
  //     //   // console.log(this.PatientID);
  //     //   const intRegex = /^\d+$/;
  //     //   console.log(intRegex.test(this.PatientID));
  //     //   // return Number(this.PatientID);
  //     //   // return Number.isNaN(this.PatientID);
  //     //   return intRegex.test(this.PatientID);
  //     // }
  //     // console.log(this.PatientID);
  //     const intRegex = /^\d+$/;
  //     // console.log(this.PatientID && intRegex.test(this.PatientID));
  //     // if (this.PatientID && intRegex.test(this.PatientID)) {
  //     if (this.PatientID == null || intRegex.test(this.PatientID)) {
  //       return true;
  //     }
  //     return false;
  //     // return this.PatientID && intRegex.test(this.PatientID);
  //   },
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
    validateState(param) {
      const { $dirty, $error } = this.$v.form[param];
      return $dirty ? !$error : null;
    },
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
          this.showPopUp(error.response.data);
        });
    },
    showPopUp(data) {
      this.popUp = '';
      this.$bvModal.msgBoxOk(data, {
        title: 'Error',
        size: 'xl',
        buttonSize: 'sm',
        okVariant: 'sucsses',
        headerClass: 'p-2 border-bottom-0',
        footerClass: 'p-2 border-top-0',
        centered: true,
      })
        .then((value) => {
          this.popUp = value;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
