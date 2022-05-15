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
            <a :href="`https://www.drugs.com/search.php?searchterm=${data.item.Drug_Name}`" target="_blank">{{ data.item.Drug_Name }}</a>
          </template>
        </b-table>
    </div>
    <div>
      <h4><b>* Click On Drug Name For More Information &nbsp;
        <b-icon icon="info-circle-fill" scale="2">
      </b-icon></b></h4>
    </div>
    <b-button
      id="expandBtn"
      size="lg"
      pill variant="info"
      class="ml-5w-75"
      v-on:click="changeFields">
      {{ expend_button_text }}
    </b-button>
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
      res: null,
      confidenceFilter: '',
      fields: [{ key: 'index', visable: true },
        { key: 'Drug_Name', visable: true },
        { key: 'MIC', visable: true },
        { key: 'MIC_Confidence', visable: true },
        { key: 'Coverage', visable: false },
        { key: 'Comments', visable: true }],
      expend_button_text: 'Expend View',
    };
  },
  created() {
    this.res = this.$route.params.res;
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
    changeFields() {
      const keysToChange = { Coverage: 4 };
      Object.keys(keysToChange).forEach((field) => {
        if (this.fields[keysToChange[field]].visable) {
          this.fields[keysToChange[field]].visable = false;
          this.expend_button_text = 'Expend View';
        } else {
          this.fields[keysToChange[field]].visable = true;
          this.expend_button_text = 'Hidden View';
        }
      });
    },
  },
};
</script>

<style>
#confi{
  width: 100%;
  font-weight: bold;
  margin-left: 25%;
}
#confibox{
  width: 40%;
}
</style>
