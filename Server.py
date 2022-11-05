#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 21:54:35 2019

@author: jason
"""
import math
import time
import numpy as np
from operator import itemgetter
from sklearn.preprocessing import normalize
class objects:
    def __init__ (self, x, y, z, file):
        self.position=np.array([x, y, z],dtype='float32')
        self.soundfile=file
class help_fun:
    def distance(self, obj, hedge):
        thread_switcher_array=np.zeros((len(obj)))
        if isinstance(obj, list):
            dis=[0]*len(obj) # define the distance array between objects and hedge
            for i in range (len(obj)):
                dis[i]=math.sqrt((obj[i][0]-hedge[0])**2+(obj[i][1]-hedge[1])**2+(obj[i][2]-hedge[2])**2)
            sorted_dis_index, dis_sorted=zip(*sorted(enumerate(dis), key=itemgetter(1), reverse=False))
            thread_switcher_array[sorted_dis_index[0]]=1
            if len(obj)>1:
                thread_switcher_array[sorted_dis_index[1]]=1
        #    print(sorted_dis_index)
        #    print(dis_sorted)
            if len(obj)==1:
                return sorted_dis_index[0], dis_sorted[0]
            if len(obj)>1:
                return thread_switcher_array, dis_sorted, sorted_dis_index
        elif isinstance(obj,np.ndarray):
             dis=math.sqrt((obj[0]-hedge[0])**2+(obj[1]-hedge[1])**2+(obj[2]-hedge[2])**2)
             return dis
            
            
    def paired_position(self, hedge_pos1, hedge_pos2):
        if isinstance(hedge_pos1, np.ndarray):
            hedge_pos1=hedge_pos1
        elif isinstance(hedge_pos1, list):
            hedge_pos1=np.asarray(hedge_pos1)
        if isinstance(hedge_pos2, np.ndarray):
            hedge_pos2=hedge_pos2
        elif isinstance(hedge_pos2, list):
            hedge_pos2=np.asarray(hedge_pos2)
        hedge_position = np.hstack((hedge_pos1, hedge_pos2))
        return hedge_position
        
    def qMult(self,q1, q2):
        if isinstance(q1, np.ndarray):
            q1=q1
        elif isinstance(q1, list):
            q1=np.asarray(q1)
        if isinstance(q2, np.ndarray):
            q2=q2
        elif isinstance(q2, list):
            q1=np.asarray(q2)
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2
        w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
        x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
        y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
        z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
        return [w, x, y, z]
    
    def qConjugate(self,q):
        if isinstance(q, np.ndarray):
            q=q
        elif isinstance(q, list):
            q=np.asarray(q)
        w, x, y, z = q
        return (w, -x, -y, -z)
    
    def quaternionRotate(self, q1, v1):
        if isinstance(q1, np.ndarray):
            q1=q1
        elif isinstance(q1, list):
            q1=np.asarray(q1)
            
        if isinstance(v1, np.ndarray):
            v1=v1
        elif isinstance(v1, list):
            v1=np.asarray(v1)
            
        q2 = np.append([0], v1)
        return self.qMult(self.qMult(q1, q2), self.qConjugate(q1))[1:]
    
    def quaternionToEulerianAngle(self,q):
        if isinstance(q, np.ndarray):
            q=q
        elif isinstance(q, list):
            q=np.asarray(q)
        w, x, y, z = q
        ysqr = y*y
        
        t0 = +2.0 * (w * x + y*z)
        t1 = +1.0 - 2.0 * (x*x + ysqr)
        X = math.degrees(math.atan2(t0, t1))
        
        t2 = +2.0 * (w*y - z*x)
        t2 =  1 if t2 > 1 else t2
        t2 = -1 if t2 < -1 else t2
        Y = math.degrees(math.asin(t2))
        
        t3 = +2.0 * (w * z + x*y)
        t4 = +1.0 - 2.0 * (ysqr + z*z)
        Z = math.degrees(math.atan2(t3, t4))
        
        return X, Y, Z 
    def y_hedge_axis_Angle_z(self,Angle_z):
        
        new_y=np.array([-math.sin(math.radians(Angle_z)),math.cos(math.radians(Angle_z)),0])
        return new_y
    def y_hedge_axis(self, hedge_pos1, hedge_pos2):
        if isinstance(hedge_pos1, np.ndarray):
            hedge_pos1=hedge_pos1
        elif isinstance(hedge_pos1, list):
            hedge_pos1=np.asarray(hedge_pos1)
        if isinstance(hedge_pos2, np.ndarray):
            hedge_pos2=hedge_pos2
        elif isinstance(hedge_pos2, list):
            hedge_pos2=np.asarray(hedge_pos2)
#            print(hedge_position)
#            col = len(hedge_position)
#            row = np.shape(hedge_position)
#            print(row)
        left_pos = hedge_pos1
        right_pos= hedge_pos2
        zero_dot = (right_pos-left_pos)/2+left_pos
        x_dot = normalize((right_pos-zero_dot).reshape(-1,1),axis=0)
#        print('x_dot:', x_dot)
        rot_mat = np.array([[0,-math.sin(math.pi/2),0],
                          [math.sin(math.pi/2),0,0],
                          [0,0,1]],dtype='float32')
        y_dot = (np.matmul(rot_mat,x_dot).T).flatten()
        
        return y_dot, zero_dot
    def vectorMult(self,v1,v2):
        if isinstance(v1, np.ndarray):
            v1=v1
        elif isinstance(v1, list):
            v1=np.asarray(v1)
        if isinstance(v2, np.ndarray):
            v2=v2
        elif isinstance(v2, list):
            v2=np.asarray(v2)
        x1, y1, z1 = v1
        x2, y2, z2 = v2
        
        return x1 * x2 + y1 * y2 + z1 * z2
    
    def vector_len(self,v):
        if isinstance(v, np.ndarray):
            v=v
        elif isinstance(v, list):
            v=np.asarray(v)
        x, y, z = v
        return math.sqrt(x * x + y * y + z * z)
        
    
    def calculateAzimuths_qua(self, v): #surpose y axis is the face front 
        if isinstance(v, np.ndarray):
            v=v
        elif isinstance(v, list):
            v=np.asarray(v)

        return math.ceil(math.degrees(math.atan2(v[1],v[0])))
#
##        return -math.degrees(math.atan2(v[0],v[1]))
        
    def calculateAzimuths_pos(self, v1, v2): #surpose y axis is the face front 
        if isinstance(v1, np.ndarray):
            v1=v1
        elif isinstance(v1, list):
            v1=np.asarray(v1)
        if isinstance(v2, np.ndarray):
            v2=v2
        elif isinstance(v2, list):
            v2=np.asarray(v2)
        x1, y1, z1 = v1
        x2, y2, z2 = v2
        return math.floor(-math.degrees(math.atan2(x1*y2-y1*x2,x1*x2+y1*y2)))

#        return -math.degrees(math.atan2(v[0],v[1]))

    
    def HRTF_Interpolation(self, azimuths, azimuths_body, HRTF_data):
    #    azimuths_body=calculateAzimuths(vb)
        if azimuths_body<0:
            aIndex=0
        else:
            aIndex=math.floor(len(azimuths)/2)-1
            
        while azimuths_body>=azimuths[aIndex]:
            aIndex +=1
            if aIndex > len(azimuths)-1: 
                aIndex=aIndex-1
                break
        aIndex_low = aIndex-1
        aIndex_up = aIndex
        

        left_low = np.squeeze(HRTF_data['hrir_l'][aIndex_low, :])  # 200*1
        right_low = np.squeeze(HRTF_data['hrir_r'][aIndex_low, :])  # 200*1
        left_up = np.squeeze(HRTF_data['hrir_l'][aIndex_up, :])  # 200*1
        right_up = np.squeeze(HRTF_data['hrir_r'][aIndex_up, :])  # 200*1

        
        if azimuths_body<= azimuths[0]: #calculate lamda and decide boundary value
            lamda=0
        elif azimuths_body>= azimuths[len(azimuths)-1]:
            lamda=1
        else:
            lamda=(azimuths_body-azimuths[aIndex_low])/(azimuths[aIndex_up]-azimuths[aIndex_low])
        left_inter=(1-lamda)*left_low+lamda*left_up    
        right_inter=(1-lamda)*right_low+lamda*right_up

        
        return left_inter, right_inter

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

hp_fun=help_fun()
x_out= np.array([0,0,0,0,0,0])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        time.sleep(0.2)
        try:
            x_out[0] += 1
            x_out[1] += 1
            hedge_iner_posi=hp_fun.y_hedge_axis(x_out[0:3],x_out[3:6])[1]
            s.send(str(hedge_iner_posi).encode('utf-8'))
            print(f"Send {str(hedge_iner_posi)!r}")
        except OSError:
            s.close()
            print('Unable to send Beacon data to GUI')
            break
        



