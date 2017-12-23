
import sys, winsound, time
import re
import sqlite3

soundFile="C:\\Users\\bing\\Downloads\\railway.wav" #只接受WAV文件
sleeptime=0 #设置延时



print("正在监听键盘，请勿动.......")


def playmusic():
	time.sleep(sleeptime)
	winsound.PlaySound(soundFile, winsound.SND_ASYNC) 

pattern=r'\d{3}\w\d\w{2}\d{8}' #检验冷媒码
while True:
	s=str(sys.stdin.readline()).strip("\n")
	
	if len(s)>10: playmusic()
