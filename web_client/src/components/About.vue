<template>
  <div v-show="enabled" class="fill-height">
    <v-container fluid class="fill-height">
      <v-row style="height: 50%"
        ><v-col v-for="author in authors" v-bind:key="author.qq" style="width: 33%">
          <v-card
            class="fill-height rounded-lg pa-3"
            elevation="2"
            color="blue-grey lighten-5"
          >
            <v-card-title class="headline font-weight-bold text-no-wrap">
              <v-avatar color="primary" size="80" Left
                ><img v-bind:src="'http://q1.qlogo.cn/g?b=qq&nk=' + author.qq + '&s=640'"
              /></v-avatar>
              <div color="blue-grey darken-4" class="ml-5">
                {{ author.nickname }}
              </div>
            </v-card-title>
            <div class="text-center">
              {{ author.work }}
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-row style="height: 50%">
        <v-col style="width: 33%">
          <v-card
            class="fill-height rounded-lg pa-3"
            elevation="2"
            color="blue-grey lighten-5"
          >
            <v-card-title class="headline font-weight-bold">
              <v-avatar color="primary" size="80" Left
                ><span class="white--text headline">SI100B</span></v-avatar
              >
              <div color="blue-grey darken-4" class="ml-5">
                All SI100B staff
              </div>
            </v-card-title>
            <div class="text-center">Provide us a chance to create this project.</div>
          </v-card>
        </v-col>
        <v-col style="width: 33%">
          <v-card
            class="fill-height rounded-lg pa-3"
            elevation="2"
            color="blue-grey lighten-5"
          >
            <v-card-title class="headline font-weight-bold">
              <v-avatar color="white" size="80" Left
                ><img src="https://cn.vuejs.org/images/logo.png"
              /></v-avatar>
              <div color="blue-grey darken-4" class="text-no-wrap ml-5">Vue.js</div>
            </v-card-title>
            <div class="text-center">Help us build up this website.</div>
          </v-card>
        </v-col>
        <v-col style="width: 33%">
          <v-card
            class="fill-height rounded-lg pa-3"
            elevation="2"
            color="blue-grey lighten-5"
          >
            <v-card-title class="headline font-weight-bold">
              <v-avatar color="white" size="80" Left
                ><img
                  src="https://cdn.vuetifyjs.com/docs/images/logos/vuetify-logo-light-atom.svg"
              /></v-avatar>
              <div color="blue-grey darken-4" class="text-no-wrap ml-5">Vuetify</div>
            </v-card-title>
            <div class="text-center">Provide fancy UI components for this website.</div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";
let self;
export default {
  name: "about",
  data: () => {
    return {
      authors: [
        {
          qq: "953551078",
          work: "Responsible for data retrieving/formating/cleaning.",
          nickname: "",
        },
        { qq: "2364261262", work: "Responsible for backend.", nickname: "" },
        {
          qq: "2654791554",
          work: "Responsible for frontend+data visualization.",
          nickname: "",
        },
      ],
    };
  },
  props: {
    enabled: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    getNickname(author) {
      axios({
        method: "post",
        url: "/proxy/",
        "content-type": "application/json",
        data: JSON.stringify({
          _url: "https://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg",
          _method: "GET",
          uins: author.qq,
        }),
      })
        .then((response) => {
          console.log(response);
          /,"([^"]+)",/.test(response.data);
          author.nickname = RegExp.$1;
        })
        .catch((error) => {
          console.error(error);
        });
      return false; //For calling convenient
    },
  },
  created: function () {
    //This must not be arrow function, or "this" would be undefined.
    self = this;
  },
  mounted() {
    
    self.$data.authors.forEach(self.$options.methods.getNickname);
  },
};
</script>
