#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib as il

import dataInterface as di
import flowInterface as fi
import transInterface as ti
import sendInterface as si
from PyCRC.CRCCCITT import CRCCCITT

il.reload(di)
il.reload(fi)
il.reload(ti)
il.reload(si)

CRC = 4

def interprete(data):
  data = data.decode("utf-8")
  if data[0]=="#" and data[-2:]=="\r\n":
    num = int(tdata[2:4],16)
    coreData = data[4:-2]
    if len(coreData.encode('utf-8')) == num:
      if ord(coreData[0]) & CRC:
        crc = CRCCCITT().calculate(data[2:-7])
        if crc == int(data[-6:-2],16):
          print (coreData)
        else:
          print("CRC nicht in Ordnung")
    else:
      print("Datenlänge passt nicht")
  else:
    print("Anfangs- oder Endekennung fehlerhaft")
    

iface = si.sendInterface("/dev/ttyUSB0",19200)
test2 = fi.flowInterface("Qb")
tr = ti.transInterface(encryption=True,crc=True)

print(iface.send("P",tr.transport(test2.flow("FS",test2.sendCommand('F','j',"Kommando")))))
print(iface.send("P",tr.transport(test2.flow("FS",test2.sendCommand('F','j',45.65)))))
tdata = iface.send("P",tr.transport(test2.flow("FS",test2.sendInfo('Information'))))
print(tdata)
interprete(tdata)


