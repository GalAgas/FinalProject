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
            :disabled="nextButtonDisabled"
            class="ml-5w-75"
            v-on:click="handleNext">
            Next
          </b-button>
      </b-form>
      <b-form id="inputform" v-if="!step1">
        <b-form-group>
          <b-form-select
            id="age"
            v-model="$v.Inputs.ageSelected.$model"
            :options="Inputs.ageOptions"
            :state="validatePatientState('ageSelected')"
            size="sm">
           </b-form-select>
        </b-form-group>
          <b-form-radio-group
            v-model="Inputs.genderSelected"
            :options="Inputs.genderOptions"
            name="Gender"
          ></b-form-radio-group>
        <div class="mt-2">Creatinine Level: {{ Inputs.creatinine }}</div>
        <b-form-input
          v-model="Inputs.creatinine"
          type="range"
          min="0" max="3" step="0.1"></b-form-input>
        <b-form-checkbox
          v-model="Inputs.fever"
          switch>
          Fever
        </b-form-checkbox>
        <b-form-checkbox
          v-model="Inputs.flankPain"
          switch>
          Flank Pain
        </b-form-checkbox>
        <b-form-checkbox
          v-model="Inputs.Dysuria"
          switch>
          Dysuria
        </b-form-checkbox>
        <div>
        <b-form-group label="More Drugs of Patient" label-for="tags-with-dropdown">
          <b-form-tags
            id="tags-with-dropdown"
            v-model="drugsValue">
            <template v-slot="{ tags, disabled, removeTag, addTag }">
              <ul v-if="tags.length > 0" class="list-inline d-inline-block">
                <li v-for="tag in tags" :key="tag" class="list-inline-item">
                  <b-form-tag
                    @remove="removeTag(tag)"
                    :title="tag"
                    :disabled="disabled"
                    variant="info"
                  >{{ tag }}</b-form-tag>
                </li>
              </ul>
              <b-dropdown size="sm" variant="outline-secondary" block menu-class="w-100">
                <template #button-content>
                  <b-icon icon="tag-fill"></b-icon> Choose Patient Drugs
                </template>
                <b-dropdown-form @submit.stop.prevent="() => {}">
                  <b-form-group
                    label="Search tags"
                    label-for="tag-search-input"
                    label-cols-md="auto"
                    class="mb-0"
                    label-size="sm"
                    :description="searchDesc"
                    :disabled="disabled"
                  >
                    <b-form-input
                      v-model="Inputs.drugsSearch"
                      id="tag-search-input"
                      type="search"
                      size="lg"
                      autocomplete="off"
                    ></b-form-input>
                  </b-form-group>
                </b-dropdown-form>
                <b-dropdown-divider></b-dropdown-divider>
                <b-dropdown-item-button
                  v-for="option in availableOptions"
                  :key="option"
                  @click="onDrugsOptionClick({ option, addTag })"
                >
                  {{ option }}
                </b-dropdown-item-button>
                <b-dropdown-text v-if="availableOptions.length === 0">
                  There are no tags available to select
                </b-dropdown-text>
              </b-dropdown>
            </template>
          </b-form-tags>
        </b-form-group>
        </div>
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
          :disabled="submitButtonDisabled"
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
      csvFile: null,
      txtFile: null,
      msg: '',
      popUp: '',
      step1: true,
      txtFileName: 'Choose the require txt file or drop it here...',
      csvFileName: 'Choose the require Gene Correlation file or drop it here...',
      Inputs: {
        ageSelected: '',
        ageOptions: [
          { value: '', text: 'Select patient age' },
          { value: '0-5', text: '0-5' },
          { value: '6-17', text: '6-17' },
          { value: '18-39', text: '18-39' },
          { value: '40-59', text: '40-59' },
          { value: '60-79', text: '60-79' },
          { value: '80+', text: '80+' },
        ],
        genderSelected: '',
        genderOptions: [
          { text: 'Male', value: 'Male' },
          { text: 'Female', value: 'Female' },
        ],
        drugsOptions: ['A', 'AB', 'B', 'C', 'CB'],
        drugsSearch: '',
        creatinine: '1.5',
        fever: false,
        flankPain: false,
        Dysuria: false,
      },
      drugsValue: [],
    };
  },
  validations: {
    form: {
      PatientID: {
        required,
        integer,
      },
    },
    Inputs: {
      ageSelected: {
        required,
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
    nextButtonDisabled() {
      if (this.form.PatientID === '' || this.csvFile == null || this.txtFile == null || !this.validateTXT || !this.validateCSV || !this.validateState('PatientID')) {
        return true;
      }
      return false;
    },
    submitButtonDisabled() {
      return this.Inputs.genderSelected === '' || this.Inputs.ageSelected === '';
    },
    criteria() {
      // Compute the search criteria
      return this.Inputs.drugsSearch.trim().toLowerCase();
    },
    availableOptions() {
      // Filter out already selected options
      const options = this.Inputs.drugsOptions.filter((opt) => this.drugsValue.indexOf(opt) === -1);
      if (this.criteria) {
        // Show only options that match criteria
        return options.filter((opt) => opt.toLowerCase().indexOf(this.criteria) > -1);
      }
      // Show all options available
      return options;
    },
    searchDesc() {
      if (this.criteria && this.availableOptions.length === 0) {
        return 'There are no tags matching your search criteria';
      }
      return '';
    },
  },
  watch: {
    txtFile(newval) {
      if (this.txtFile) {
        this.txtFileName = newval.name;
      } else {
        this.txtFileName = 'Choose the require txt file or drop it here...';
      }
    },
    csvFile(newval) {
      if (this.csvFile) {
        this.csvFileName = newval.name;
      } else {
        this.csvFileName = 'Choose the require Gene Correlation file or drop it here...';
      }
    },
  },
  methods: {
    validateState(param) {
      const { $dirty, $error } = this.$v.form[param];
      return $dirty ? !$error : null;
    },
    validatePatientState(param) {
      const { $dirty, $error } = this.$v.Inputs[param];
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
      bodyFormData.append('id', this.form.PatientID);
      bodyFormData.append('gene_correlation_csv', this.csvFile);
      bodyFormData.append('gene_correlation_txt', this.txtFile);
      bodyFormData.append('patientAge', this.Inputs.ageSelected);
      bodyFormData.append('patientGender', this.Inputs.genderSelected);
      bodyFormData.append('patientCreatinine', this.Inputs.creatinine);
      bodyFormData.append('patientFever', this.Inputs.fever);
      bodyFormData.append('patientFlankPain', this.Inputs.flankPain);
      bodyFormData.append('patientDysuria', this.Inputs.Dysuria);
      bodyFormData.append('patientDrugsInUse', this.drugsValue);
      const config = {
        headers: { 'content-type': 'multipart/form-data' },
      };
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
    onDrugsOptionClick({ option, addTag }) {
      addTag(option);
      this.Inputs.drugsSearch = '';
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

#inputform{
  width: 80%;
  padding-left: 20%;
}

#age{
  width: 50%;
}

</style>
