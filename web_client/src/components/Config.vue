<template>
  <!--Don't use v-if since it'll delete the DOM-->
  <div v-show="enabled" class="fill-height">
    <v-container fluid class="fill-height">
      <v-row class="fill-height"
        ><v-col style="width: 50%">
          <v-card
            class="fill-height rounded-lg pa-3"
            elevation="2"
            color="blue-grey lighten-5"
          >
            <v-card-title class="headline font-weight-bold">
              <v-icon large left> mdi-spider </v-icon>
              <div color="blue-grey darken-4">Crawler</div>
            </v-card-title>
            <v-form ref="crawler_form">
              <v-slider
                v-model="crawler_interval"
                label="Crawl interval:"
                thumb-label
                min="10"
                max="60"
              ></v-slider>
              <v-slider
                v-model="crawler_token_life_new"
                label="Token lifespan:"
                thumb-label
                min="30"
                max="90"
              ></v-slider>
              <v-subheader class="text-caption"
                >{{ crawler_token_state_string }}
              </v-subheader>
              <v-text-field
                label="Range"
                :rules="crawler_range_rules"
                hide-details="auto"
                v-model="crawler_range_string"
                v-bind:value="crawler_range_string"
              ></v-text-field>
              <v-subheader class="text-caption">
                (e.g. "31.17940, 121.59043, 32.67940, 120.09043" for Shanghaitech
                University)</v-subheader
              >
              <v-btn
                elevation="2"
                class="mx-5 my-3"
                @click="pushCrawler()"
                v-bind:color="crawler_submit_state"
                >Update!</v-btn
              >
              <v-btn
                elevation="2"
                class="mx-5 my-3"
                @click="pushToken(true)"
                v-bind:color="crawler_update_token_state"
                >Refresh token!</v-btn
              >
            </v-form>
          </v-card> </v-col
        ><v-col style="width: 50%">
          <v-card
            class="fill-height rounded-lg pa-3"
            elevation="2"
            color="blue-grey lighten-5"
          >
            <v-card-title class="headline font-weight-bold">
              <v-icon large left> mdi-led-on </v-icon>
              <div color="blue-grey darken-4">LED</div>
            </v-card-title>
            <v-form ref="led_form">
              <label
                class="v-label theme--light"
                style="left: 0px; right: auto; position: relative width: fixed"
              >
                Enabled:
              </label>
              <v-switch
                style="display: inline-block"
                v-model="led_active"
                class="mx-5"
              ></v-switch>
              <v-slider
                v-model="led_interval"
                label="LED interval:"
                thumb-label
                min="1"
                max="60"
              ></v-slider>
              <v-slider
                v-model="led_base"
                label="Base:"
                thumb-label
                min="0"
                max="5"
              ></v-slider>
              <v-select label="Mode" v-model="led_mode" :items="led_mode_set"></v-select>
              <v-btn
                elevation="2"
                class="mx-5 my-3"
                @click="pushLed()"
                v-bind:color="led_submit_state"
                >Update!</v-btn
              >
            </v-form>
          </v-card></v-col
        ></v-row
      >
    </v-container>
  </div>
</template>

