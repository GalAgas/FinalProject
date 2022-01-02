<template>
  <div class="container">
    <h1> Result Page </h1>
    <div class="table_div">
        <b-table striped hover :items="res" :fields="fields">
          <template #cell(index)="data">
            {{ data.index + 1 }}
          </template>
        </b-table>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ResultsPage',
  data() {
    return {
      res: null,
      fields: ['index', { key: 'Drug Name' }, { key: 'MIC' }, { key: 'Rank' }, { key: 'Comments' }],
    };
  },
  created() {
    this.res = this.$route.params.res;
  },
  methods: {
  },
};
</script>
