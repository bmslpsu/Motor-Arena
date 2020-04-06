import pandas
import matplotlib.pyplot as plt
import numpy

class Ploting:
    def __init__(self):
        self.filetrajecory = "trajectory.csv"
        self.filemotorhist = "CSVWriting.csv"
        self.cpr = 324
        self.timemult = 100000

    def readfile(self):
        self.readertra = pandas.read_csv("/home/george/Desktop/Testing_Figure/Trajectory/NewTraj/0.5Hz_Sine_40deg.csv", sep=',')
        self.readerhist = pandas.read_csv("CSVWriting.csv", sep=',')

    def positionPloting(self):
        self.motorTime = self.readerhist.Time
        self.motorPosition = self.readerhist.Position
        self.motorPWM = self.readerhist.AnalogVolt
        self.motorDiff = self.readerhist.Error

        self.trajectory = [0] * len(self.readertra)
        for ii in range(0, len(self.readertra)):
            self.trajectory[ii] = int(self.readertra.Angle[ii] * self.cpr / 360)

        x = numpy.linspace(0, 10, 10000)

        plt.plot(x, self.trajectory,'b-')
        plt.plot(self.motorTime, self.motorPosition,'y-')
        plt.title('0.5Hz_Sine_40deg', fontsize=25)
        plt.legend(['Target','Actual'], fontsize=25,loc = 'upper right')
        plt.xlabel('Time')
        plt.ylabel('Count')

        plt2 = plt.twinx()
        plt2.set_ylabel('Voltage Output(V)', color = 'red')
        plt2.tick_params(axis='y', labelcolor='red')
        plt2.plot(self.motorTime,self.motorPWM,'r-')
        plt.show()

    def velocityPloting(self):
        self.motorTime = self.readerhist.Time
        self.motorRPM = self.readerhist.RPM
        self.motorPosition = self.readerhist.Position
        self.motorRPMdiff = self.readerhist.RPMDifferent
        self.motorAnalog = self.readerhist.AnalogOutput

        self.trajectory = [0] * len(self.readertra)
        for ii in range(0, len(self.readertra)):
            self.trajectory[ii] = int(self.readertra.Velocity[ii] * self.cpr / 360)

        x = numpy.linspace(0, 10, 10000)

        plt.plot(x, self.trajectory,'b-')
        plt.plot(self.motorTime, self.motorRPM,'y-')
        plt.title('0.1Hz_Sine_250RPM', fontsize=25)
        plt.legend(['Target','Actual'], fontsize=25,loc = 'upper right')
        plt.xlabel('Time')
        plt.ylabel('RPM')

        plt2 = plt.twinx()
        plt2.set_ylabel('PWM', color = 'red')
        plt2.tick_params(axis='y', labelcolor='red')
        plt2.plot(self.motorTime,self.motorAnalog,'r-')
        plt2.legend(['PWM'], fontsize=25, loc='lower right')
        plt.show()

if __name__ == '__main__':
    main = Ploting()
    main.readfile()
    main.positionPloting()