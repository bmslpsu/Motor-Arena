from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID
import time
import pandas

class Position_Control:
	def __init__(self):
		self.cpr = 324					#	Number of count per Revolution of Encoder
		self.totcount = 0				#	Position Counter
		self.iniVelocity = 0.1			#	initial velocity
		self.samplingrate = 0.01		# 	samplingrate in (second)
		self.numEncoderRead = 0
		self.timemult = pow(10,3)		# 	millisecond
		
		self.timeval0 = int(time.clock()*self.timemult)

		
	def setup(self):
		self.encoder0 = Encoder()
		self.dcMotor0 = DCMotor()
		
		self.degToCount()				# 	Load in desired position
		self.inicsv()					#	Initial data file

		self.encoder0.openWaitForAttachment(5000)
		self.dcMotor0.openWaitForAttachment(5000)

		self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())
		
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
		for ii in self.targetCount:
			self.pid = PID(0.0015, 0.0003, 0.01, setpoint= ii)
			error = abs(self.totcount - ii)
			while error >= 10:
				#while (self.gettime() % 3000) != 0:
				velocity = self.PIDposition()
				self.dcMotor0.setTargetVelocity(velocity)
				self.encoderread()
				error = abs(self.totcount - ii)
				time.sleep(self.encoder0.getMinDataInterval()/pow(10,5))
			#self.dcMotor0.setTargetVelocity(0)
			time.sleep(5)

	def PIDposition(self):
		velocity = self.pid(self.totcount)
		if 1 < velocity:
			velocity = 1
		elif -1 > velocity:
			velocity = -1
		return velocity
	
	def	encoderread(self):
		self.totcount= self.encoder0.getPosition()
		print(self.totcount)
		self.numEncoderRead=self.numEncoderRead+1
		#self.writecsv(self.numEncoderRead,self.totcount)
	
	def degToCount(self):
		angle = self.readcsv()
		self.targetCount = [0] * len(angle)
		for ii in range(0, len(angle)):
			self.targetCount[ii]=int(angle[ii]*self.cpr/360)
		
	def readcsv(self):
		reader = pandas.read_csv("CSVReading.csv",sep=',')
		return reader.Angle

		
	def inicsv(self):
		df = pandas.DataFrame(columns=['Time','Position'])
		df.to_csv("CSVWriting.csv", index = False, header=True)
	
	def writecsv(self,numEncoderRead,totcount):
		with open('CSVWriting.csv', 'w') as file:
			self.writer = [csv.writer(file)]*numEncoderRead
			self.writer[int(numEncoderRead)].writerow([numEncoderRead, '\t', "Time", '\t', totcount])
	
	def gettime(self):
		timeval1 = int(time.clock() * self.timemult)
		timedif = timeval1 - self.timeval0
		#print (timedif)
		return timedif
		
   
		
if __name__ == '__main__':
	main = Position_Control()
	main.setup()
	