import time
import pymysql
from beacontools import BeaconScanner, IBeaconFilter, IBeaconAdvertisement
import requests
import json

#conn = pymysql.connect(
#        host='192.168.0.8',
#        user='root',
#        password='autoset',
#        db='test',
#        charset='utf8' )

scannerID = "1_S004"
url = 'http://172.26.2.132:3000'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
beaconList = [15013, 15014, 15015]
def callback(bt_addr, rssi, packet, additional_info):
    global checkList
    
    #if additional_info['minor'] in checkList:
    if additional_info['minor'] in beaconList:
        print("<%s, %d>" % (bt_addr, rssi))
        print(packet)
        print(additional_info)
        sendBeaconData(additional_info['uuid'], additional_info['major'], additional_info['minor'], rssi)
        print("------------------------------------------------------------")
        #insertToDB("kalmanData", additional_info['major'], additional_info['minor'], -59, rssi)
        
def insertToDB(argUUID, argMajor, argMinor, argTx, argRSSI):
    global conn
    sql = ("insert IBeaconRSSI2 VALUES(0, '%s', %d, %d, %d, %d, now(), 1004)" % (argUUID, argMajor, argMinor, argTx, argRSSI))
    curs = conn.cursor()
    curs.execute(sql)
    conn.commit()
    #print(sql)
    
def sendBeaconData(argUUID, argMajor, argMinor, argRSSI,):
    global scannerID
    data = {'beaconData': {"scannerID":scannerID, "UUID":argUUID, "Major":argMajor, "Minor":argMinor, "RSSI":argRSSI}}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    r = requests.get(url);
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r)

def checkMyBeacon():
    global conn
    global scannerID
    checkBeaconList = []
    
    sql = ("select beacon_id_minor from test_beacons where beacon_scanner_id = '%s'" % (scannerID))
    curs = conn.cursor()
    curs.execute(sql)
    result = curs.fetchall()
    
    for value in result:
        checkBeaconList.append(value[0])
    print(checkBeaconList)
    
    return checkBeaconList
#------------------------------------------------------------------
    
# scan for all iBeacon advertisements from beacons with certain properties:
# - uuid
# - major
# - minor

print("I am getting checkList..")
#checkList = checkMyBeacon()

scanner = BeaconScanner(callback,
    packet_filter=IBeaconAdvertisement
)
scanner.start()

