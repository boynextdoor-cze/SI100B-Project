<template>
  <!--Don't use v-if since it'll delete the DOM-->
  <div v-show="enabled" class="fill-height">
    <v-row align="center" class="fill-height mx-6">
      <v-item-group v-model="window" class="shrink mr-6" mandatory tag="v-flex">
        <v-item v-for="item in vis_list" :key="item.title" v-slot="{ active, toggle }">
          <div>
            <v-btn :input-value="active" icon @click="toggle">
              <v-icon>mdi-record</v-icon>
            </v-btn>
          </div>
        </v-item>
      </v-item-group>

      <v-col fill-height>
        <v-window v-model="window" class="elevation-1 ma-0" vertical>
          <v-window-item v-for="item in vis_list" :key="item.title" class="ma-0">
            <v-card flat>
              <v-card-text>
                <strong class="title text-h4 pl-3">{{ item.title }}</strong>
                <v-divider></v-divider>
                <v-subheader> {{ item.description }} </v-subheader>

                <v-container class="pa-0 ma=0">
                  <v-row justify="center" align="center pa-0 ma=0">
                    <img class="ma-0" width="80%" :src="item.image" />
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
import { Bus } from "../modules/Bus";
let self;
export default {
  name: "visualization",
  data: () => {
    return {
      now: parseInt(new Date().valueOf() / 1000),
      render_upd: 0,
      vis_list: {},
      vis_update_sleep: 0,
      window: 0,
    };
  },
  props: {
    enabled: {
      type: Boolean,
      required: true,
    },
  },
  watch: {},
  methods: {
    clock() {
      self.$data.now = parseInt(new Date().valueOf() / 1000);
      if (!self.$data.vis_update_sleep) {
        ++self.$data.vis_update_sleep;
        axios({
          method: "get",
          url: "/agg/last-render-timestamp/",
        })
          .then((response) => {
            let new_render_upd = response.data["render-upd"];
            if (new_render_upd != self.$data.render_upd)
              self.$data.render_upd = new_render_upd;
            self.$options.methods.updateVisualization();
            console.log(response);
          })
          .catch((error) => {
            console.error(error);
          })
          .finally(()=>{
            --self.$data.vis_update_sleep;
          });
      }
    },
    updateVisualization() {
      //Update images
      for (let key in self.$data.vis_list) {
        ++self.$data.vis_update_sleep;
        axios({
          method: "get",
          url: `/agg/${key}`,
        })
          .then((response) => {
            self.$set(self.$data.vis_list[key], "image", response.data["image"]);
            console.log(response);
          })
          .catch((error) => {
            console.error(error);
          })
          .finally(() => {
            setTimeout(() => {
              --self.$data.vis_update_sleep;
            }, 10000);
          });
      }
    },
  },
  created: function () {
    self = this;
  },
  mounted: () => {
    self.$emit("overlay", true);
    //Init agg list

    axios({
      method: "get",
      url: "/agg/",
    })
      .then((response) => {
        self.$data.vis_list = response.data["list"];
        self.$options.methods.updateVisualization();
        console.log(response);
      })
      .catch((error) => {
        console.error(error);
      })
      .finally(() => {
        setTimeout(() => {
          self.$emit("overlay", false);
        }, 200);
      });

    Bus.$on("pub_crawler_interval", (msg) => {
      self.$data.crawler_interval = msg.crawler_interval;
    });

    setInterval(self.$options.methods.clock, 1000);
  },
};
</script>
