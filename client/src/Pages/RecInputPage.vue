<template>
  <div class="container">
    <h1>  in RecInputPage </h1>
    <b-form-file
      v-model="file1"
      :state="Boolean(file1)"
      placeholder="Choose a file or drop it here..."
      drop-placeholder="Drop file here..."
    ></b-form-file>
  </div>
</template>

<script>

export default {
  name: 'RecInputPage',
  data() {
    return {
      file1: null,
    };
  },
  methods: {
  },
};
</script>
