#!/usr/bin/env python
""" module docstring, yo! """

import sys
import rospy
from py4j.java_gateway import JavaGateway

from iiwa_py4j_pkg.msg import JointCommandEffort

GATEWAY = JavaGateway()

FRI = GATEWAY.entry_point


def callback(data):
    """ function docstring, yo! """
    rospy.loginfo("%f %f %f %f %f %f %f", data.values[0], data.values[1], data.values[2], data.values[3],
                  data.values[4], data.values[5], data.values[6])
    double_array = GATEWAY.new_array(GATEWAY.jvm.double, 7)

    for i in range(0, len(data.values)):
        double_array[i] = data.values[i]
    FRI.setCommandedJointTorque(double_array)


def listener():
    """ function docstring, yo! """
    rospy.init_node('kuka_torque_control', anonymous=True)
    rospy.Subscriber("cmd_trq", JointCommandEffort, callback)
    rospy.spin()


if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)

    print("args I don't care about: ", MYARGV)
    try:
        listener()
    except rospy.ROSInterruptException:
        pass