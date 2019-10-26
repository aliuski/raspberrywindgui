import urllib2
import RPi.GPIO as GPIO

SH_CP = 14;
ST_CP = 15;
DS = 18;

class RaspberryPinout:

 def __init__(self):
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(SH_CP, GPIO.OUT)
  GPIO.setup(ST_CP, GPIO.OUT)
  GPIO.setup(DS, GPIO.OUT)
 
 def writeToGpio(self,nopeusms,suunta):
  nopeus = int(nopeusms * 10.0)
  a = nopeus/100
  n = nopeus - a * 100
  b = n/10
  c = n - b * 10
  d = int(round(suunta / 22.5)) & 15
  data = d + c * 16 + b * 256 + a * 4096
  d = data
  for i in range(1,17) :
   GPIO.output(DS, d&1)
   GPIO.output(SH_CP, 1)
   GPIO.output(ST_CP, 0)
   GPIO.output(SH_CP, 0)
   GPIO.output(ST_CP, 1)
   d = data >> i

 def __del__(self):
  GPIO.cleanup()
