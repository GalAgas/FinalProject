<template>
  <div>
    <h1> <B>Recommendation Inputs Page</B> </h1>
    <div class="formDiv">
      <b-form v-if="step1">
        <h2> <B>Please enter patient ID & NGS csv file :</B> </h2>
        <b-form-group>
          <b-form-input
            id="input-small"
            size="lg"
            v-model="$v.form.PatientID.$model"
            :state="validateState('PatientID')"
            placeholder="Enter Patient ID">
          </b-form-input>
          <b-form-invalid-feedback v-if="!$v.form.PatientID.integer">
            Patient ID must contain only digits
          </b-form-invalid-feedback>
        </b-form-group>
        <b-form-group>
          <b-form-file
          accept=".csv"
          v-model="csvFile"
          :state="validateCSV"
          :placeholder="csvFileName"
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
          :state="validateTXT"
          :placeholder="txtFileName"
          drop-placeholder="Drop file here..."
          ></b-form-file>
          <b-form-invalid-feedback :state="validateTXT">
          Contigs input must be a .txt file.
          </b-form-invalid-feedback>
        </b-form-group>
          <b-button
            size="lg"
            pill variant="info"
            :disabled="buttonDisabled"
            class="ml-5w-75"
            v-on:click="handleNext">
            Next
          </b-button>
          <!--b-button
            size="lg"
            pill variant="info"
            :disabled="buttonDisabled"
            class="ml-5w-75"
            v-on:click="handleSubmit">
            Submit
          </b-button-->
      </b-form>
      <b-form v-if="!step1">
        <b-button
          size="lg"
          pill variant="info"
          class="ml-5w-75"
          v-on:click="handleBack">
          Back
        </b-button>
        <b-button
          size="lg"
          pill variant="info"
          :disabled="buttonDisabled"
          class="ml-5w-75"
          v-on:click="handleSubmit">
          Submit
        </b-button>
      </b-form>
    </div>
  </div>
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
        PatientID: '',
      },
      forminputs: {
        age: '',
      },
      csvFile: null,
      txtFile: null,
      msg: '',
      popUp: '',
      step1: true,
      txtFileName: 'Choose the require txt file or drop it here...',
      csvFileName: 'Choose the require Gene Correlation file or drop it here...',

    };
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
    validateCSV() {
      return this.csvFile && this.csvFile.type.endsWith('.ms-excel');
    },
    validateTXT() {
      return this.txtFile && this.txtFile.type.startsWith('text/');
    },
    buttonDisabled() {
      if (this.form.PatientID === '' || this.csvFile == null || this.txtFile == null || !this.validateTXT || !this.validateCSV || !this.validateState('PatientID')) {
        return true;
      }
      return false;
    },
  },
  watch: {
    txtFile(newval) {
      this.txtFileName = newval.name;
    },
    csvFile(newval) {
      this.csvFileName = newval.name;
    },
  },
  methods: {
    validateState(param) {
      const { $dirty, $error } = this.$v.form[param];
      return $dirty ? !$error : null;
    },
    handleNext() {
      this.step1 = false;
      
    },
    handleBack() {
      this.step1 = true;
    },
    handleSubmit() {
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
        size: 'md',
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

<style>
.formDiv{
  width: 75%;
  padding-top: 5%;
  padding-left: 25%;
}

.ml-5w-75 {
  margin-top: 3%;
  width: 20%;
  background-color: #454545!important;
  border-color: #000000!important;
}
</style>
