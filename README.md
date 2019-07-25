# ros_iiwa_py4j_pkg
iiwa pubs´n´subs using FRI, java app and py4j.

# How to use:
Using ubuntu 16.04 with ROS Kinetic

Terminal
1. cd
2. mkdir -p <my_ws>/src
3. cd <my_ws>
4. catkin_make

Clone this repo to <my_ws>/src. Make sure the .py files you want to run are executable.

If roscore and the java app for FRI is running and working, then the following will publish the measured joint state:
 
./measured_joint_state.py 


