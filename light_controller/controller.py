#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#
GPIO_AVAILABLE=__import__('os').path.isfile('/usr/bin/gpio')
ENABLE_LED_LOG=True

LED_PIN = [
        4,
        17,
        27,
        5
]

LED_CNT = len(LED_PIN)

MODE_STABLE = 0
MODE_BLINK = 1
BLKDUR_ON = 0.5
BLKDUR_OFF = 0.5

import gpiozero
import itertools
import logging
import time


class BaseController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_handler = logging.StreamHandler()
        self.log_formatter = logging.Formatter(fmt=r'[%(levelname)s] file=%(filename)s time=%(asctime)s :: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)
        

        if GPIO_AVAILABLE: self.led = list(map(gpiozero.PWMLED,LED_PIN))
        self.map = [0.0 for i in range(LED_CNT)]
        self.off()

    def work_once(self,s,mode):
        self.map = s
        if ENABLE_LED_LOG: self.logger.info('set LED output={}'.format(s))

        if not GPIO_AVAILABLE: return None # for testing on PC
        for (led,val) in zip(self.led,self.map):
            if mode==MODE_STABLE:
                led.value = val
            elif mode==MODE_BLINK:
                if val>0: led.blink(on_time=BLKDUR_ON,off_time=BLKDUR_OFF)
            else: # TODO: add other display mode
                pass


    def set_all(self,power): self.work_once([power for i in self.map],mode=MODE_STABLE)
    def off(self):
        if not GPIO_AVAILABLE: return None # for testing on PC
        for i in self.led: i.off()


# running test
if __name__=='__main__':
    c = BaseController()
    LIM = 100
    tmp = list(range(LIM))[::-1]


    def test_group():
        for i in tmp:
            c.set_all(float(i)/LIM)
            time.sleep(0.01)
        c.off()
        pass
    def test_one(x):
        for i in tmp:
            c.work_once([float(i)/LIM if j==x else 0.0 for j  in range(LED_CNT)],mode=MODE_STABLE)
            time.sleep(0.01)
        c.off()
        pass
    def test_blink(x):
        c.work_once([1 if j==x else 0 for j  in range(LED_CNT)],mode=MODE_BLINK)
        time.sleep(2)
        c.off()
        pass




    test_group()
    time.sleep(3)

    for i in range(LED_CNT):
        test_one(i)
    time.sleep(3)

    for i in range(LED_CNT):
        test_blink(i)

