import json
with open('IATA data.json', 'r') as f:
    data = json.loads(f.read())
output = {}
t = {}
for i in data:
    try:
        t = i
        j = t['Location served']
        t['Location served'] = [k.strip() for k in j.split(',')]
    except:
        pass
    else:
        output[t['IATA']] = t
with open('IATA data fix.json', 'w') as g:
    g.write(json.dumps(output))
