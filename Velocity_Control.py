from Phidget22.Phidget import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.Encoder import *
from simple_pid import PID                                  # PID library
import time
import pandas                                               # Reading and Writing .csv file
import matplotlib.pyplot as plt                             # Ploting trajectory
import numpy

class Velocity_Control:
    def __init__(self):
        self.cpr = 324.0                                    # Number of count per Revolution of Encoder
        self.iniVelocity = 0.25                             # initial velocity
        self.samplingrate = 0.001                           # sampling rate of trajectory (second)
        self.pid = PID(0.01 , 0.008665 , 0.0015, setpoint=0)            # PID control gain
        self.numstored = 25                                 # Number of samples for moving average, since the time.time() does not accurated enough during short period of time
        self.trajectoryRoot = "sampleTrajectory/VelocityControl/1.5Hz_Step_100rpm.csv"
        self.motorHistoryRoot = "sampleTrajectory/VelocityControl/HISTORY_1.5Hz_Step_100rpm.csv"
#=======================================================================================================================
        self.ii = 0                                         # Accumulated number of trajectory passed
        self.RPMDiff = 0                                    # Different between current velocity VS desired velocity (RPM)
        self.timeMult = (1/self.samplingrate)*100           # Converting time.time unit to millisecond
        self.encoderCount = [0]*self.numstored              # Storing encoder read for moving average
        self.encoderTime = [0] *self.numstored              # Storing time value for each correlated encoder reading

    def setup(self):
        self.encoder0 = Encoder()                           # setup encoder and motor from Phidget Library
        self.dcMotor0 = DCMotor()
        self.readcsv()                                      # Read Trajectory File

        # Define the variables to store trajectory history, will be writen into .csv file
        self.motorTime = [0] * (len(self.targetVelocity))           # Time History
        self.motorRPM = [0] * (len(self.targetVelocity))            # RPM History
        self.motorPosition = [0]*(len(self.targetVelocity))         # Position history
        self.motorRPMDiff = [0] * (len(self.targetVelocity))        # Difference bwtween desired and actual motor position
        self.motorAnalogOut = [0] * (len(self.targetVelocity))      # PWM signal history

        self.encoder0.openWaitForAttachment(5000)                   # Open Phidget Channel and wait for 5 second for data
        self.dcMotor0.openWaitForAttachment(5000)

        self.dcMotor0.setTargetVelocity(self.iniVelocity)                   # set motor to inivial speed.
        self.encoder0.setDataInterval(self.encoder0.getMinDataInterval())   # Set the encoder reading interval to minimum, which is 8 ms for Phidget 1065_1 Motor Driver
        self.encoder0.setOnPositionChangeHandler(self.encoderread)          # Similar to the interrupt function, call encoderread function when position changed

        self.time0 = time.time() * self.timeMult                            # define Time 0
        self.encoderTime = [self.time0]* self.numstored                     # Prevent strange value in Moving Average Calculation, Predefine each value to Time 0


        while self.ii != len(self.targetVelocity):                          # Loop through the value in Desired trajectory array
            self.velocityControl()                                          # main function to control the motor position
            self.getdata()                                                  # Record the time and position data, will be converted into .csv file.
            self.ii = self.ii + 1

        self.encoder0.close()                               # Turn off encoder and motor
        self.dcMotor0.close()

        self.writecsv()                                     # Write the Data in getdata function into a .csv file
        self.ploting()                                      # Plot the scatter plot of desired and actual motor position

    def velocityControl(self):
        target = self.targetVelocity[self.ii]                   # getting one value from the target trajectory array
        while (self.pullingtime() % 100) != 0:                  # Time Pulling, control the motor position every 0.001 second
            pass
        self.getRPM()                                           # Computing Current RPM value
        self.RPMDiff = self.currentRPM - target                 # compute the difference between Desired and Current
        velocity = self.PIDvelocity(self.RPMDiff)               # Using PID to compute the velocity based on the RPM different
        #velocity = 0.25
        self.dcMotor0.setTargetVelocity(velocity)               # set velocity between -1 to 1 to Phidget Motor driver

    def PIDvelocity(self,RPMDiff):
        velocity = self.pid(RPMDiff)                            # use simple_PID library to compute velovity
        self.motorAnalogOut[self.ii] = velocity                 # recording the value of analog output
        if 1 < velocity:                                        # Bound the velocity between -1 and 1
            velocity = 1
        elif -1 > velocity:
            velocity = -1
        return velocity

    def encoderread(self,positionChange, timeChange, indexTriggered,test):
        for ii in range (self.numstored-1):                                     # Passing each Position and Time Values
            self.encoderCount[ii] =self.encoderCount[ii+1]
            self.encoderTime[ii] = self.encoderTime[ii + 1]

        self.encoderCount[self.numstored-1] = self.encoder0.getPosition()           # Read encoder count when the encoder is turning
        self.encoderTime[self.numstored-1] = time.time()*self.timeMult              # Read time when encoder turning detected

    def pullingtime(self):
        timepulling = time.time()*self.timeMult
        timepass = int((timepulling - self.time0))                                  # Time Pulling function for accurate sampling time
        return timepass

    def getRPM(self):
        countDiff = (self.encoderCount[self.numstored-1]-self.encoderCount[0])      # compute the position different for Moving Average calculation
        timeDiff = (self.encoderTime[self.numstored-1]-self.encoderTime[0])         # compute the time different for Moving Average calculation
        if timeDiff == 0:
            timeDiff=1                                                              # Prevent 0 in denominator
        self.currentRPM = ((countDiff/self.cpr)/(timeDiff)*self.timeMult)*60        # compute the RPM

    def getdata(self):  # Recording the values when new velocity is setted to Motor Driver, all values will be saved to a .csv file
        self.motorTime[self.ii] = (self.encoderTime[self.numstored-1] - self.time0)/self.timeMult       # Recording the Time
        self.motorPosition[self.ii] = self.encoderCount[self.numstored-1]                               # Record the motor position
        self.motorRPM[self.ii] = self.currentRPM                                                        # Recording RPM History of the motor
        self.motorRPMDiff[self.ii] = -self.RPMDiff                                                      # Recording the different between desired and actual RPM

    def readcsv(self):
        reader = pandas.read_csv(self.trajectoryRoot, sep=',')                      # read Trajectory angle from a .csv file
        self.targetVelocity = reader.Velocity

    def writecsv(self):
        table = [0]*(len(self.motorTime)+1)                                         # Create a table to store time spend, motor position history and difference between target and actual position
        table[0] = ["Time",'\t',"RPM",'\t',"Position",'\t',"RPMDifferent",'\t',"AnalogOutput"]      # the heading for each column
        for ii in range(1,len(table)):                                                              # Import information into each cell of table array
            time = self.motorTime[ii-1]-self.motorTime[1]
            table[ii] = [time,'\t',self.motorRPM[ii-1],'\t',self.motorPosition[ii-1],'\t',self.motorRPMDiff[ii-1],'\t',self.motorAnalogOut[ii-1]]
        df = pandas.DataFrame(table)                                                                # convert table array into pandas dataFrame
        df.to_csv(self.motorHistoryRoot, index=False, header=False)                                      # write into .csv file named CSVWriting.csv


    def ploting(self):                                                      # Plot the history, same as Ploting.py.
        self.trajectory = self.targetVelocity
        x = numpy.linspace(0, 10, 10000)

        plt.plot(x, self.trajectory, 'b-')
        plt.plot(self.motorTime, self.motorRPM, 'y-')
        plt.title('1Hz_Sine_50RPM', fontsize=25)
        plt.legend(['Target', 'Actual'], fontsize=25, loc='upper right')
        plt.xlabel('Time')
        plt.ylabel('RPM')

        #plt2 = plt.twinx()
        #plt2.set_ylabel('PWM', color='red')
        #plt2.tick_params(axis='y', labelcolor='red')
        #plt2.plot(self.motorTime, self.motorAnalogOut, 'r-')
        #plt2.legend(['PWM'], fontsize=25, loc='lower right')
        plt.show()

if __name__ == '__main__':
    main = Velocity_Control()
    main.setup()