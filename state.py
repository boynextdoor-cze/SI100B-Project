#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#
from data_source.fr24_crawler import Fr24Crawler
from light_controller.controller import *
import json
import time
import redis
import logging


class State:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_handler = logging.StreamHandler()
        self.log_formatter = logging.Formatter(fmt=r'[%(levelname)s] file=%(filename)s time=%(asctime)s :: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)

        self.led_ctl = BaseController(); self.led_ctl.off()

        self.redis = redis.Redis(host='localhost',port=6379,db=0)
        self.msg_src = self.redis.pubsub()
        self.msg_src.subscribe('control-led-interval','control-led-active','control-led-base','control-led-mode')
        self.active=True; self.interval=7; self.base=1; self.mode=MODE_STABLE
        self.redis.set('led-active',str(1 if self.active else 0))
        self.redis.set('led-interval',str(self.interval))
        self.redis.set('led-base',str(self.base))
        self.redis.set('led-mode',str(self.mode))


    def refresh(self): # TODO: change LED output according to (mode and flights)
        fs = self.redis.get('flights')
        if fs is None: fs = []
        else: fs = json.loads(fs.decode())
        tmp = len(fs)//(10**self.base)
        if ENABLE_LED_LOG: self.logger.info('flights.len={} base={};output={}'.format(len(fs),self.base,tmp))

        # count of LED-on = max{ LED_CNT,flights_cnt/(10^base) }
        self.output = [1 if tmp>=i else 0 for i in range(1,LED_CNT+1)]
        self.led_ctl.off()
        self.led_ctl.work_once(self.output,self.mode)


    def spin(self,interval=7):
        self.interval=interval;self.redis.set('led-interval',str(self.interval))
        last_upd_time = time.time()
        wake_up_interval = 0.3
        while True:
            if self.active: self.refresh()
            last_upd_time = time.time()

            while time.time() < last_upd_time + self.interval:
                time.sleep(wake_up_interval)
                while True: # deal with all received message
                    msg = self.msg_src.get_message()
                    if msg is None: break
                    if msg['type']!='message': continue
                    chn,data = msg['channel'].decode(),msg['data'].decode()
                    self.logger.info('message received. channel,data={},{}'.format(chn,data))

                    if chn=='control-led-interval':
                        self.interval = int(data)
                        self.redis.set('led-interval',str(self.interval))
                        pass
                    elif chn=='control-led-active':
                        self.active = True if int(data)>0 else False
                        self.redis.set('led-active',str(1 if self.active else 0))
                        if self.active: self.refresh()
                        else: self.led_ctl.off()
                    elif chn=='control-led-base':
                        self.base = int(data)
                        self.redis.set('led-base',str(self.base))
                    elif chn=='control-led-mode':
                        self.mode = int(data)
                        if self.active: self.refresh()
                        self.redis.set('led-mode',str(self.mode))
                    self.logger.info('state changed to intveval={},active={},base={},mode={}'.format(self.interval,self.active,self.base,self.mode))

                


if __name__ == "__main__":
    State().spin()
