
# Android QPython 3

# yus 20150912

import android, time
from http.client import HTTPConnection

droid = android.Android()
droid.startSensingTimed(1, 250)
try:
    conn = HTTPConnection('192.168.0.100',8080)
    conn.connect()
    time.sleep(2.0)
    while True:
        time.sleep(0.1)
        #s = droid.readSensors().result
        s = droid.sensorsReadOrientation().result
        #p = ','.join(map(str,s))
        p = '%.7f,%.7f,%.7f'%(s[0],s[1],s[2])
        conn.request('GET', p)
        print(p)
        resp = conn.getresponse().read()
        #print(resp)
except:
    pass
finally:
    conn.close()
droid.stopSensing()
