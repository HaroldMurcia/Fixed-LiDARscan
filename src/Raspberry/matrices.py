import numpy as np
import math
def rconstr (n,pitch,r,yaw):
	r=float(r)
	phi=(n*240/725)-120
	ex=-0.05
	ey=-0.05
	ez=-0.05
	pitch=math.radians(pitch)
	epit=0.0408
	eyaw=0.1492
	eroll=-0.0281
	x=r*math.sin(math.radians(phi))
	y=r*math.cos(math.radians(phi))
	z=x*0
	ang=math.radians(yaw)
	cart=np.array([[x],[y],[z],[1]])
	T0=np.array([[1,0,0,ex],[0,1,0,ey],[0,0,1,ez],[0,0,0,1]])
	T1=np.array([[1,0,0,0],[0,math.cos(epit),-1*math.sin(epit),0],[0,math.sin(epit),math.cos(epit),0],[0,0,0,1]])
	T2=np.array([[math.cos(eroll),0,math.sin(eroll),0],[0,1,0,0],[-1*math.sin(eroll),0,math.cos(eroll),0],[0,0,0,1]])
	T3=np.array([[math.cos(eyaw),-1*math.sin(eyaw),0,0],[math.sin(eyaw),math.cos(eyaw),0,0],[0,0,1,0],[0,0,0,1]])
	T4=np.array([[1,0,0,0],[0,math.cos(pitch),-1*math.sin(pitch),0],[0,math.sin(pitch),math.cos(pitch),0],[0,0,0,1]])
        rot=np.array([[math.cos(ang),-1*math.sin(ang),0,0],[math.sin(ang),math.cos(ang),0,0],[0,0,1,0],[0,0,0,1]])

	T43=np.dot(T4,T3)
	T32=np.dot(T43,T2)
	T21=np.dot(T32,T1)
	T10=np.dot(T21,T0)
	T01=np.dot(T10,cart)
	output=np.dot(rot,T01)

	return output
