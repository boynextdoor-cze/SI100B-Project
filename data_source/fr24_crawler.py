#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#

import redis
import logging
import json
import requests
import time
import re
from pprint import pprint



class Fr24Crawler:
    def __init__(self, loc, rng): # loc=(latitude,lontitude)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_handler = logging.StreamHandler()
        self.log_formatter = logging.Formatter(fmt=r'[%(levelname)s] file=%(filename)s time=%(asctime)s :: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)

        self.redis = redis.Redis(host='localhost',port=6379,db=0)
        self.get_range(loc,rng)

        self.url_template = r'https://zh.flightaware.com/ajax/vicinity_aircraft.rvt?&minLat={}&maxLat={}&minLon={}&maxLon={}&token={}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
        self.token = '';self.token_life = 30;self.token_upd = -1e9
        self.get_token(force_refresh=True)
        self.interval = int(1e9)

        self.msg_src = self.redis.pubsub()
        self.msg_src.subscribe('control-range','control-token-life','control-token-refresh','control-fetch-interval')
        self.redis.set('token-life',str(self.token_life))
        self.redis.set('fetch-interval',str(self.interval))


    def get_range(self,loc,rng):
        self.center_lat,self.center_lon = loc
        self.corner_lat,self.corner_lon = rng
        
        lat_delta=abs(loc[0]-rng[0])
        lon_delta=abs(loc[1]-rng[1])
        self.minLon=rng[1]
        self.maxLon=self.center_lon+lon_delta
        self.minLat=self.center_lat-lat_delta
        self.maxLat=rng[0]

        self.redis.set('range',str((self.center_lat,self.center_lon,self.corner_lat,self.corner_lon)))



    def get_token(self,force_refresh=False):
        if time.time()>self.token_life + self.token_upd or force_refresh:
            r = requests.get('https://zh.flightaware.com/live/')
            m = re.search('"VICINITY_TOKEN":"([^"]+)"', r.text)
            self.token = m.group(1)
            self.redis.set('token',str(self.token))
        self.token_upd = int(time.time())
        self.redis.set('token-upd',str(self.token_upd))



    def get_data_once(self):
        self.get_token()
        url = self.url_template.format(self.minLat,self.maxLat,self.minLon,self.maxLon,self.token)
        response = requests.get(url,headers=self.headers)
        if response.status_code != 200: # re-try if the token expires
            self.get_token(force_refresh=True)
            response = requests.get(url,headers=self.headers)


        origin=json.loads(response.text)['features']
        self.logger.info('request get -> response {}'.format(response.status_code))
        data=[]
        for item in origin:
            detail={}
            if "coordinates" not in item["geometry"]:
                detail['longitude'] = detail['latitude'] = None
            else:
                detail['longitude'] = item['geometry']["coordinates"][0]
                detail['latitude'] = item['geometry']["coordinates"][1]
            if "direction" not in item["properties"]:
                detail['heading'] = None
            else:
                detail['heading'] = item["properties"]["direction"]
            if "ident" not in item["properties"]:
                detail['ident'] = None
            else:
                detail['ident'] = item["properties"]["ident"]
            if ("origin" not in item["properties"]) or ("iata" not in item["properties"]["origin"]):
                detail['departure'] = None
            else:
                detail['departure'] = item["properties"]["origin"]["iata"]
            if ("destination" not in item["properties"]) or ("iata" not in item["properties"]["destination"]):
                detail['arrival'] = None
            else:
                detail['arrival'] = item["properties"]["destination"]["iata"]
            if 'altitude' not in item["properties"]:
                detail['altitude'] = None
            else:
                detail['altitude'] = item["properties"]["altitude"] * 100/3.32 # 100 ft -> 1 m
            if 'groundspeed' not in item["properties"]:
                detail['groundspeed'] = None
            else:
                detail['groundspeed'] = item["properties"]["groundspeed"]
            data.append(detail)
        
        with open('/tmp/flights.json','w') as f:
            f.write(json.dumps(data))
        self.redis.set('flights',json.dumps(data))
        self.redis.set('flights-upd',int(time.time()))
        self.redis.publish('control-data-update', ' ')


    
    def spin(self, interval=10):
        self.interval = interval
        self.redis.set('fetch-interval',str(self.interval))

        last_fetch_time = time.time()
        wake_up_interval = 0.3
        while True:
            self.get_data_once()
            last_fetch_time = time.time()
            while time.time() < last_fetch_time + self.interval:
                time.sleep(wake_up_interval)
                while True: # deal with all received message
                    msg = self.msg_src.get_message()
                    if msg is None: break
                    if msg['type']!='message': continue
                    chn,data = msg['channel'].decode(),msg['data'].decode()
                    self.logger.info('message received. channel,data={},{}'.format(chn,data))

                    if chn=='control-range':
                        pos = eval(data)
                        loc,rng = (pos[0],pos[1]),(pos[2],pos[3])
                        self.get_range(loc,rng)
                        pass
                    elif chn=='control-fetch-interval':
                        self.interval = int(data)
                        self.redis.set('fetch-interval',str(self.interval))
                        pass
                    elif chn=='control-token-life':
                        self.token_life = int(data)
                        self.redis.set('token-life',str(self.token_life))
                        pass
                    elif chn=='control-token-refresh':
                        self.get_token(force_refresh=True)
                        pass

                    self.logger.info("state changed to loc{}; interval={}; token_upd={}".format((self.minLat,self.maxLat,self.minLon,self.maxLon),self.interval,self.token_upd))

            

if __name__ == "__main__":
    shtu_lat,shtu_lon = 31.17940,121.59043
    rng = 1.5
    testing_crawler=Fr24Crawler((shtu_lat,shtu_lon),(shtu_lat+rng,shtu_lon-rng))
    testing_crawler.spin()
