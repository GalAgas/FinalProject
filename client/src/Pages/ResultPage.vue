<template>
  <div class="container">
    <h1> Results Page <b-icon icon="list-stars"></b-icon>
    </h1>
    <br/>
    <br/>
    <div class="table_div">
        <b-table striped hover :items="res" :fields="fields" id="results"
         :dark="true" :filter="confidenceFilter" :filter-function="filterTable">
          <template #cell(index)="data">
            {{ data.index + 1 }}
          </template>
          <!-- <template #cell(Details)="data">
            <a :href="`https://www.drugs.com/search.php?searchterm=${data.item.Drug_Name}`">More Details</a>
          </template> -->
          <template #cell(Drug_Name)="data">
            <a :href="`https://www.drugs.com/search.php?searchterm=${data.item.Drug_Name}`" target="_blank">{{ data.item.Drug_Name }}</a>
          </template>
        </b-table>
    </div>
    <br/>
    <div>
      <h4><b>* Click On Drug Name For More Information &nbsp;
        <b-icon icon="info-circle-fill" scale="2">
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
      res: null,
      confidenceFilter: '',
      fields: ['index', 'Drug_Name', { key: 'MIC' }, { key: 'MIC_Confidence' }, { key: 'Comments' }],
    };
  },
  created() {
    this.res = this.$route.params.res;
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
    // linkCreate(drugName) {
    //   console.log(drugName);
    //   const href = 'https://www.drugs.com/search.php?searchterm=';
    //   return href + drugName;
    // },
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
