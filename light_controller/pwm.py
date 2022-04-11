import gpiozero
import time
import logging
import redis


if __name__=='__main__':
    l = gpiozero.PWMLED(17)
    a = [i for i in range(100)]
    a = a[::-1]

    for i in a:
        time.sleep(0.03)
        l.value = i/100.0
