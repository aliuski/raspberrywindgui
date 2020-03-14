import requests
from datetime import datetime
from Measurement import Measurement

class Extdev(Measurement):
 def __init__(self, place, color, id_station, password):
  Measurement.__init__(self, place, color)
  self.id_station = id_station
  self.password = password

 def read(self,starttime,endtime):
#   print "Read Laru"
   self.aika = []
   self.nopeus = []
   response = requests.get('https://www.windguru.cz/int/wgsapi.php?id_station='+self.id_station+'&password='+self.password+'&q=station_data_last&hours=3&avg_minutes=5&vars=wind_avg,wind_direction')
   data=response.json()
   for ut in data['unixtime']:
      self.aika.append(datetime.fromtimestamp(ut))
   self.kulma = data['wind_direction']
   for wa in data['wind_avg']:
      self.nopeus.append(int(wa * 5.144 + 0.5) / 10.0)
