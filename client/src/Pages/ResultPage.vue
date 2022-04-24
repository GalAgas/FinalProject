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
          <!-- <template #cell(Drug Name)="data">
            <a href="#" @click='linkCreate(data.items.Drug_Name)'>{{ data.items.Drug_Name+'t' }}</a>
          </template> -->
        </b-table>
    </div>
    <br/>
    <br/>

    <b-form-input
      class="mx-auto"
      id="confi"
      size="lg"
      v-model="confidenceFilter"
      placeholder="Confidence Level Filter:">
    </b-form-input>

  </div>
</template>

<script>

export default {
  name: 'ResultsPage',
  data() {
    return {
      res: null,
      confidenceFilter: '',
      fields: ['index', { key: 'Drug_Name' }, { key: 'MIC' }, { key: 'MIC_Confidence' }, { key: 'Comments' }],
      // fields: ['index', 'Drug_Name', { key: 'MIC' }, { key: 'MIC_Confidence' },
      // { key: 'Comments' }],
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
  width: 30%;
  font-weight: bold;
}
</style>
