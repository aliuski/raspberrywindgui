class Measurement:
  def __init__(self, place, color):
    self.place = place
    self.color = color

  def read(self,starttime,endtime):
    print self.place, self.color
