#@author:九世
#@time:2019/8/7
#@file:http_agent

import socket
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(thread)d %(threadName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',datefmt='%a, %d %b %Y %H:%M:%S',filename='demo.py',filemode='a')
import re

class Agent:
    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.request=[]

    def http(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((self.host,self.port))
        s.listen(1)
        while True:
            while True:
                abt, ht = s.accept()
                rec=abt.recv(1024)
                if b'\r\n\r\n' in rec:
                    self.request.append(rec)
                    break

            rg=bytes(self.request[0]).decode('utf-8')
            host=str(re.findall('Host: .*',str(rg))[0]).replace('Host:','').replace('\r','')
            if ':' in host:
                hosts=str(re.findall('.*:',host)[0]).replace(':','').replace('\n','').lstrip()
                port=int(str(re.findall(':.*',host)[0]).replace(':',''))
            else:
                hosts = str(re.findall('Host: .*', str(rg))[0]).replace('Host:', '').replace('\r', '').replace('\n','').lstrip()
                port=80

            print('request:{}:{}'.format(hosts,port))

            rqt=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            rqt.connect((hosts,port))
            rqt.sendall(self.request[0])
            calc=0
            content_length=''
            recvs = b''
            while True:
                if calc>1:
                    if len(recvs)>=int(content_length):
                        abt.sendall(recvs)
                        break
                    else:
                        print('Content-length:{} recvs:{}'.format(content_length,len(recvs)))

                recvs+=rqt.recv(1024)
                if calc==1:
                    length=re.findall('Content-Length: [0-9]{1,}',bytes.decode(recvs,encoding='utf-8'))
                    content_length+=str(length[0]).replace('Content-Length:','').replace(' ','').lstrip()

                calc+=1

if __name__ == '__main__':
    obj=Agent(host='0.0.0.0',port=4444)
    obj.http()