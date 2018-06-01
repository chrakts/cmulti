import sys, os

path = os.getcwd() 
path0 = os.path.split(path)[0] # up one directory
sys.path.append(path0)
print(path0)
from cmulti.cmulti import CMULTI

from exlcm import cmulti_command_t
from exlcm import cmulti_answer_t
from exlcm import cmulti_crc_constants_t
from exlcm import cmulti_constants_t

class Clima(CMULTI):
  def __init__(self,source,target,comPort="", baudRate=57600, backChannel="TLog", withCrc = cmulti_crc_constants_t.noCRC, timeout=5000):
    super(self.__class__,self).__init__(source,comPort , baudRate, backChannel, withCrc, timeout)
    self.target = target
    
    
  def getSerialNumber(self):
    return(self.sendCommand(self.target,"SPs?"))
    
  def getIDNumber(self):
    return(self.sendCommand(self.target,"SPi?"))

  def getIndex(self):
    return(self.sendCommand(self.target,"SPx?"))

  def setSecurityKey(self,key):
    return(self.sendCommand(self.target,"SSKT"+key)[0])

  def setSecurityKey(self,key):
    return(self.sendCommand(self.target,"SSKT"+key)[0])

  def getFreeMemory(self):
    boolAnswer,answer = self.sendCommand(self.target,"SSm?")
    if boolAnswer==True:
      return(True,int(answer))
    else:
      return(False,-1)

  def makeReset(self):
    boolAnswer,answer = self.sendCommand(self.target,"SSRTReset")
    return boolAnswer
    
  def makeBootload(self):
    boolAnswer,answer = self.sendCommand(self.target,"SSBTBootload")
    return boolAnswer
  
  def getTemperature(self):
    (boolResult,Result) = self.sendCommand(self.target,"SCt?")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getHumidity(self):
    (boolResult,Result) = self.sendCommand(self.target,"SCh?")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)

  def getAbsoluteHumidity(self):
    (boolResult,Result) = self.sendCommand(self.target,"SCa?")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getDewPoint(self):
    (boolResult,Result) = self.sendCommand(self.target,"SCd?")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getPressure(self):
    (boolResult,Result) = self.sendCommand(self.target,"SCp?")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getSealevel(self):
    (boolResult,Result) = self.sendCommand(self.target,"SCs?")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
  def getLight(self):
    (boolResult,Result) = self.sendCommand(self.target,"SCl?")
    print(Result)
    try:
      fResult = float(Result)
      return(boolResult,fResult)
    except:    
      return(False,-999.9)
  	 
test = Clima('CP','C1',withCrc=True)
print( test.getTemperature() )
print( test.getHumidity() )
print( test.getAbsoluteHumidity() )
print( test.getDewPoint() )
print( test.getPressure() )
print( test.getSealevel() )
print( test.getLight() )

