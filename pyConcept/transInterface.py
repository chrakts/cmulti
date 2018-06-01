#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib as il
import flowInterface
from PyCRC.CRCCCITT import CRCCCITT


il.reload(flowInterface)

class transInterface(object):
  def __init__(self,encryption=False,connEncryption=False,crc=False ):
    self.header = 64
    self.crc = crc
    self.connEncryption = connEncryption
    self.encryption = encryption
    if crc==True:
      self.header += 4
    if connEncryption==True:
      self.header += 16
    if encryption==True:
      self.header += 2

  def transport(self,data):
    data = chr(self.header)+data
    dataLength = len(data.encode('utf-8'))
    if self.crc == True:
      dataLength += 5
    data = ("%02x"%(dataLength) ) + data
    if self.crc == True:
      data = data + ("<%04x" % (CRCCCITT().calculate(data))) 
    return(data)
