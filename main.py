from state import State
from data_source.fr24_crawler import Fr24Crawler
from web_server.server import web_server
from static_data_loader.static_data_loader import StaticDataLoader
from visualizer.visualizer import Visualizer
from sys import argv as exec_args
import time
import logging
import multiprocessing
import os

_logger = None
def _logger_init():
    logger = logging.getLogger("si100b_proj:main")
    logger.setLevel(logging.INFO)
    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(fmt=r'[%(levelname)s] file=%(filename)s time=%(asctime)s :: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    return logger


def _start_server():
    _logger.info(f'Web server runing as PID={os.getpid()}')
    web_server.run(host="0.0.0.0", port=8999, debug=False)
    # **FIXME: server.run(debug=True) cause a fork resulting in twice code execution**
    # detailed description: 帶上debug参数,会出现两个crawler进程,两个visualizer进程.通过观察log中的PID信息可以确认是否发生了这个问题.
def _start_crawler():
    _logger.info('Crawler server runnning...')
    shtu_lat,shtu_lon = 31.17940,121.59043;rng = 1.5
    cralwer=Fr24Crawler((shtu_lat,shtu_lon),(shtu_lat+rng,shtu_lon-rng))
    cralwer.spin()
def _start_ledcontroller():
    _logger.info(f'LED controler running as PID={os.getpid()}')
    state = State()
    state.spin()
def _start_visualizer():
    _logger.info(f'Visualizer running as PID={os.getpid()}')
    visualizer = Visualizer()
    visualizer.spin()
def _prepare_static_data_loader():
    _logger.info('Static data loader starting...')
    StaticDataLoader.load()
    _logger.info('Static data loader finished.')

if __name__ == '__main__':
    _logger = _logger_init()
    _logger.info(f'Main process started at PID={os.getpid()}')

    prepare_funcs = [_prepare_static_data_loader]
    for i in prepare_funcs: i()
    
    loop_funcs = [_start_crawler, _start_visualizer, _start_ledcontroller, _start_server]
    pool = []
    for i in loop_funcs:
        proc = multiprocessing.Process(target=i)
        proc.start()
        pool.append(proc)

    try:
        wake_up_interval = 10
        while True:
            time.sleep(wake_up_interval)
    except KeyboardInterrupt:
        for i in pool:
            i.terminate()
    finally:
        for i in pool:
            i.join() #Wait for all processes to terminate
        _logger.info('All processes terminated.')
