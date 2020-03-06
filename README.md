# Motor-Arena
ROS library to control am insect virtual-reality arena mounted on a motor

Installation step
1. Install ROS
2. install rospy:
	sudo apt-get update -y
	sudo apt-get install -y python-rospy
2. detail instruction: https://artisan-roasterscope.blogspot.com/2017/01/connecting-phidgets-on-linux.html	
3. check libusb-1.0.0 library installed or not (usually installed)
	sudo apt-get install libusb-1.0-0-dev
3. Download phidget22 library from website
4. Following the README file and install phidget22 library(use sudo for every step)
5. Now Linux usually required the root to access USB devices, use sudo to run scripts or install udev
6. For installing udev, cd into the unzipped phidget22 folder
	run: sudo cp plat/linux/udev/99-libphidget22.rules /etc/udev/rules.d
	reboost computer

Libraries needed:
	Phidget22
	simple_pid
	time
	pandas
	matplotlib
