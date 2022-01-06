<template>
  <div class="container">
    <h1> Result Page </h1>
    <div class="table_div">
        <b-table striped hover :items="res" :fields="fields" id="results"
        :filter="confidenceFilter" :filter-function="filterTable">
          <template #cell(index)="data">
            {{ data.index + 1 }}
          </template>
        </b-table>
    </div>
    <br/>
    <br/>

    <b-form-input
      id="input-small"
      size="lg"
      v-model="confidenceFilter"
      placeholder="Please enter confidence level in order to filter the results:">
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
      fields: ['index', { key: 'Drug Name' }, { key: 'MIC' }, { key: 'MIC_Confidence' }, { key: 'Comments' }],
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
  },
};
</script>
