#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 12/05/2020                           #
#=============================================================================#

import json
import logging
import redis
import requests  # For proxy
import traceback
import time

from flask import Flask, request, render_template, redirect, url_for, jsonify, make_response, send_file, Response

web_server = Flask(__name__)
web_server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
server_time = time.localtime(time.time())
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

# Resolve conflicts between Jinja and Vue.js
# Needless, since Jinja isn't used.
# web_server.jinja_env.variable_start_string = '{['
# web_server.jinja_env.variable_end_string = ']}'

# Install logging
web_server.logger = logging.getLogger(__name__)
web_server.logger.setLevel(logging.INFO)
web_server.log_handler = logging.StreamHandler()
web_server.log_formatter = logging.Formatter(
    fmt=r'[%(levelname)s] file=%(filename)s time=%(asctime)s :: %(message)s', datefmt=r'%Y-%m-%d %H:%M:%S')
web_server.log_handler.setFormatter(web_server.log_formatter)
web_server.logger.addHandler(web_server.log_handler)

visualizer_list = {}
inited_data = False
def init_data():  
    global inited_data
    if inited_data: return
    inited_data = True
    rc = redis.Redis(connection_pool=redis_pool)
    global visualizer_list
    visualizer_list = json.loads(rc.get('vis-list').decode())
    #del rc
    # No longer using
    # # Initialize flights data to memory.
    # static_data_loader.StaticDataLoader.init()


@web_server.route('/', methods=['GET'])
@web_server.route('/index/', methods=['GET'])
@web_server.route('/home/', methods=['GET'])
@web_server.route('/config/', methods=['GET'])
@web_server.route('/vis/', methods=['GET'])
@web_server.route('/about/', methods=['GET'])
@web_server.route('/map/', methods=['GET'])
#@web_server.route('/raw/', methods=['GET']) # Not implemented
def vue_interface():
    return send_file("templates/index.html")


@web_server.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_file("favicon.ico")


@web_server.errorhandler(404)
def handler_404(error):
    return make_response(r'page not found <br> redirecting to homepage<script>setTimeout(()=>{window.location="/"},1000)</script>', 404)


@web_server.errorhandler(500)
def handler_500(error):
    return make_response(r'An error occured, please try again later <br> redirecting to homepage<script>setTimeout(()=>{window.location="/"},1000)</script>', 500)


@web_server.route('/agg/', methods=['GET'])
def visualize_list():
    init_data()
    return {'list': visualizer_list}


@web_server.route('/agg/<id>', methods=['GET'])
def visualize_image(id):
    init_data()
    if not id in visualizer_list:
        return make_response('Error: the id of the resource is not found', 500)
    redis_connection = redis.Redis(connection_pool=redis_pool)
    
    # For details, see visualizer.py
    # Make a response to output raw svg directly
    '''
        data = json.loads(redis_connection.get('flights').decode())
        response = make_response(visualizer.visualizerList[id](data).output())
        response.headers['Content-Type'] = 'image/svg+xml'
        return response
    '''

    # Return Data URI
    return {
        'image': redis_connection.get(id).decode()
        #visualizer.visualizerList[id](data).output()
    }


@web_server.route('/proxy/', methods=['POST'])
def proxy():
    '''
        This is the proxy for cross site requests from client, 
        please merge it to the final version.
    '''
    client_json = request.get_json()
    url = client_json['_url']
    del client_json['_url']
    method = client_json['_method']
    del client_json['_method']
    if method == 'GET':
        response = requests.get(url, params=client_json)
    elif method == 'POST':
        response = requests.post(url, data=client_json)
    else:
        return make_response('error', 500)
    #print(response.text)
    return response.text

# helper function. simply skip the actions when None is returned.


def smart_fetch(rc, key, *actions):
    data = rc.get(key)
    if data is None:
        return None
    for y in actions:
        data = y(data)
    return data


@web_server.route('/flights/', methods=['GET'])
def query_flights():
    try:
        rc = redis.Redis(connection_pool=redis_pool)
        fl = json.loads(rc.get('flights').decode())
        upd = int(rc.get('flights-upd').decode())
        return jsonify({'flights': fl, 'flights-upd': upd})
    except Exception as e:
        traceback.print_exc()
        return make_response({'error': str(e)}, 500)


@web_server.route('/agg/last-render-timestamp/', methods=['GET'])
def query_render_upd():
    try:
        rc = redis.Redis(connection_pool=redis_pool)
        upd = int(rc.get('render-upd').decode())
        return jsonify({'render-upd': upd})
    except Exception as e:
        traceback.print_exc()
        return make_response({'error': str(e)}, 500)


