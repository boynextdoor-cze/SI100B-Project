# Data visualization
import matplotlib
import matplotlib.figure
#import xml.etree.ElementTree as ET

# Data processing
import numpy as np
import collections
import math

#IO
import base64
import io
import json
import redis

# Miscs
import sys
import time
import typing
import logging

redis_pool = None

colors = {  # Material Design Colors
    'red lighten-2': '#E57373',
    'pink lighten-2': '#F06292',
    'purple lighten-2': '#BA68C8',
    'deep-purple lighten-2': '#9575CD',
    'indigo lighten-2': '#7986CB',
    'blue lighten-2': '#64B5F6',
    'light-blue lighten-2': '#4FC3F7',
    'cyan lighten-2':  '#4DD0E1',
    'teal lighten-2':  '#4DB6AC',
    'green lighten-2': '#81C784',
    'light-green lighten-2': '#AED581',
    'lime lighten-2': '#DCE775',
    'yellow lighten-2': '#FFF176',
    'amber lighten-2': '#FFD54F',
    'orange lighten-2': '#FFB74D',
    'deep-orange lighten-2': '#FF8A65',
    'brown lighten-2': '#A1887F',
    'blue-grey lighten-2': '#90A4AE',
    'grey lighten-2': '#E0E0E0'
}
class StaticDataReader:
    def __init__(self):
        global redis_pool
        self.redis_connection = redis.Redis(connection_pool=redis_pool)
        self.airports = json.loads(str(self.redis_connection.get('static-airports').decode()))
    
    def locateAirport(self, IATA:str):

        if IATA in self.airports:
            return self.airports[IATA]['Location served'][-1] # Last element
        else:
            return None # Do not raise an error for convenience
            #raise KeyError('There is no such IATA code!')
class Drawer:
    description = {}

    def draw(self, fig: matplotlib.figure.Figure):
        raise NotImplementedError

    def output(self):
        self.dpi = 100
        fig = matplotlib.figure.Figure(figsize=[8, 4.5], dpi=self.dpi)
        self.draw(fig)
        # fig.tight_layout() # Useless, cause warning
        buf = io.BytesIO()
        fig.savefig(buf, format="svg")
        # Return raw SVG directly
        '''
            return buf.getvalue().decode()
        '''
        # Return Base64 encoded SVG in Data URI
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f"data:image/svg+xml;base64,{data}"


class AltitudeDistribution(Drawer):
    description = {
        "title": "Altitude Distribution",
        "description": "Who is 仌?",
    }

    def __init__(self, data):
        self.data = np.array([i["altitude"] for i in data])
        self.data = self.data[self.data != None]

    def draw(self, fig: matplotlib.figure.Figure):
        axs = fig.subplots()
        '''data = np.random.randint(0, 10, 1000)
        axs.hist(data, bins=range(11))
        axs.set_xticks(range(10))

        '''
        axs.hist(self.data, bins=range(0, 15000+1500, 1500),
                 color=colors['teal lighten-2'])
        axs.set_xlabel("Altitude(m)")
        axs.set_ylabel("Quantity of flights")
        axs.set_xlim(left=0)
        axs.set_xticks(range(0, 15000, 1500))

class GroundSpeedDistribution(Drawer):
    description = {
        "title": "Ground Speed Distribution",
        "description": "Hong Kong reporters NO. 1!",
    }

    def __init__(self, data):
        self.data = np.array([i["groundspeed"] for i in data])
        self.data = self.data[self.data != None]

    def draw(self, fig: matplotlib.figure.Figure):
        axs = fig.subplots()
        axs.hist(self.data, bins=range(0, 1000+100, 100),
                 color=colors['teal lighten-2'])
        axs.set_xlabel("Ground Speed(kn)")
        axs.set_ylabel("Quantity of flights")
        axs.set_xlim(left=0)
        axs.set_xticks(range(0, 1000, 100))


