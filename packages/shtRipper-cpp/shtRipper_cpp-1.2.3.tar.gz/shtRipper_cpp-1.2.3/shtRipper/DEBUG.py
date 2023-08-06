import shtRipper_entry
ripper = shtRipper_entry.Ripper()

import time
import json

filename = 'd:/data/cfm/original/sht40808.SHT'


start_time = time.time()
for iteration in range(1):
    pass
    #res = ripper.read(filename)
    #print('yeah')
print("--- %.2f seconds ---" % (time.time() - start_time))

shotn = 40974
path = 'D:/tmp/'
poly = 9


with open('%s%d.json' % (path, shotn), 'r') as file:
    data = json.load(file)
    x = []
    T_c = []
    n_c = []
    for event in data['events']:
        if 'T_e' in event and 'T' in event['T_e'][poly]:
            x.append(event['timestamp'] * 1e-3)
            T_c.append(event['T_e'][poly]['T'])
            n_c.append(event['T_e'][poly]['n'])

path = 'D:/tmp/'
to_pack = {
    'central Te': {
        'comment': 'Температура в центре',
        'unit': 'T_e(eV)',
        'timestamp': time.time(),  # not required
        'x': x,
        'y': T_c
    },
    'signal 2': {
        'comment': 'Температура в центре',
        'unit': 'T_e(eV)',
        'x': x,
        'y': T_c
    }
}

packed = ripper.write(path=path, filename='TS_%d.SHT' % shotn, data=to_pack)
if len(packed) != 0:
    print('packed error = "%s"' % packed)


#filename = 'd:/tmp/TS.SHT'
#res = ripper.read(filename)

for i in range(50000000):  # wait for possible errors in dll
    d = 56784678 / 5423621543

print('OK.')