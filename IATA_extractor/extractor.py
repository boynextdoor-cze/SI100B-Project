from bs4 import BeautifulSoup
import json
import requests
import time

l = []
head = {
    0 : 'IATA',
    1 : 'ICAO',
    2 : 'Airport name',
    3 : 'Location served'
}
h =  {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}
for i in range(0, 26):
    letter = chr(ord('A')+i)
    response = requests.get('https://en.wikipedia.org/wiki/List_of_airports_by_IATA_airport_code:_' + letter, headers=h)
    print("{}: Server response with status code {}".format(letter, response.status_code))
    soup = BeautifulSoup(response.text)
    for tr in soup.find_all('tr'):
        cur = {}
        j = 0
        for td in tr.find_all('td'):
            cur[head[j]] = td.text.strip()
            j += 1
        l.append(cur)
    break
    time.sleep(3)
g = open('out.json', 'w')
g.write(json.dumps(l))
g.close()