from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID
import time
import pandas
import matplotlib.pyplot as plt
import numpy

class Position_Control:
    def __init__(self):
        self.cpr = 324  # Number of count per Revolution of Encoder
        self.iniVelocity = 0  # initial velocity

        self.ii = 0
        self.totcount = 0  # Position Counter
        self.samplingrate = 0.01  # samplingrate in (second)
        self.numEncoderRead = 0

        self.timemult = (1/self.samplingrate)*100  # millisecond
        self.timeval0 = int(time.time() * self.timemult)

    def setup(self):
        self.encoder0 = Encoder()
        self.dcMotor0 = DCMotor()

        self.degToCount()  # Load in desired position
        self.inicsv()  # Initial data file
        self.motorposition = [0]*(len(self.targetCount))
        self.motortime = [0] * (len(self.targetCount))

        self.encoder0.openWaitForAttachment(5000)
        self.dcMotor0.openWaitForAttachment(5000)

        self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())

        self.dcMotor0.setTargetVelocity(self.iniVelocity)
        self.encoder0.setOnPositionChangeHandler(self.encoderread)

        while self.ii != len(self.targetCount):
            self.positionControl()
            self.ii = self.ii + 1

        self.encoder0.close()
        self.dcMotor0.close()

        self.writecsv()
        self.ploting()

    def positionControl(self):
        target = self.targetCount[self.ii]
        self.pid = PID(0.005, 0, 0, setpoint=target)
        while (self.gettime() % 100) != 0:
            pass
        velocity = self.PIDposition(self.totcount)
        self.dcMotor0.setTargetVelocity(velocity)

    def PIDposition(self,currentloca):
        velocity = self.pid(currentloca)
        if 1 < velocity:
            velocity = 1
        elif -1 > velocity:
            velocity = -1
        return velocity

    def encoderread(self,positionChange, timeChange, indexTriggered,test):
        self.totcount = self.encoder0.getPosition()
        self.numEncoderRead = self.numEncoderRead + 1
        self.getdata()


    def getdata(self):
        self.motortime[self.ii] = self.gettime()
        self.motorposition[self.ii] = self.totcount

    def degToCount(self):
        angle = self.readcsv()
        self.targetCount = [0] * len(angle)
        for ii in range(0, len(angle)):
            self.targetCount[ii] = int(angle[ii] * self.cpr / 360)

    def readcsv(self):
        reader = pandas.read_csv("trajectory.csv", sep=',')
        return reader.Angle

    def inicsv(self):
        df = pandas.DataFrame(columns=['Position'])

    def writecsv(self):
        table = [0]*(len(self.motortime)+1)
        table[0] = ["Time",'\t',"Position"]
        for ii in range(1,len(table)):
            time = self.motortime[ii-1]-self.motortime[1]
            table[ii] = [time,'\t',self.motorposition[ii-1]]
        df = pandas.DataFrame(table)
        df.to_csv("CSVWriting.csv", index=False, header=False)

    def gettime(self):
        timeval1 = int(time.time() * self.timemult)
        self.timedif = float(timeval1 - self.timeval0)
        return self.timedif

    def ploting(self):
        x = numpy.linspace(0, 10, 1000)
        tt = [0.1]*len(self.motortime)
        t0 = self.motortime[1]
        for ii in range (len(self.motortime)):
            tt[ii] = (self.motortime[ii]-self.motortime[1])/self.timemult

        plt.plot(x,self.targetCount,tt,self.motorposition)
        #print (tt)
        #plt.plot(tt, self.motorposition)
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.show()

if __name__ == '__main__':
    main = Position_Control()
    main.setup()