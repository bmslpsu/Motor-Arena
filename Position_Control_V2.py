from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID
import time
import pandas


class Position_Control:
    def __init__(self):
        self.cpr = 324  # Number of count per Revolution of Encoder
        self.iniVelocity = 1  # initial velocity

        self.ii = 0
        self.totcount = 0  # Position Counter
        self.samplingrate = 0.01  # samplingrate in (second)
        self.numEncoderRead = 0
        self.timemult = pow(10, 4)  # millisecond

        self.timeval0 = int(time.clock() * self.timemult)

    def setup(self):
        self.encoder0 = Encoder()
        self.dcMotor0 = DCMotor()

        self.degToCount()  # Load in desired position
        self.inicsv()  # Initial data file
        self.motorposition = [0]*(len(self.targetCount)+100)
        self.motortime = [0] * (len(self.targetCount) + 100)

        self.encoder0.openWaitForAttachment(5000)
        self.dcMotor0.openWaitForAttachment(5000)

        self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())

        self.dcMotor0.setTargetVelocity(self.iniVelocity)
        self.encoder0.setOnPositionChangeHandler(self.encoderread)

        try:
            input("Press Enter to Stop\n")
        except (Exception, KeyboardInterrupt):
            pass

        self.encoder0.close()
        self.dcMotor0.close()

        # self.writecsv()

    def positionControl(self,totcount):
        target = self.targetCount[self.ii]
        print(target)
        self.pid = PID(0.022, 0.0003, 0.01, setpoint=target)
        timer = self.gettime()
        self.motortime[self.ii] = timer
        self.motorposition[self.ii] = totcount

        while (timer % 10) != 0:
            velocity = self.PIDposition(totcount)
            self.dcMotor0.setTargetVelocity(velocity)
            timer = self.gettime()
        self.ii=self.ii+1

        if self.ii == len(self.targetCount):
            self.encoder0.close()
            self.dcMotor0.close()
            self.writecsv()

    def PIDposition(self,currentloca):
        velocity = self.pid(currentloca)
        if 1 < velocity:
            velocity = 1
        elif -1 > velocity:
            velocity = -1
        return velocity

    def encoderread(self,positionChange, timeChange, indexTriggered,test):
        totcount = self.encoder0.getPosition()
        self.numEncoderRead = self.numEncoderRead + 1
        self.positionControl(totcount)

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
            table[ii] = [self.motortime[ii-1],'\t',self.motorposition[ii-1]]
        df = pandas.DataFrame(table)
        df.to_csv("CSVWriting.csv", index=False, header=False)

    def gettime(self):
        timeval1 = int(time.clock() * self.timemult)
        timedif = timeval1 - self.timeval0
        return timedif


if __name__ == '__main__':
    main = Position_Control()
    main.setup()
