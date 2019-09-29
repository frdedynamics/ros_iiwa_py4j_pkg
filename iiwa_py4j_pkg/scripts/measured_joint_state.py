#!/usr/bin/env python
""" module docstring, yo! """

import sys
import rospy
from py4j.java_gateway import JavaGateway

from sensor_msgs.msg import JointState

GATEWAY = JavaGateway()

FRI = GATEWAY.entry_point


def talker():
    """ docsctring, yo! """
    
    joint_state_pub = rospy.Publisher('iiwa_joint_states', JointState, queue_size=1)
    rospy.init_node('kuka_joint_state', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        try:
            msg = JointState()
            tmp = FRI.getTimeStampSecNanoSec()
            msg.header.stamp.secs = tmp[0]
            msg.header.stamp.nsecs = tmp[1]
            msg.name = ['joint_a1', 'joint_a2', 'joint_a3', 'joint_a4', 'joint_a5', 'joint_a6', 'joint_a7']
            msg.position = list(FRI.getMeasuredJointPosition())
            # msg.velocity = list(FRI.getMeasuredJointPosition())
            msg.effort = list(FRI.getMeasuredTorque())

            joint_state_pub.publish(msg)
        except Exception as exception_e:
            rospy.logerr("%s", exception_e)
        rate.sleep()


if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)

    print("args I don't care about: ", MYARGV)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
