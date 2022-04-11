<template>
  <v-app>
    <link href="https://fonts.font.im/css?family=Do+Hyeon" rel="stylesheet" />
    <v-navigation-drawer app>
      <v-list dense nav>
        <v-list-item
          id="item.title"
          v-for="item in items"
          :key="item.title"
          v-on:click="navigate(item.target)"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="indigo darken-1" id="head_line">
      <v-img src="./assets/logo.svg" id="logo" max-width="1.5em"></v-img>
      {{ head_line }}
    </v-app-bar>
    <v-main>
      <config v-bind:enabled="page == 'Config'" @overlay="overlay" />
      <visualization v-bind:enabled="page == 'Visualization'" @overlay="overlay" />
      <about v-bind:enabled="page == 'About'" />
      <!-- Map must be placed on the last layer... 
       This is due to some fancy bugs of the mapbox -->
      <map-selector v-bind:enabled="page == 'Map'" />
      <v-fade-transition>
        <v-overlay v-show="loading" z-index="0" absolute="absolute">
          <v-progress-circular indeterminate size="64"></v-progress-circular>
        </v-overlay>
      </v-fade-transition>
    </v-main>
    <!--
    <v-footer app>
      Copyright ©2020-{{ year }} SI100B GG Team, All Rights Reserved.
    </v-footer> -->
  </v-app>
</template>

<style scoped>
#head_line {
  font-family: "Do Hyeon", sans-serif;
  font-size: 2em;
  text-align: center;
  color: #e8eaf6;
}
#logo {
  margin: 0.3em;
}
</style>

<script>
import Config from "./components/Config";
import MapSelector from "./components/MapSelector";
import Visualization from "./components/Visualization";
import About from "./components/About";
// Sometimes there's a conflict in names, so don't use 'Map' as a variable name!

export default {
  name: "App",
  components: {
    Config,
    MapSelector,
    Visualization,
    About,
  },

  data: () => {
    return {
      //Avaiable values for page name: 'Config', 'Map', 'Visualization', 'About'
      page: "",
      //year: new Date().getFullYear(),
      loading: 0,
      urlJump: {
        "/": "/config/",

        "/home/": "/config/",
        "/index/": "/config/",
        "/config/": "/config/",
        "/vis/": "/vis/",
        "/about/": "/about/",
        "/map/": "/map/",
        //"/raw/": "/raw/",

        "/home": "/config/",
        "/index": "/config/",
        "/config": "/config/",
        "/vis": "/vis/",
        "/about": "/about/",
        "/map": "/map/",
        //"/raw": "/raw/",
      },
      url2View: {
        "/config/": "Config",
        "/vis/": "Visualization",
        "/about/": "About",
        "/map/": "Map",
        //"/raw/": "Raw",
      },
      view2Url: {},
      items: [
        { target: "Config", title: "Config Panel", icon: "mdi-view-dashboard" },
        { target: "Map", title: "Map", icon: "mdi-google-maps" },
        {
          target: "Visualization",
          title: "Data Visualization",
          icon: "mdi-image",
        },
        //{target: "Raw", title: "Raw Data", icon: "mdi-xml" },
        { target: "About", title: "About", icon: "mdi-help-box" },
      ],
      right: null,
      head_line: "Who is Flying over?",
    };
  },
  methods: {
    navigate(destination) {
      this.$data.page = destination;
      history.pushState({}, "", this.$data.view2Url[destination]);
    },
    overlay(state) {
      this.$data.loading += state ? 1 : -1;
    },
  },
  watch: {},
  mounted() {
    let real_page = this.$data.urlJump[window.location.pathname];
    history.pushState({}, "", real_page);
    this.$data.page = this.$data.url2View[real_page];
    for (let i in this.$data.url2View) {
      this.$data.view2Url[this.$data.url2View[i]] = i;
    }
  },
};
</script>
