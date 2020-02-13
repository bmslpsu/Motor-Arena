from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
import time

class EncoderRead:
	def __init__(self):
		self.countprev = 2797
		self.totcount = 0

	def printposition(self, positionChange, timeChange, indexTriggered,extra):
		print("PositionChange: " + str(self.totcount))
		print("TimeChange: " + str(timeChange))
		print("IndexTriggered: " + str(indexTriggered))
		print("----------")
		self.totcount = self.encoder0.getPosition()
		
		
	
	def run(self):
		self.encoder0 = Encoder()
		#self.dcMotor0 = DCMotor()
		
		self.encoder0.setOnPositionChangeHandler(self.printposition)
		
		self.encoder0.openWaitForAttachment(5000)
		#self.dcMotor0.openWaitForAttachment(5000)
		
		#self.dcMotor0.setTargetVelocity(0.1)
		
		
		try:
			input("Press Enter to Stop\n")
		except (Exception, KeyboardInterrupt):
			pass
	
		self.encoder0.close()
		#self.dcMotor0.close()
		
if __name__ == '__main__':
	main = EncoderRead()
	main.run()
	
	
	