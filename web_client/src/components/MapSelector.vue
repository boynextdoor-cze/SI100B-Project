<template>
  <!-- 
    No v-show here, 
    See: https://github.com/mapbox/mapbox-gl-js/issues/3265#issuecomment-561801434
  -->
  <div v-show="enabled" class="fill-height fill-width ma-0">
    <!--<v-row align="center" class="fill-height fill-width ma-3">-->
    <div id="map-box-gl" style="width: 100%; height: 100%"></div>
    <!--</v-row>-->
  </div>
</template>

<script>
import mapboxgl from "mapbox-gl";
import axios from "axios";

import { Bus } from "../modules/Bus";
//import { createElementFromHTML } from "../modules/Parse";

import "../styles/mapbox-gl.css";

import plane from "../assets/plane.svg";
import $ from "jquery";

let self;

export default {
  name: "map-selector",
  data: () => {
    return {
      now: parseInt(new Date().valueOf() / 1000),
      flights_upd: 0,
      flights_update_sleep: false,
      crawler_interval: 10,
      crawler_range: {
        center_lat: 31.1794,
        center_lon: 121.59043,
        corner_lat: 32.6794,
        corner_lon: 120.09043,
      },
      map: undefined,
      map_token:
        "pk.eyJ1IjoibHlob2tpYSIsImEiOiJja2l4NGIzbWkxN2E3MnJwZnQ1NDZxdWY2In0.XbgXKDuQ9g_1RpjciAQOaw",
      marker_center: new mapboxgl.Marker({
        color: "#2196F3",
        draggable: true,
      }),
      marker_corner: new mapboxgl.Marker({
        color: "#3F51B5",
        draggable: true,
      }),
      marker_planes: [],
    };
  },
  computed: {
    //No arrow functions in computed! computed use this.* to listen data!
  },
  props: {
    enabled: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    clock: () => {
      self.$data.now = parseInt(new Date().valueOf() / 1000);
      if (
        self.$data.now > self.$data.flights_upd + self.$data.crawler_interval &&
        !self.$data.flights_update_sleep
      ) {
        self.$data.flights_update_sleep = true;
        axios({
          method: "get",
          url: "/flights/",
        })
          .then((response) => {
            self.$data.flights_upd = response.data["flights-upd"];
            self.$data.marker_planes.forEach((e) => {
              e.remove();
            });
            self.$data.marker_planes = [];
            let cursor_plane = $("<img>", { src: plane, width: "20px", height: "20px" });
            response.data["flights"].forEach((e) => {
              let flight_marker = new mapboxgl.Marker({
                anchor: "center",
                element: cursor_plane.clone()[0], //Pull raw DOM elements from jQuery Objects.
              })
                .setLngLat([e["longitude"], e["latitude"]])
                .setRotation(e["heading"] - 45) //The svg heads northeast
                .addTo(self.$data.map);
              self.$data.marker_planes.push(flight_marker);
            });
            console.log(response);
          })
          .catch((error) => {
            console.error(error);
          })
          .finally(() => {
            self.$data.flights_update_sleep = false;
          });
      }
    },
    createMap: () => {
      mapboxgl.accessToken = self.$data.map_token;
      self.$data.map = new mapboxgl.Map({
        container: "map-box-gl",
        style: "mapbox://styles/mapbox/dark-v10", // stylesheet location
        center: [
          self.$data.crawler_range.center_lon,
          self.$data.crawler_range.center_lat,
        ], // starting position [lng, lat]
        zoom: 6, // starting zoom
      });

      self.$data.map.addControl(
        new mapboxgl.ScaleControl({
          maxWidth: 80,
          unit: "metric",
        })
      );

      self.$data.marker_center
        ?.setLngLat([
          self.$data.crawler_range.center_lon,
          self.$data.crawler_range.center_lat,
        ])
        ?.addTo(self.$data.map)
        ?.on("dragend", self.$options.methods.updateCrawlerRange);
      self.$data.marker_corner
        ?.setLngLat([
          self.$data.crawler_range.corner_lon,
          self.$data.crawler_range.corner_lat,
        ])
        ?.addTo(self.$data.map)
        ?.on("dragend", self.$options.methods.updateCrawlerRange);
    },

    updateCrawlerRange: () => {
      let center_cord = self.$data.marker_center.getLngLat();
      let corner_cord = self.$data.marker_corner.getLngLat();
      //range: for latitudes, [-90, 90]; for longitudes, [-360, 360].
      let fit_lat = (lat) => {
        return ((lat + 90) % 180) - 90;
      };
      let fit_lng = (lng) => {
        return ((lng - 360) % 720) + 360;
      };
      Bus.$emit("pub_map_crawler_range", {
        crawler_range: {
          center_lon: fit_lng(center_cord.lng),
          center_lat: fit_lat(center_cord.lat),
          corner_lon: fit_lng(corner_cord.lng),
          corner_lat: fit_lat(corner_cord.lat),
        },
      });
    },
  },
  watch: {
    enabled() {
      self.$nextTick(() => {
        self.$data.map.resize(); //Resize the map so it's properly shown.
      });
    },
  },
  created() {
    //This must not be arrow function, or "this" would be undefined.
    self = this;
  },
  mounted() {
    self.$options.methods.createMap();

    Bus.$on("pub_crawler_interval", (msg) => {
      self.$data.crawler_interval = msg.crawler_interval;
    });

    Bus.$on("pub_config_crawler_range", (message) => {
      self.$data.crawler_range = message.crawler_range;
      self.$data.marker_center.setLngLat([
        self.$data.crawler_range.center_lon,
        self.$data.crawler_range.center_lat,
      ]);
      self.$data.marker_corner.setLngLat([
        self.$data.crawler_range.corner_lon,
        self.$data.crawler_range.corner_lat,
      ]);
    });

    //Don't add () after a function when call setInterval!
    setInterval(self.$options.methods.clock, 1000);
  },
};
</script>
