<!--
Todo: show a prettified and formated raw data json on this page.
-->
<template>
  <div v-if="enabled">
    <!--Your HTML here-->
  </div>
</template>

<script>
export default {
  name: "raw-data",
  data: () => {
    return {
      //Your data here.
    };
  },
  computed: {
    //Your computed properties here.
  },
  watch: {
    //Your watch properties here.
  },
  props: {
    //Your properties here.
    enabled: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    //Your methods here.
  },
};
</script>
