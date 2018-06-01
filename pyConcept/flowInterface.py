#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib as il
import dataInterface

il.reload(dataInterface)

class flowInterface(dataInterface.dataInterface):
  def __init__(self,source ):
    super(dataInterface.dataInterface,self).__init__( ) 
    self.source = source
  def flow(self,destination,data):
    return(self.source+destination+data)
