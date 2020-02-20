from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID
import time
import csv

class EncoderRead:
	def __init__(self):
		self.cpr = 700.8				#	Number of count per Revolution of Encoder
		self.totcount = 0				#	Position Counter
		self.iniVelocity = 0.1			#	initial velocity
		
	def setup(self):
		self.encoder0 = Encoder()
		self.dcMotor0 = DCMotor()
		
		self.readcsv()

		self.encoder0.openWaitForAttachment(5000)
		self.dcMotor0.openWaitForAttachment(5000)
		self.dcMotor0.setTargetVelocity(self.iniVelocity)
		
		self.encoder0.setOnPositionChangeHandler(self.positionControl)
		

		try:
			input("Press Enter to Stop\n")
		except (Exception, KeyboardInterrupt):
			pass
	
		self.encoder0.close()
		self.dcMotor0.close()
	
		
	def positionControl(self):
		self.encoderread()
		self.degToCount()

	def	encoderread(self):
		self.totcount=self.encoder0.getPosition()
		
	def PIDposition(self,position):
		pid = PID(0.001, 0, 0.00022, setpoint=position)
		velocity = pid(position)
		if 1 < velocity:
			velocity = 1
		elif 0 > velocity:
			velocity = 0
		return velocity
		
	def degToCount(self):
		angle = self.readcsv()
		self.targetCount = [0] * len(angle)
		for ii in range(0, len(angle)):
			self.targetCount[ii]=int(angle[ii]*self.cpr/360)
		print()
		
		
		
	def readcsv(self):
		with open('CVStesting.csv') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			row = list(reader)
			Angle=[0.0] * len(row)
			for ii in range(0, len(row)):
				for x in row[ii]:
					Angle[ii]=float(x)
		return Angle
		
			

		
		
if __name__ == '__main__':
	main = EncoderRead()
	main.readcsv()
	main.degToCount()



	