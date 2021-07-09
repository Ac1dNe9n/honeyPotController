import datetime
import json
import os
from pyrdp.mitm.rdp_client import *





def WriteLogFile(ip,port,starttime):
    with open('log.txt','a+',encoding="utf8") as f:
        mydict={'ip': ip, 'port': port, 'ConnectTime': starttime, 'DisconnectTime': 'Connecting...','Success2Login':'No'}
        f.write(str(mydict))
    with open('log.txt','r+',encoding="utf8") as f:
        mydict=f.read()
        mydict=mydict.replace('{',',{').replace(',','',1)
        mydict='['+mydict+']'
        mydict=mydict.replace("'", '"')
        mydict=json.loads(mydict)
        print('11111111111111111111111111111111111111111111111111111111111111')
    #发日志
    send_log()

def UpdateLogFile(endTime):
    with open('log.txt', 'r+', encoding="utf8") as f:
        mydict = f.read()
        mydict1=mydict.replace('{',',{').replace(',','',1)
        mydict1 = '[' + mydict1 + ']'
        mydict1 = mydict1.replace("'", '"')
        mydict1 = json.loads(mydict1)
        print('222222222222222222222222222222222222222222222222222222222222222222222222222222')
        mydict=mydict.replace('Connecting...',endTime)
        print("=================================================="+mydict)

    #发文件
    ConnectTime=mydict1[-1]['ConnectTime']
    ConnectTime=ConnectTime.replace('-','').replace(' ','_').replace(':','-')
    ConnectTime=ConnectTime.split(".")[0]
    print(ConnectTime)
    mydict=mydict.replace('No',check_attack(ConnectTime))
    with open('log.txt', 'w', encoding="utf8") as f:
        f.write(mydict)
    send_log_and_pyrpd_flie(ConnectTime)

if __name__ == '__main__':
    dateTime_p = datetime.datetime.now()
    WriteLogFile('12','212',str(dateTime_p))
    UpdateLogFile(str(dateTime_p ))
