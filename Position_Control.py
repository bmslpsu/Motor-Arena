from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID
import time
import csv

class Position_Control:
	def __init__(self):
		self.cpr = 324					#	Number of count per Revolution of Encoder
		self.totcount = 0				#	Position Counter
		self.iniVelocity = 0.1			#	initial velocity
		self.samplingrate = 0.01		# 	samplingrate in (second)
		self.numEncoderRead = 0
		self.timemult = pow(10,4)		# 	millisecond
		
		self.timeval0 = int(time.clock()*self.timemult)
		
	def setup(self):
		self.encoder0 = Encoder()
		self.dcMotor0 = DCMotor()
		
		self.degToCount()				# 	Load in desired position
		self.inicsv()					#	Initial data file

		self.encoder0.openWaitForAttachment(5000)
		self.dcMotor0.openWaitForAttachment(5000)
		
		self.dcMotor0.setTargetVelocity(self.iniVelocity)
		# self.encoder0.setOnPositionChangeHandler(self.positionControl)
		
		self.positionControl()

		try:
			input("Press Enter to Stop\n")
		except (Exception, KeyboardInterrupt):
			pass
	
		self.encoder0.close()
		self.dcMotor0.close()
	
		
	def positionControl(self):
		for self.ii in self.targetCount:
			self.pid = PID(0.0015, 0.0003, 0.01, setpoint= self.ii)
			error = abs(self.totcount - self.ii)
			while (self.gettime() % 30000 != 0):
				while error >= 10:
					velocity = self.PIDposition()
					self.dcMotor0.setTargetVelocity(velocity)
					error = abs(self.totcount - self.ii)
					print (error)
				self.dcMotor0.setTargetVelocity(0)

	def PIDposition(self):
		velocity = self.pid(self.encoderread())
		if 1 < velocity:
			velocity = 1
		elif -1 > velocity:
			velocity = -1
		return velocity
	
	def	encoderread(self):
		self.totcount= self.encoder0.getPosition()
		self.numEncoderRead=self.numEncoderRead+1
		self.writecsv(self.numEncoderRead,self.totcount)
		return self.totcount
	
	def degToCount(self):
		angle = self.readcsv()
		self.targetCount = [0] * len(angle)
		for ii in range(0, len(angle)):
			self.targetCount[ii]=int(angle[ii]*self.cpr/360)
		
	def readcsv(self):
		with open('CSVReading.csv') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			row = list(reader)
			Angle=[0.0] * len(row)
			for ii in range(0, len(row)):
				for x in row[ii]:
					Angle[ii]=float(x)
		return Angle
		
	def inicsv(self):
		with open('CSVWriting.csv', 'w') as file:
			self.writer = [csv.writer(file)]
			self.writer[0].writerow(["Num",'\t',"Time",'\t', "Count"])
	
	def writecsv(self,numEncoderRead,totcount):
		with open('CSVWriting.csv', 'w') as file:
			self.writer = [csv.writer(file)]*numEncoderRead
			self.writer[int(numEncoderRead)].writerow([numEncoderRead, '\t', "Time", '\t', totcount])
	
	def gettime(self):
		timeval1 = int(time.clock() * self.timemult)
		timedif = timeval1 - self.timeval0
		print(timedif)
		return timedif
		
   
		
if __name__ == '__main__':
	main = Position_Control()
	main.setup()
	



	