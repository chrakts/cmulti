#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

class sendInterface(serial.Serial):
  def __init__(self,comPort,baudRate ):
    super(serial.Serial,self).__init__( port=comPort, baudrate=baudRate ) 
    print("sendInterface "+comPort+" "+str(baudRate))
  def send(self,priority,text):
    return(("#"+priority+text+"\r\n").encode('utf-8'))
  
