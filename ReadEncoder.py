from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID
import time

class EncoderRead:
	def __init__(self):
		self.countprev = 700.8
		self.totcount = 0
		self.inivelocity = 0.5
		self.pid = PID(0.001, 0, 0.00022, setpoint=700)

	def setup(self):
		self.encoder0 = Encoder()
		self.dcMotor0 = DCMotor()
		

		self.encoder0.openWaitForAttachment(5000)
		self.dcMotor0.openWaitForAttachment(5000)
		self.dcMotor0.setTargetVelocity(self.inivelocity)
		
		self.encoder0.setOnPositionChangeHandler(self.printposition)
		

		try:
			input("Press Enter to Stop\n")
		except (Exception, KeyboardInterrupt):
			pass
	
		self.encoder0.close()
		self.dcMotor0.close()
	
	def printposition(self,positionChange, timeChange, indexTriggered, extra):
		self.encoderread()
		print("PositionChange: " + str(self.totcount))
		print("TimeChange: " + str(self.control))
		print("----------")
		
	def spiningmotor(self):
		self.PIDposition(self.totcount)
		self.dcMotor0.setTargetVelocity(self.control)
	
	def	encoderread(self):
		self.totcount=self.encoder0.getPosition()
		self.spiningmotor()
		
	def PIDposition(self,v):
		self.control = self.pid(v)
		
	
		
		
if __name__ == '__main__':
	main = EncoderRead()
	main.setup()
	
	
	