# Fixed LiDAR Scan
This repository presents the software of a three-dimensional laser range finder based on a 2D laser scanner Hokuyo URG-04LX-UG01 and two step motors.

### Description:
A reconstruction of the real world from a computer graphics tool is one of the main problems in two different communities such as robotics and artificial intelligence, under different topics of computer science, perception and artificial vision . A real scene can be reconstructed with the help of depth sensors, rotational elements and mathematical transformations depending on the physical design, to obtain point clouds. This project presents the development of a three-dimensional laser rangefinder based on a two-dimensional laser scanner Hokuyo URG-04LX-UG01 and two stepper motors. The design and kinematic model of the system to generate point clouds in 3D will be presented with an experimental acquisition algorithm implemented in Robotic Operative System ROS in Python language. The quality of the reconstruction generated will be improved with a calibration algorithm based on a parameter optimization model on a reference surface. The simultaneous application of the system will allow viewing the scene from different perspectives. The results achieved can be visualized with Python or MATLAB and can be used for surface reconstruction, scene classification or mapping. In this way, typical robotic tasks could be performed, such as the prevention of collisions, the calculation of grip or the handling of objects, navigation of autonomous vehicles, supervision of levels, monitoring of structures, prevention of natural disasters, among others.

### Read the publicated paper ["3D Scene Reconstruction Based on a 2D Moving LiDAR"](https://link.springer.com/chapter/10.1007/978-3-030-01535-0_22).

## This repository contents:

  - Source codes (Python|ROS)
  - Data examples

### Repository folders

    /your root                          -path
    |--- src
        |--- Arduino
            |--- Prot_Com.ino           #communication protocol
        |--- Raspberry
            |--- scan.py                #script to scan
            |--- matrices.py            #library script to rebuild
        |--- App
            |--- webserver.py           #script launcher of the web page
            |--- templates
                |--- main.html          #main menu template
                |--- scan.html          #menu template scan
    |--- Data                           
        |---pasilloMec.txt              #point cloud example

## Hardware requirements:
 - Raspberry Pi 3
 - Arduino Nano
 - Step by step drivers "EasyDriver V44 A3967" 
 - Hokuyo "URG-04LX-UG01"
 
## Software requirements:
 - Python 2.7 *Flask
 - ROS Kinetic
 - Arduino IDLE 
 
## How to install:

**Note:** Before accessing the Raspberry via ssh you have to enable the SSH on the raspberry.

### In your computer:

* Update the libraries:

    `$ sudo apt-get update`
    `$ sudo apt-get upgrade`
    
* Install arduino on Raspberry by using :

	`$ sudo apt-get install arduino arduino-core`

* Connect the raspberry and verify  which port it was configured. Open the command window and execute the following line of code:
    
   ` $ ls /dev`
    
* Disconnect the arduino and execute the previous line. Observe the port number, for example: ttyUSB0.

* Enable read and write permissions to the arduino board:
    
    `$ sudo chmod 666 /dev/ttyUSB0`
    
    
### Installing ROS

* Create a catkin Workspace. In order to build the core packages, you will need a catkin workspace. Create one now:

    `$ mkdir -p ~/ros_catkin_ws`
   `$ cd ~/ros_catkin_ws`
    
* Next we will want to fetch the core packages so we can build them. We will use wstool for this. Select the wstool command for the particular variant you want to install:  Communication package. ROS-Comm: (recommended) ROS package, build, and communication libraries. No GUI tools.

    `$ rosinstall_generator ros_comm --rosdistro kinetic --deps --wet-only --tar > kinetic-ros_comm-wet.rosinstall`
    `$ wstool init src kinetic-ros_comm-wet.rosinstall`
    
* LiDAR package

    `$ rosinstall_generator urg_node robot_upstart --rosdistro kinetic --deps --wet-only --tar > kinetic-custom_ros.rosinstall`
    `$ wstool merge -t src kinetic-custom_ros.rosinstall`
    `$ wstool update -t src`

* Resolve Dependencies

* Before you can build your catkin workspace, you need to make sure that you have all  the required dependencies. We use the rosdep tool for this, however, a couple of dependencies are not available in the repositories. They must be manually built first.

    `$ mkdir -p ~/ros_catkin_ws/external_src`
    `$ cd ~/ros_catkin_ws/external_src`
    `$ wget http://sourceforge.net/projects/assimp/files/assimp-3.1/assimp-3.1.1_no_test_models.zip/download -O assimp-3.1.1_no_test_models.zip`
    `$ unzip assimp-3.1.1_no_test_models.zip`
    `$ cd assimp-3.1.1`
    `$ cmake .`
    `$ make`
    `$ sudo make install`
    
* Resolving Dependencies with rosdep
The remaining dependencies should be resolved by running rosdep:

    `$ cd ~/ros_catkin_ws`
    `$ rosdep install -y --from-paths src --ignore-src --rosdistro kinetic -r --os=debian:stretch`

* Building the catkin Workspace
Once you have completed downloading the packages and have resolved the dependencies, you are ready to build the catkin packages.

* Invoke catkin_make_isolated: 

    `$ sudo ./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release --install-space /opt/ros/kinetic -j2`
    
### Initialize the controller for Hokuyo

* Open a command window and copy the following line:

    `$ nano .bashrc`
    
* At the end of the file copy the following (only once):

   `function hokuyo {
        sudo chmod a+rw /dev/ttyACM0
        rosrun urg_node getID /dev/ttyACM0
        rosparam set urg_node/calibrate_time false
        rosparam set urg_node/port /dev/ttyACM0
        rosrun urg_node urg_node
    }`
    
* Save the changes

### Installing Flask
* In order to install Flask, you’ll need to have pip installed. If you haven’t already
installed pip, it’s easy to do:

    `$ sudo apt-get install python-pip`
    
* After pip is installed, you can use it to install Flask and its dependencies:

    `$ sudo pip install flask`
    
### Create the Access Point

* Follow the instructions in the following video: [video](https://www.youtube.com/watch?v=WqpvjzyZleU).

## How to Use:

* On the computer with installed putty, open putty (enter raspberry's IP, username and password), and execute the following line

    `$ roscore`
    
* In another command window and write the line:

    `$ hokuyo & ./webserver.py`
    
* In the browser of any mobile device (cell phone, tablet, etc.) enter the IP: 10.3.141.1:8080

* Go to scan, then enter the required data:

    name of the file:
    minimum limit inclination:
    maximum limit inclination:
    resolution of the engine inclination:
    resolution of the engine rotation:
    email:
    
* Press Scan

## Authors:
**Universidad de Ibagué** - **Ingeniería Electrónica**
**Proyecto de Grado 2019/A**
 - [Harold F. Murcia](http://haroldmurcia.com/)
 -  [Luis Fernando Mora](mailto:2420111029@estudiantesunibague.edu.co)
***