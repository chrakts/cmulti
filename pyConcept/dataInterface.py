#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib as il
import sendInterface

il.reload(sendInterface)

class dataInterface(object):
  def __init__(self):
    pass
  def sendInfo(self,text):
    return('U'+text)
  def sendCommand(self,function,job,command):
    if  type(command) == str:
      return('S'+function+job+'T'+command)
    elif type(command) == float:
      return('S'+function+job+'F'+str(command))
