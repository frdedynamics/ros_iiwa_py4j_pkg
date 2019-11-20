#!/usr/bin/env python
""" module docstring, yo! """

import sys
import rospy
from py4j.java_gateway import JavaGateway

from sensor_msgs.msg import JointState

GATEWAY = JavaGateway()

FRI = GATEWAY.entry_point

TMP_PREV = (0, 0)


def talker():
    """ docsctring, yo! """
    global TMP_PREV

    joint_state_pub = rospy.Publisher('iiwa_joint_states', JointState, queue_size=1)
    rospy.init_node('kuka_joint_state', anonymous=True)

    previous_iiwa_seconds_and_nano = 0.0
    previous_joint_positions = None
    latest_joint_velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    while not rospy.is_shutdown():
        try:
            msg = JointState()
            tmp = FRI.getMeasurementsPacket()

            latest_iiwa_seconds_and_nano = tmp[0] + tmp[1] / 1e9
            latest_delta_iiwa_seconds_and_nano = latest_iiwa_seconds_and_nano - previous_iiwa_seconds_and_nano
            latest_joint_positions = [tmp[2], tmp[3], tmp[4], tmp[5], tmp[6], tmp[7], tmp[8]]
            if previous_joint_positions is not None:
                if latest_delta_iiwa_seconds_and_nano > 0.0:
                    for i in range(0, 7):
                        latest_joint_velocities[i] = (latest_joint_positions[i] - previous_joint_positions[i])\
                                                     / latest_delta_iiwa_seconds_and_nano

            msg.header.stamp.secs = int(tmp[0])
            msg.header.stamp.nsecs = int(tmp[1])
            msg.name = ['joint_a1', 'joint_a2', 'joint_a3', 'joint_a4', 'joint_a5', 'joint_a6', 'joint_a7']
            msg.position = latest_joint_positions
            msg.velocity = latest_joint_velocities
            msg.effort = [tmp[9], tmp[10], tmp[11], tmp[12], tmp[13], tmp[14], tmp[15]]

            if latest_delta_iiwa_seconds_and_nano != previous_iiwa_seconds_and_nano:
                joint_state_pub.publish(msg)

            previous_iiwa_seconds_and_nano = latest_iiwa_seconds_and_nano
            previous_joint_positions = latest_joint_positions

        except Exception as exception_e:
            rospy.logerr("%s", exception_e)


if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)

    print("args I don't care about: ", MYARGV)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
