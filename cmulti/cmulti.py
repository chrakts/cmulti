import time
from PyCRC.CRCCCITT import CRCCCITT

class cmulti_crc_constants_t(object):
    noCRC = 0
    CRC_8 = 1
    CRC_16 = 2
    CRC_32 = 3
    CRC_ccitt_1d0f = 4
    CRC_ccitt_ffff = 5
    CRC_dnp = 6
    CRC_kermit = 7
    CRC_modbus = 8
    CRC_sick = 9
    CRC_xmodem = 10

    def __init__(self):
        pass


"""


import lcm
from exlcm import cmulti_command_t
from exlcm import cmulti_answer_t
from exlcm import cmulti_crc_constants_t
from exlcm import cmulti_constants_t
"""
import argparse
import serial

class CMULTI(object):
   def __init__(self,source,comPort="", baudRate=57600, backChannel="Klima", withCrc = cmulti_crc_constants_t.noCRC, timeout=1000):
      if comPort != "":
         self.interface = serial.Serial(comPort, baudRate, timeout=3)
      else:
         self.interface = backChannel
         self.lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=1")
         self.subscription = self.lc.subscribe(backChannel,self.answer_handler)
      if withCrc==True:
         self.crc = cmulti_crc_constants_t.CRC_xmodem
      else:
         self.crc = cmulti_crc_constants_t.noCRC
      self.crc = withCrc
      self.source = source
      self.backChannel = backChannel
      self.timeout = timeout
      self.gotAnswer = False
      self.subscription = None
   
   def sendCommand(self,target,command,parameter,expectAnswer = False):
      if type(self.interface)==str:
         boolAnswer,answer = self.sendCommandServer(target,command,parameter,expectAnswer)
      else:
         boolAnswer,answer = self.sendCommandTTY(command,parameter,expectAnswer)
      return(boolAnswer,answer)
            
   def sendCommandServer(self,target,command,parameter,expectAnswer = True):
      self.msg = cmulti_command_t()
      self.msg.command = command
      self.msg.target = target
      self.msg.source = self.source
      self.msg.parameter = parameter
      
      self.msg.expect_answer = expectAnswer
      self.msg.crcType = self.crc
      self.msg.timeout_ms = int(self.timeout/3)
      self.lc.publish("CNET", self.msg.encode())
      if(expectAnswer==True):
        if(self.subscripe()==False):
          return(False,"Server-Timeout")
        else:
          if(self.msganswer.command_origin!=command):
            return(False,"Falsche Quelle !")
          else:
            if(self.msganswer.answer[-1]!='.'):
              return(False,self.msganswer.answer[:-1])
            else:
              return(True,self.msganswer.answer[:-1])
      else:
        return(True,"CNET: no answer, as expected")
     #       return(self.msganswer.error,self.msganswer.answer[:-1])
        
      
   def sendCommandTTY(self,command,parameter,expectAnswer = True):
      crcstring =  ("%04x" % (CRCCCITT().calculate(command)))  # ************************
      if self.crc != cmulti_crc_constants_t.noCRC:
         self.outputTTY("\\>"+command+"<"+crcstring+"\\")
      else:
         self.outputTTY("\\>"+command+"<\\")
      result,resultBool,resultCRC,inTime = self.input()
      return(resultBool,result)
          
   def outputTTY(self,text):
      towrite = text
      self.interface.write(towrite.encode('ascii'))
        
   def _readline(self):
      eol = b'>'
      leneol = len(eol)
      line = bytearray()
      while True:
         c =  self.interface.read(1)
         if c:
            line += c
            if line[-leneol:] == eol:
               break
         else:
            break
      return bytes(line)
     
     
   def input(self):
      inTime = True
      hello = self._readline().decode('utf-8')
      if len(hello) == 0:
         return("",False,False,False)
      crcState = True
      crcString = ""
      if hello[0] != '<':
         print("!! start character error")
      if hello[-1] != '>':
         print("!! end character error")
      if self.crc != cmulti_crc_constants_t.noCRC:
         crcString = hello[-5:-1]
         signString = hello[-6:-5]
         answerString = hello[1:-5]
         if crcString == ("%04x" % (CRCCCITT().calculate(answerString))):
            crcState = True
         else:
            crcState = False
            print("!! CRC error")
         answerString = answerString[0:-1] # das sign abtrennen
      else:
         answerString = hello[1:-2]
         signString = hello[-2:-1]
      if signString == '.':
         return(answerString,True,crcState,inTime)
      elif signString == '!':
         return(answerString,False,crcState,inTime)
      else:
         print("!! sign character error")
         return(answerString,False,crcState,inTime)

   def answer_handler(self,channel,data):
      self.msganswer = cmulti_answer_t.decode(data)
      self.gotAnswer = True
      
   def subscripe(self):
      self.gotAnswer = False
#     self.subscription = self.lc.subscribe(self.backChannel,self.answer_handler)
      try:
         while not self.gotAnswer:
            if(self.lc.handle_timeout(self.timeout )==0):
              print("CNET: Server-Timeout,eingestelltes Timeout: "+str(self.timeout ))
              return(False)
      except KeyboardInterrupt:
         pass   
      if(self.msganswer.error==0):
         print("Antwort lautet:" + self.msganswer.answer)
      else:
         print("CNET: Timeout mit Antwort:" + self.msganswer.answer)
      return(True)
   def close(self):
      if type(self.interface)!=str:
         self.interface.close()

