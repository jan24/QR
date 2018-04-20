#coding=utf-8

import threading
import QR
import webserver

def loop1():
    QR.scan()
def loop2():
    webserver.app.run()

t1= threading.Thread(target=loop1, name='scan')
t2= threading.Thread(target=loop2, name='WebUI')

t1.start()
t2.start()

t1.join()
t2.join()