<script>
let self;
import axios from "axios";
import { Bus } from "../modules/Bus";
axios.defaults.headers.post["Content-Type"] = "application/json";
export default {
  name: "config",
  data: () => {
    return {
      now: parseInt(new Date().valueOf() / 1000),

      crawler_token_update_sleep: false,
      crawler_interval: 10,
      crawler_token: null,
      crawler_token_life_new: 60,
      crawler_token_life: 60,
      crawler_token_birth: 0,
      crawler_token_state_string: "",
      crawler_range: {
        center_lat: 31.1794,
        center_lon: 121.59043,
        corner_lat: 32.6794,
        corner_lon: 120.09043,
      },
      crawler_range_rules: [
        function (value) {
          //Write all rules in one key-value pair to control the orders of the rules.
          if (
            !/^\s*(-?\d*(\.\d+)?)\s*,\s*(-?\d*(\.\d+)?)\s*,\s*(-?\d*(\.\d+)?)\s*,\s*(-?\d*(\.\d+)?)\s*$/.test(
              value
            )
          )
            return "Please input longtitudes and latitudes!";
          else if (self && !self.parseRange(value))
            //wait for init
            return "Longtitudes and latitudes are out of bounds!";
            
          Bus.$emit("pub_config_crawler_range", {
            crawler_range: self.$data.crawler_range,
          });

          return true;
        },
      ],
      crawler_submit_state: "normal",
      crawler_update_token_state: "normal",

      led_interval: 5,
      led_active: false,
      led_base: 3,
      led_mode_set: [
        {
          text: "Normally on",
          value: 0,
        },
        {
          text: "Twinkle",
          value: 1,
        },
      ],
      led_mode: 0,
      led_submit_state: "normal",
    };
  },
  computed: {
    //No arrow functions in computed! computed use this.* to listen data!
    crawler_range_string: {
      get() {
        return `${this.crawler_range.center_lat}, ${this.crawler_range.center_lon}, ${this.crawler_range.corner_lat}, ${this.crawler_range.corner_lon}`;
      },
      set(value) {
        this.crawler_range = this.parseRange(value);
      },
    },
  },
  props: {
    enabled: {
      type: Boolean,
      required: true,
    },
  },
  watch: {
    //enabled(new_val){
    //   if(new_val)
    //self.$data.crawler_range = (new Sharer).crawler_range;
    //},
    crawler_token() {
      let life_left =
        self.$data.crawler_token_life + self.$data.crawler_token_birth - self.$data.now;
      self.$data.crawler_token_state_string = self.$data.crawler_token
        ? 'Current token: "' +
          self.$data.crawler_token +
          '", ' +
          (life_left > 0 ? "expire in " + life_left + "s" : "already expired") +
          "."
        : "Failed to get current token.";
    },
  },
  methods: {
    clock() {
      self.$data.now = parseInt(new Date().valueOf() / 1000);

      let life_left =
        self.$data.crawler_token_life + self.$data.crawler_token_birth - self.$data.now;
      if (life_left < 0 && !self.$data.crawler_token_update_sleep)
        self.$options.methods.pullToken();
      self.$data.crawler_token_state_string = self.$data.crawler_token
        ? `Current token: "${self.$data.crawler_token}", ` +
          (life_left > 0 ? `expire in ${life_left} s.` : "already expired.")
        : "Failed to get current token.";
    },
    parseRange(input) {
      try {
        let group_input = input.split(",");
        let output = {};
        output.center_lat = parseFloat(group_input[0].trim());
        output.center_lon = parseFloat(group_input[1].trim());
        output.corner_lat = parseFloat(group_input[2].trim());
        output.corner_lon = parseFloat(group_input[3].trim());
        return -90 <= output.center_lat &&
          output.center_lat <= 90 &&
          -360 <= output.center_lon &&
          output.center_lon <= 360 &&
          -90 <= output.corner_lat &&
          output.corner_lat <= 90 &&
          -360 <= output.corner_lon &&
          output.corner_lon <= 360
          ? output
          : undefined;
      } catch (error) {
        console.error(error);
        return undefined;
      }
    },
    pushToken() {
      if (self.$data.crawler_update_token_state != "normal") return;
      self.$emit("overlay", true);
      axios({
        method: "post",
        url: "/crawler/",
        "content-type": "application/json",
        data: JSON.stringify({ "token-refresh": 1 }),
      })
        .then((response) => {
          self.$data.crawler_update_token_state = "success";
          setTimeout(() => {
            self.$data.crawler_update_token_state = "normal";
          }, 200);

          setTimeout(self.$options.methods.pullToken(), 5000);
          console.log(response);
        })
        .catch((error) => {
          self.$data.crawler_update_token_state = "error";
          setTimeout(() => {
            self.$data.crawler_update_token_state = "normal";
          }, 200);
          console.error(error);
        })
        .finally(() => {
          setTimeout(() => {
            self.$emit("overlay", false);
          }, 200);
        });
    },
    pullToken(click = false) {
      self.$data.crawler_token_update_sleep = true; //Stop token on-time refresh to prevent bugs.
      axios({
        method: "get",
        url: "/crawler/",
      })
        .then((response) => {
          self.$data.crawler_token_life = response.data["token-life"];
          if (click) self.$data.crawler_token_life_new = self.$data.crawler_token_life;
          self.$data.crawler_token_birth = response.data["token-upd"];
          self.$data.crawler_token = response.data["token"];
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          self.$data.crawler_token_update_sleep = false;
        });
    },
    pushCrawler() {
      if (self.$data.crawler_submit_state != "normal") return;
      if (self.$refs.crawler_form.validate()) {
        self.$emit("overlay", true);
        axios({
          method: "post",
          url: "/crawler/",
          "content-type": "application/json",
          data: JSON.stringify({
            "token-life": self.$data.crawler_token_life_new,
            interval: self.$data.crawler_interval,
            range: self.$data.crawler_range,
          }),
        })
          .then((response) => {
            self.$data.crawler_submit_state = "success";
            self.$data.crawler_token_life = self.$data.crawler_token_life_new;
            Bus.$emit("pub_crawler_interval", {
              crawler_interval: self.$data.crawler_interval,
            });
            setTimeout(() => {
              self.$data.crawler_submit_state = "normal";
            }, 200);
            console.log(response);
          })
          .catch((error) => {
            self.$data.crawler_submit_state = "error";
            setTimeout(() => {
              self.$data.crawler_submit_state = "normal";
            }, 200);
            console.log(error);
          })
          .finally(() => {
            setTimeout(() => {
              self.$emit("overlay", false);
            }, 200);
          });
      }
    },
    pullCrawler() {
      self.$data.crawler_token_update_sleep = true; //Stop token on-time refresh to prevent bugs.
      self.$emit("overlay", true);
      axios({
        method: "get",
        url: "/crawler/",
      })
        .then((response) => {
          self.$data.crawler_interval = response.data["interval"];
          self.$data.crawler_token_birth = response.data["token-upd"];
          self.$data.crawler_token_life_new = self.$data.crawler_token_life =
            response.data["token-life"];
          self.$data.crawler_range = response.data["range"];
          self.$data.crawler_token = response.data["token"];

          Bus.$emit("pub_config_crawler_range", {
            crawler_range: self.$data.crawler_range,
          });

          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          setTimeout(() => {
            self.$emit("overlay", false);
          }, 200);
          self.$data.crawler_token_update_sleep = false;
        });
    },
    pushLed() {
      self.$refs.led_form;
      if (self.$data.led_submit_state != "normal") return;
      if (self.$refs.led_form.validate()) {
        self.$emit("overlay", true);
        axios({
          method: "post",
          url: "/led/",
          "content-type": "application/json",
          data: JSON.stringify({
            active: self.led_active,
            interval: self.$data.led_interval,
            mode: self.$data.led_mode,
            base: self.$data.led_base,
          }),
        })
          .then((response) => {
            self.$data.led_submit_state = "success";
            setTimeout(() => {
              self.$data.led_submit_state = "normal";
            }, 200);
            console.log(response);
          })
          .catch((error) => {
            self.$data.led_submit_state = "error";
            setTimeout(() => {
              self.$data.led_submit_state = "normal";
            }, 200);
            console.error(error);
          })
          .finally(() => {
            setTimeout(() => {
              self.$emit("overlay", false);
            }, 200);
          });
      }
    },
    pullLed() {
      self.$emit("overlay", true);
      axios({
        method: "get",
        url: "/led/",
      })
        .then((response) => {
          self.$data.led_interval = response.data["interval"];
          self.$data.led_active = response.data["active"];
          self.$data.led_mode = response.data["mode"];
          self.$data.led_base = response.data["base"];
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
    },
  },
  created() {
    //This must not be arrow function, or "this" would be undefined.
    self = this;
  },
  mounted() {
    //axios is async so the overlay won't shine.

    Bus.$on("pub_map_crawler_range", (message) => {
      self.$data.crawler_range = message.crawler_range;
    });

    self.$options.methods.pullCrawler();
    self.$options.methods.pullLed();

    setInterval(self.$options.methods.clock, 1000);
  },
};
</script>
