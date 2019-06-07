# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 15:58:14 2018

@author: mafe Xaira Mora & Harold
"""
import serial, time
import  rospy, os, sys, time, math
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import *
from math import radians
import math
import matrices as mat
import urllib, httplib, smtplib, socket, fcntl, struct

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os.path

path_data = os.getcwd() + "/data/raw"
flag=0
flag2=0
p0=0
X = np.zeros([726,1])
cad=""
arduino = serial.Serial("/dev/ttyUSB0", 9600)
time.sleep(2)

class scan():
    global flag
    def __init__(self):
        global sub_scan
        rospy.loginfo("Starting node")
        sub_scan = rospy.Subscriber('/scan',LaserScan, self.read_data, queue_size=1)
	rospy.spin()

    def read_data(self,data):
        global flag, flag2, X, sub_scan,p0 #ciclo repetitivo desde aca...
        x = np.ones([len(data.ranges),1])
	minNPitch=float(minPitch) #convertir de string a decimal
        maxNPitch=float(maxPitch)
	yaw_lim=360-(float(res_yaw)) #establecer un limite de incremento en yaw
	if p0==0:
		msj="dec_pitch:"+str(-1*minNPitch) #
		arduino.write(msj)		   #algoritmo para llevar el sensor a la primera posicion
    		angulo=arduino.readline()	   #
		p0=1 # para ignorar las instrucciones del if en las siguientes iteraciones
        x[:,0]=data.ranges
        flag2 = flag2 +1;
        X[:,0] = X[:,0]+x[:,0] #?
        samples  = 1.0
        if flag2 == samples:
            #resolucion_motor = round(442.294*angulo);
	    msj2="inc_pitch:"+res_pitch
            arduino.write(msj2)
            ang = arduino.readline()
            pos_dp=ang.find(":") #encontrar la posicion de : en el string de entrada
	    PIT=ang[0:pos_dp] #tomar el valor de pitch
	    YA=ang[pos_dp+1:len(ang)-1] # tomar el valor de yaw
	    YA=float(YA.rstrip('/n')) # eliminar salto de linea
            print "Distancia centro: " + str(data.ranges[362])+ " en "+ang
            x[:,0]= X[:,0]/samples
            X       = np.zeros([726,1])
            flag2   = 0
            for i in range(len(data.ranges)):
                #x[i,0] = x[i,0]*data.ranges[i]
                s=str(x[i,0])
                ss=s.strip("["+"]") #elimina llaves cuadradas
                angulo=float(PIT) #convierte de string a decimal
		aux=mat.rconstr(i,angulo,ss,YA) # reconstruye los datos recibidos del LiDAR
		Xf=float(aux[0])*-1 #toma datos de coordenada en X
		Yf=float(aux[1])   #toma datos de coordenada en Y
		Zf=float(aux[2])   #toma datos de coordenada en Z
                dataLine = str(Xf)+"\t"+str(Yf)+"\t"+str(Zf)+"\n"
                f.write(dataLine)
            if angulo >= maxNPitch:
                flag=1
		p0=0 #habilitar el algoritmo de llevar a la primera posicion
		arduino.write("pitch:0") #llevar el primer motor a posicion inicial
		ang = arduino.readline()
		angulo=0
		arduino.write("inc_yaw:"+res_yaw)
                ang = arduino.readline()
		if YA >=yaw_lim:
         		arduino.write("pitch:0")
                	ang = arduino.readline()
                	arduino.write("yaw:0") #llevar el segundo motor a posicion inicial
			ang = arduino.readline()
			sub_scan.unregister()
			sendEmail(email,'escaneo Rpi','Escaneo completado satisfactoriamente...'+'\n'+'Límite Mínimo: '+min+'°'+'\n'+'Límite Máximo: '+max+'°'+'\n'+'Resolución Inclinación: '+res_pitch+'°'+'\n'+'Resolución Rotación: '+res_yaw+'°',completeName)
                	rospy.signal_shutdown("stop spin") # detener ciclo infinito rospy.spin
                	exit() #cerrar el script


def saveCloud_txt(fileName):
    global completeName
    fileName= fileName + "_" + time.strftime("%d-%m-%y")+'-'+time.strftime("%I-%M-%S")
    completeName = os.path.join(path_data, fileName + '.txt')
    f = open(completeName,"a") #opens file with name of "[fileName].txt"
    dataFile="%"+"\t"+"X"+"\t"+"Y"+"\t"+"Z"+"\n"
    f.write(dataFile)
    return f

def sendEmail(toaddr,subject,body,fileData):
    msg = MIMEMultipart()
    fromaddr='scan.rpi@gmail.com'
    msg['From']=fromaddr
    msg['To']= toaddr
    msg['Subject']=subject
    msg.attach(MIMEText(body ,'plain'))
    filename=os.path.basename(fileData)
    attachment=open (fileData,"rb")
    part=MIMEBase('application','octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename=%s"% filename)
    msg.attach(part)
    mailer= smtplib.SMTP('smtp.gmail.com',587)
    mailer.starttls()
    mailer.login(fromaddr,"raspberryscan")
    text=msg.as_string()
    mailer.sendmail(fromaddr,toaddr,text)
    mailer.quit()

if __name__ == "__main__":
    fileName =nombre = sys.argv[1]
    minPitch=sys.argv[2]
    maxPitch=sys.argv[3]
    res_pitch=sys.argv[4]
    res_yaw=sys.argv[5]
    email=sys.argv[6]
    f = saveCloud_txt(fileName)
    try:
        rospy.init_node('scanner_py')
        cv = scan()
    except rospy.ROSInterruptException:
        print "program interrupted before completion"
