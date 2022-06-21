<template>
  <div class="container">
    <h1> Results Page <b-icon icon="list-stars"></b-icon>
    </h1>
    <br/>
    <br/>
    <div class="table_div">
        <b-table striped hover :items="res" :fields="visibleFields" id="results"
         :dark="true" :filter="confidenceFilter" :filter-function="filterTable">
          <template #cell(index)="data">
            {{ data.index + 1 }}
          </template>
          <template #cell(Drug_Name)="data">
            <a id="linkToPopUp" @click="showPopUp(data.item.Drug_Name)">
            {{ data.item.Drug_Name }}
            </a>
          </template>
        </b-table>
        <b-modal
        ref='modalpopup'
        footer-bg-variant= 'light'
        header-bg-variant= 'dark'
        header-text-variant= 'light'
        body-bg-variant= 'light'
        :title="popupTitle" okOnly centered
        headerClass='p-2 border-bottom-0'
        footerClass='p-2 border-top-0'
        okVariant='success'
        buttonSize='md'>
          <p id='popupbody'>
          {{ message }}<a :href="link" target="_blank">Click For More Information</a></p></b-modal>
    </div>
    <div>
      <h4><b>* Click On Drug Name For Explainability &nbsp;
        <b-icon icon="file-earmark-code-fill" scale="2">
      </b-icon></b></h4>
    </div>
    <br/>
    <br/>
    <b-form-group id="confi" label="Confidence Level Filter: " label-for="confi"
      label-size="lg"
      label-cols-sm="4"
      label-cols-lg="3"
      content-cols-sm
      content-cols-lg="7">
      <b-form-input
        id="confibox"
        size="md"
        v-model="confidenceFilter"
        placeholder="Enter Number between 0 and 1">
      </b-form-input>
    </b-form-group>
  </div>
</template>

<script>

export default {
  name: 'ResultsPage',
  data() {
    return {
      popupTitle: '',
      link: '',
      message: '',
      res: null,
      pregnant: null,
      female: '',
      confidenceFilter: '',
      fields: [{ key: 'index', visable: true },
        { key: 'Drug_Name', visable: true },
        { key: 'MIC', visable: true },
        { key: 'MIC_Confidence', visable: true }],
    };
  },
  created() {
    this.res = this.$route.params.res;
    this.pregnant = this.$route.params.pregnant;
    this.female = this.$route.params.female === 'Female';
  },
  computed: {
    visibleFields() {
      return this.fields.filter((filed) => filed.visable);
    },
  },
  methods: {
    filterTable(row, filter) {
      if (filter === '') {
        return true;
      }
      if (row.MIC_Confidence < filter) {
        return false;
      }
      return true;
    },
    showPopUp(data) {
      const keysToshow = {
        Major_DDI: 4,
        Moderate_DDI: 5,
        Minor_DDI: 6,
        Coverage: 7,
      };
      let msg = '';
      Object.keys(this.res).forEach((idx) => {
        if (data === this.res[idx].Drug_Name) {
          Object.keys(keysToshow).forEach((field) => {
            const cleanField = field.replaceAll('_', ' ');
            msg = `${msg}${cleanField}: ${this.res[idx][field]}\n`;
          });
          if (this.female && this.pregnant === 'pregnant') {
            msg += `Pregnancy Category: ${this.res[idx].Pregnancy_Category}\n`;
          }
        }
      });
      this.message = msg;
      this.link = `https://www.drugs.com/search.php?searchterm=${data}`;
      this.popupTitle = `${data.charAt(0).toUpperCase()}${data.slice(1)} Infromation`;
      const mymodal = this.$refs.modalpopup;
      mymodal.show();
    },
  },
};
</script>

<style>
.container{
  zoom: 80%;
}

#confi{
  width: 100%;
  font-weight: bold;
  margin-left: 25%;
}
#confibox{
  width: 40%;
}
#linkToPopUp {
    cursor: pointer;
}
#popupbody {
  white-space: pre;
  text-align: center;
}
.modalclass {
  background: red;
}
</style>
