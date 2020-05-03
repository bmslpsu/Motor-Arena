# Motor-Arena
	An insect virtual-reality simulator that mounted on a DC motor
---
## Installation step
1. Install ROS
2. install rospy:
	sudo apt-get update -y
	sudo apt-get install -y python-rospy
3. detail instruction: [Phidget website](https://artisan-roasterscope.blogspot.com/2017/01/connecting-phidgets-on-linux.html)
4. check libusb-1.0.0 library installed or not (usually installed)
	`sudo apt-get install libusb-1.0-0-dev`
5. Download phidget22 library from website
6. Following the `README` file and install phidget22 library(use `sudo` for every step)
7. Linux usually required the root to access USB devices, please install the udev(recommended), or use `sudo` to run scripts. Without admin permission, phidget cannot be activated and will display connection error. udev can give phidget library the permission for ever. 
8. For installing udev, `cd` into the unzipped phidget22 folder
	run: `sudo cp plat/linux/udev/99-libphidget22.rules /etc/udev/rules.d`
	Then reboost computer
---
## Libraries needed:
* Phidget22
* simple_pid
* time
* pandas
* matplotlib
* numpy
---
## Purposes of each file
* Connectiontest.py file is the program provided by Phidget, that will drive the motor and display encoder velocity reading. You can use this code to test the connection of power and encoder pins. Furthermore, you can use this code to test if you installed the udev successfully. 
* CSVReading is the sample trajectory for the program to read.
* CSVWriting is the sample output from the program
* PID_gain file is the PID gains that tuned by ZHengqi(George) Zhong under different conditions for both position and velocity control.
* Position_Control.py will read the position trajectory, and used PID controller to control the DC motor to follow this given target trajectory. Then recording the motor Time, Position, PWM output(Analog Voltage, between (-1 and 1)), and the Error between motor trajectory and target trajectory history. Then generate a plot about target trajectory and actual trajectory.
* Velocity_Control.py is similar with Position_Control.py, but taking the velocity trajectory. It will output Time, motor speed (RPM), motor position, RPM different between motor and target velocity, and the PWM output (between -1 and 1). Then generate a plot about target trajectory and actual trajectory.
* ploting will read the target trajectory CSV file (both position and velocity) and the recorded history CSV file, then generate plots that are same as the plot generated in the end of Position_Control.py and Velocity_Control.py.
---
## Tips about generating trajectory .CSV file
* For position control trajectory, all the numbers are in unit of degree, in the first line of trajectory, you must add "Angle" for the program to recognize. Usually I create a trajectory with 10000 data point in 10 second. It seem like the optimal number of element for the phidget device, because of the sampling interval. 
* For velocity control trajectory, all the number are in unit of RPM, the first line must have "Velocity" to begin with. Usually I create a trajectory with 10000 data point in 10 second. It seem like the optimal number of element for the phidget device, because of the sampling interval. 
* There should not have a empty line in the end of trajectory, otherwise will cause .csv file reading error. 
---

