import requests
import re
#r = requests.get('https://zh.flightaware.com/live/airport/ZBAA')
r = requests.get('https://zh.flightaware.com/live/')
m = re.search('"VICINITY_TOKEN":"([^"]+)"', r.text)
print('TOKEN:', m.group(1))
