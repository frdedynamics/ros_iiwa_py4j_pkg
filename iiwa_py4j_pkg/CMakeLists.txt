cmake_minimum_required(VERSION 2.8.3)
project(iiwa_py4j_pkg)

find_package(catkin REQUIRED COMPONENTS
    rospy
    std_msgs
    message_generation
)

 add_message_files(
   FILES
   JointCommandPosition.msg
   JointCommandEffort.msg
   ExternalTorque.msg
)
generate_messages(
    DEPENDENCIES
    std_msgs
)

catkin_package(
)


include_directories(
    ${catkin_INCLUDE_DIRS}
)
