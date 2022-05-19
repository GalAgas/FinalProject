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
            <a :href="`https://www.drugs.com/search.php?searchterm=${data.item.Drug_Name}`" target="_blank">
            {{ data.index + 1 }}
            </a>
          </template>
          <!-- <template #cell(Drug_Name)="data">
            <a :href="`https://www.drugs.com/search.php?searchterm=${data.item.Drug_Name}`" target="_blank">{{ data.item.Drug_Name }}</a>
          </template> -->
          <template #cell(Drug_Name)="data">
            <a id="linkToPopUp" @click="showPopUp(data.item.Drug_Name)">
            {{ data.item.Drug_Name }}
            </a>
          </template>
        </b-table>
    </div>
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
      show: false,
      popUp: '',
      res: null,
      pregnant: null,
      female: '',
      confidenceFilter: '',
      fields: [{ key: 'index', visable: true },
        { key: 'Drug_Name', visable: true },
        { key: 'MIC', visable: true },
        { key: 'MIC_Confidence', visable: true }],
      // { key: 'Major_DDI', visable: false },
      // { key: 'Moderate_DDI', visable: false },
      // { key: 'Minor_DDI', visable: false },
      // { key: 'Coverage', visable: false },
      // { key: 'Pregnancy_Category', visable: false }],
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
      this.popUp = '';
      let msg = '';
      Object.keys(this.res).forEach((idx) => {
        if (data === this.res[idx].Drug_Name) {
          Object.keys(keysToshow).forEach((field) => {
            const cleanField = field.replaceAll('_', ' ');
            msg = `${msg}${cleanField}: ${this.res[idx][field]}\n`;
          });
          if (this.female && this.pregnant === 'pregnant') {
            msg += `Pregnancy Category: ${this.res[idx].Pregnancy_Category}`;
          }
        }
      });
      // const container = document.getElementById('modal1');
      // console.log(container);
      // const t = document.createElement('b-modal');
      // // console.log(u);
      // // const t = document.getElementById('outer');
      // t.model = this.show;
      // const con = document.createElement('b-container');
      // t.appendChild(con);
      // const p = document.createElement('p');
      // const a = document.createElement('a');
      // p.innerText = msg;
      // con.appendChild(p);
      // a.href = `https://www.drugs.com/search.php?searchterm=${data}`;
      // a.text = 'click here';
      // a.target = '_blank';
      // con.appendChild(a);
      // // document.getElementById('outer').appendChild(t);
      // this.show = true;
      // const p = this.$createElement('p');
      // p.text = msg;
      // const a = 'click me';
      // const r = a.link(`https://www.drugs.com/search.php?searchterm=${data}`);
      // console.log(p);
      this.$bvModal.msgBoxOk([msg], {
        id: 'pop',
        title: [`${data} information`],
        size: 'md',
        buttonSize: 'sm',
        okVariant: 'info',
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
#pop {
  white-space: pre;
  text-align: center;
}
</style>
