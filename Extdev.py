import urllib2
from datetime import datetime
from Measurement import Measurement

class Extdev(Measurement):

 def __init__(self, place, color):
  Measurement.__init__(self, place, color)

 def read(self,starttime,endtime):
#   print "Read Laru"
   self.aika = []
   self.kulma = []
   self.nopeus = []
   
   dnow = datetime.now()
   response = urllib2.urlopen('http://dlarah.org/wind_data/Laru_'+dnow.strftime("%Y-%-j")+'.txt')

   for line in response:
      sp = line.rstrip().split(",")
      dat = datetime(int(sp[0]), int(sp[1]), int(sp[2]), int(sp[3]), int(sp[4]), 0, 0)
      if dat > starttime:
         self.aika.append(dat)
         self.kulma.append(int(float(sp[6])))
         self.nopeus.append(float(sp[8]))
