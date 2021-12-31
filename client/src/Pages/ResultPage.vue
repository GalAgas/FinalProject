<template>
  <div class="container">
    <h1> in Result Page </h1>
    <p>{{ this.res }}</p>
    <div class="table_div">
        <b-table striped hover :items="res"></b-table>
    </div>
  </div>
</template>

<script>

export default {
  name: 'ResultsPage',
  data() {
    return {
      res: [{ name: 'AB1', mic: '10mg', comment: 'lol1' }, { name: 'AB2', mic: '12mg', comment: 'lol2' }, { name: 'AB3', mic: '2mg', comment: 'lol3' }],
    };
  },
  created() {
    // this.res = this.$route.params.res;
    // console.log(this.res);
  },
  methods: {
  },
};
</script>
