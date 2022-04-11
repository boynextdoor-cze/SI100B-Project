import json
import os
import redis

class StaticDataLoader:
    @classmethod
    def load(cls):
        r = redis.Redis(host='localhost',port=6379,db=0)
        with open(os.path.dirname(__file__)+'/airports.json', 'r') as f:
            r.set('static-airports', f.read())