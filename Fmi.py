import time
import urllib2
from xml.dom import minidom
from datetime import datetime, timedelta
from Measurement import Measurement

class Fmi(Measurement):

 def __init__(self, place, color, fmisid):
  Measurement.__init__(self, place, color)
  self.fmisid = fmisid

 def parametrit(self, itemlist):
  itemlist2 = itemlist.getElementsByTagName('omso:PointTimeSeriesObservation')
  itemlist3 = itemlist2[0].getElementsByTagName("om:result")
  itemlist4 = itemlist3[0].getElementsByTagName("wml2:MeasurementTimeseries")
  return itemlist4[0].getElementsByTagName("wml2:point")

 def read(self,starttime,endtime):
#  print "fmisid", self.fmisid
  self.aika = []
  self.kulma = []
  self.nopeus = []
  td = timedelta(hours=3)
  gmdstarttime = starttime - td
  gmdendtime = endtime - td
  xmldoc = minidom.parse(urllib2.urlopen('http://opendata.fmi.fi/wfs?request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&fmisid='+self.fmisid+'&starttime='+gmdstarttime.strftime('%Y-%m-%dT%H:%M:%SZ')+'&endtime='+gmdendtime.strftime('%Y-%m-%dT%H:%M:%SZ')+'&parameters=windspeedms,WindDirection'))
  itemlist = xmldoc.getElementsByTagName('wfs:member')
  itemlist5 = self.parametrit(itemlist[1])

  for s in itemlist5:
   itemlist6 = s.getElementsByTagName("wml2:MeasurementTVP")
   itemlist7 = itemlist6[0].getElementsByTagName("wml2:time")[0]
   self.aika.append(datetime.strptime(itemlist7.childNodes[0].data, '%Y-%m-%dT%H:%M:%SZ') + td)

  for s in itemlist5:
   itemlist6 = s.getElementsByTagName("wml2:MeasurementTVP")
   itemlist8 = itemlist6[0].getElementsByTagName("wml2:value")[0]
   self.kulma.append(int(float(itemlist8.childNodes[0].data)))

   itemlist5 = self.parametrit(itemlist[0])

  for s in itemlist5:
   itemlist6 = s.getElementsByTagName("wml2:MeasurementTVP")
   itemlist8 = itemlist6[0].getElementsByTagName("wml2:value")[0]
   self.nopeus.append(float(itemlist8.childNodes[0].data))