@web_server.route('/crawler/', methods=['GET', 'POST'])
def crawler_controller():
    try:
        rc = redis.Redis(connection_pool=redis_pool)
        if request.method == 'GET':  # TODO: use pipeline+watch transaction to avoid data race
            current_range = eval(rc.get('range').decode())
            crawler_status = {
                'token-life': int(rc.get('token-life').decode()),
                'token-upd': int(rc.get('token-upd').decode()),
                'interval': int(rc.get('fetch-interval').decode()),
                'range': {
                    'center_lat': float(current_range[0]),
                    'center_lon': float(current_range[1]),
                    'corner_lat': float(current_range[2]),
                    'corner_lon': float(current_range[3]),
                },
                'token': rc.get('token').decode()
            }
            return jsonify(crawler_status)
        else:  # TODO: data validation
            data = request.json
            web_server.logger.info('changing crawler status {}'.format(data))
            if data.get('token-life') is not None:
                new_token_life = int(data.get('token-life'))
                if new_token_life < 30:
                    raise Exception(
                        'invalid crawler status change request: token-life <30')
                rc.publish('control-token-life', str(new_token_life))
            if data.get('token-refresh') is not None:
                rc.publish('control-token-refresh', ' ')
            if data.get('interval') is not None:
                new_interval = int(data.get('interval'))
                if new_interval < 10:
                    raise Exception(
                        'invalid crawler status change request: fetch-interval <10')
                rc.publish('control-fetch-interval', str(new_interval))
            if data.get('range') is not None:
                new_range = data.get('range')
                web_server.logger.info('change range to {}'.format(new_range))
                ct_lat, ct_lon = float(new_range['center_lat']), float(
                    new_range['center_lon'])
                lu_lat, lu_lon = float(new_range['corner_lat']), float(
                    new_range['corner_lon'])
                rc.publish('control-range',
                           str((ct_lat, ct_lon, lu_lat, lu_lon)))
            return make_response('', 200)
    except Exception as e:
        traceback.print_exc()
        return make_response({'error': str(e)}, 500)


@web_server.route('/led/', methods=['GET', 'POST'])
def led_controller():
    try:
        rc = redis.Redis(connection_pool=redis_pool)
        if request.method == 'GET':  # TODO: use pipeline+watch transaction to avoid data race
            led_status = {
                'interval': int(rc.get('led-interval').decode()),
                'active': int(rc.get('led-active').decode()),
                'base': int(rc.get('led-base').decode()),
                'mode': int(rc.get('led-mode').decode())
            }
            return jsonify(led_status)
        else:
            data = request.json
            web_server.logger.info('changing LED status {}'.format(data))
            if data.get('interval') is not None:
                new_interval = int(data.get('interval'))
                rc.publish('control-led-interval', str(new_interval))
            if data.get('active') is not None:
                new_act = int(data.get('active'))
                rc.publish('control-led-active', str(new_act))
            if data.get('base') is not None:
                new_base = int(data.get('base'))
                rc.publish('control-led-base', str(new_base))
            if data.get('mode') is not None:
                new_mode = int(data.get('mode'))
                rc.publish('control-led-mode', str(new_mode))
            return make_response('', 200)
    except Exception as e:
        traceback.print_exc()
        return make_response({'error': str(e)}, 500)

@web_server.route('/form-demo/',methods=['GET','POST'])
def form_demo():
    try:
        if request.method == 'GET':
            rc = redis.Redis(connection_pool=redis_pool)
            return render_template('try-form.html',flights=json.loads(rc.get('flights')))
        else:
            f = request.form
            light_mode = str(f.get('led-mode','normal')).lower()
            apt = str(f.get('airport','PuDong')).lower()
            msg = None
            if light_mode == 'normal':
                web_server.logger.info('changing led mode to normal(0)')
            elif light_mode == 'blink':
                web_server.logger.info('changing led mode to blink(0)')
            else:
                msg = json.dumps({'error': 'unsupported mode'})
            if apt!='nmsl':
                web_server.logger.info(f'changing focus to {apt}airport')
            else:
                msg = json.dumps({'error': 'mind your words'})
            return render_template('try-form.html',msg=msg)
    except Exception as e:
        traceback.print_exc()
        return make_response({'error': str(e)}, 500)


if __name__ == "__main__":
    web_server.run(host="localhost", port=8999, debug=True)
