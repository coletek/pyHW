import random

class SimpleVoltageMonitor:

  # dynamic variables
  
  is_debug = False
  is_simulator = False

  vref = -1.0
  percentage = 0.0
  
  def __init__(self, is_debug = False, vref = -1.0):
    self.is_debug = is_debug
    self.vref = vref
    
    self.is_simulator = True # todo
    
  def tick(self):
    if self.is_simulator:
      self.precentage = random.randrange(0, 100, 1) # todo
