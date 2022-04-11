from bs4 import BeautifulSoup
import json

l = []
head = {
    0 : 'IATA',
    1 : 'ICAO',
    2 : 'Airport name',
    3 : 'Location served',
    4 : 'Time',
    5 : 'DST'
}
for i in range(0, 26):
    letter = chr(ord('A')+i)
    with open('raw_data/List of airports by IATA airport code_ {} - Wikipedia.html'.format(letter)) as f:
        soup = BeautifulSoup(f.read())
    for tr in soup.find_all('tr'):
        cur = {}
        j = 0
        for td in tr.find_all('td'):
            cur[head[j]] = td.text.strip()
            j += 1
        if cur != {}: l.append(cur)
g = open('out.json', 'w')
g.write(json.dumps(l))
g.close()