class CountryDistribution(Drawer):
    description = {
        "title": "Country Distribution",
        "description": "Where do you come from? Where would you go?"
    }

    @staticmethod
    def fixData(data: typing.Dict[str, int], weight_all: int):
        if None in data:
            del data[None]
        others = 0
        for k, v in data.copy().items():
            if v < 0.015 * weight_all:
                others += v
                del data[k]
        if others != 0:
            data['Others'] = others
        data = dict(sorted(data.items(), key=lambda x: -x[1]))

    def __init__(self, data):
        self.data_reader = StaticDataReader()
        self.weight_all = len(data)

        self.departure = collections.Counter([
            self.data_reader.locateAirport(i['departure'])
            for i in data
        ])
        self.fixData(self.departure, self.weight_all)

        self.arrival = collections.Counter([
            self.data_reader.locateAirport(i['arrival'])
            for i in data
        ])
        self.fixData(self.arrival, self.weight_all)

    def drawLabels(self, ax: matplotlib.axes.Axes, pies, labels: typing.List[str]):
        '''
            A function to locate the labels for a better look
        '''
        count = len(pies)
        for i in range(count):
            raw_rotation = (pies[i].theta2 -
                            pies[i].theta1) / 2 + pies[i].theta1
            txt_path = matplotlib.textpath.TextPath((0, 0), labels[i].strip())
            txt_width = txt_path.get_extents().width
            if 90 < raw_rotation < 90 * 3:
                offset_x = 1.25 + txt_width / self.dpi 
                fix_rotation = (raw_rotation + 180) % 360
            else:
                offset_x = 1.25
                fix_rotation = raw_rotation

            txt = ax.text(x=offset_x,
                          y=0,
                          s=labels[i],
                          verticalalignment='center',
                          transform=matplotlib.transforms.Affine2D().
                          rotate_deg_around(0, 0, raw_rotation) + ax.transData)
            txt.set_zorder(1)
            txt.set_rotation_mode('anchor')
            txt.set_rotation(fix_rotation)

    def draw(self, fig):
        axs1, axs2 = fig.subplots(1, 2)

        p1, _ = axs1.pie(np.array(list(self.departure.values())) / (self.weight_all),
                         colors=colors.values(),
                         normalize=False)
        axs1.set_title('Departure Airports')
        self.drawLabels(axs1, p1, list(self.departure.keys()))

        p2, _ = axs2.pie(np.array(list(self.arrival.values())) / (self.weight_all),
                         colors=colors.values(),
                         normalize=False,)
                         #autopct="%.2f%%")
        axs2.set_title('Arrival Airports')
        self.drawLabels(axs2, p2, list(self.arrival.keys()))

class Visualizer:

    drawerList = {
        "a-altitude-distribution": AltitudeDistribution,
        "b-ground-speed_distribution": GroundSpeedDistribution,
        "c-country-distribution": CountryDistribution
    }
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.log_handler = logging.StreamHandler()
        self.log_formatter = logging.Formatter(fmt=r'[%(levelname)s] file=%(filename)s time=%(asctime)s :: %(message)s',datefmt=r'%Y-%m-%d %H:%M:%S')
        self.log_handler.setFormatter(self.log_formatter)
        self.logger.addHandler(self.log_handler)

        global redis_pool
        redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.redis_connection = redis.Redis(connection_pool=redis_pool)
        
        self.redis_connection.set('vis-list', json.dumps(
            {k:v.description for (k, v) in Visualizer.drawerList.items()}
        ))
        self.msg_src = self.redis_connection.pubsub()
        self.msg_src.subscribe('control-data-update')
        
        matplotlib.use("SVG")
        matplotlib.interactive(False)

    def draw_all(self):
        data = json.loads(self.redis_connection.get('flights').decode())
        for (k, v) in self.drawerList.items():
            self.redis_connection.set(k, v(data).output())
    def spin(self):
        import os
        self.logger.error(f"this is {os.getpid()} visual")
        wake_up_interval = 1
        while True: 
            # The structure promise that visualizer is always being runned in a single thread,
            # Therefore, there won't be issues about thread safety happen on matplotlib. 
            time.sleep(wake_up_interval)
            while True: # deal with all received message
                msg = self.msg_src.get_message()
                if msg is None: break
                if msg['type']!='message': continue
                    
                chn,data = msg['channel'].decode(),msg['data'].decode()
                from os import getpid,getppid
                self.logger.info('PID={},PPID={}::message received. channel,data={},{}'.format(getpid(),getppid(),chn,data))

                if chn=='control-data-update':
                    self.logger.info("visualizer drawing.")
                    self.draw_all()
                    self.redis_connection.set('render-upd', int(time.time()))
                    self.logger.info("visualizer finish.")
                        

if __name__ == "__main__":
    import os

    matplotlib.use("AGG")  # For PNG
    matplotlib.interactive(False)

    x = np.linspace(-1, 1, 100)
    fig = matplotlib.figure.Figure(figsize=[8, 4])
    fig.subplots().plot(x, x**2)

    path = os.path.join(os.path.dirname(__file__), 'quadric.png')

    fig.savefig(path, format="png")
