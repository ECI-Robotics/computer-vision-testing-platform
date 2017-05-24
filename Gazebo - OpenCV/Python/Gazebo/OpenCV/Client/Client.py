# -*- coding: utf-8 -*-
import requests
import urllib
from concurrent.futures._base import wait


class conect():


    def conectar(self, host, nombre_robot, nombreCamara=None,nombreSensor=None, wheelR=None,wheelL=None):
        self.datos = {}
        self.host=host
        if(nombreCamara!=None):
            self.datos["name_robot"]=nombre_robot
            self.datos["name_camera"]=nombreCamara
            self.datos["name_camera_sensor"]=nombreSensor
        else:
            self.datos["name_robot"]=nombre_robot
            self.datos["name_right_wheels"]=wheelR
            self.datos["name_left_wheels"]=wheelL
        try:
            return requests.post(self.host, json=self.datos)
        except:
            return "No se puede conectar a %s" % (self.host)

    def __init__(self):
        self.urlI = "http://127.0.0.1:8081/NameCamera"
        self.conectar(host=self.urlI, nombre_robot="my_robot",nombreCamara="camera",nombreSensor="camera")
        self.urlM="http://127.0.0.1:8080/NameMovement"
        self.wheelR=["right_wheel_hinger","right_wheel_hingerA"]
        self.wheelL=["left_wheel_hinger","left_wheel_hingerA"]
        self.conectar(host=self.urlM, nombre_robot="my_robot", wheelL=self.wheelL, wheelR=self.wheelR)



        """variables = raw_input("Inserta las variables, separadas por ':' ::> ")
        valores = raw_input("Inserta los valores, separados por ':' ::> ")
        conecta=conect()"""

    def conectarVideo(self):
        self.image = urllib.urlopen('http://127.0.0.1:8081/video.mjpg')


    def getVideo(self):
        return self.image.read(1024)

    def setMove(self,valores):
        #print(valores)
        self.host="http://127.0.0.1:8080/Instruction"
        self.datos={"Instruction":valores}
        requests.post(self.host, json=self.datos)
