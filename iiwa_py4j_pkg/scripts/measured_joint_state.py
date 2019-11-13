#!/usr/bin/env python
""" module docstring, yo! """

import sys
import rospy
import time
from py4j.java_gateway import JavaGateway

from sensor_msgs.msg import JointState

GATEWAY = JavaGateway()

FRI = GATEWAY.entry_point

TMP_PREV = (0,0)


def talker():
    """ docsctring, yo! """
    global TMP_PREV

    joint_state_pub = rospy.Publisher('iiwa_joint_states', JointState, queue_size=1)
    rospy.init_node('kuka_joint_state', anonymous=True)

    seconds_and_nano_prev = 0.0
    rate_avg = 0.0
    disp_i = 0
    t_now = time.time()
    t_prev = t_now
    delta_t = 0.0
    delta_t_avg = 0.0
    fri_sys_diff = 0.0
    while not rospy.is_shutdown():
        try:
            msg = JointState()
            tmp = FRI.getMeasurementsPacket()
            msg.header.stamp.secs = int(tmp[0])
            msg.header.stamp.nsecs = int(tmp[1])
            msg.name = ['joint_a1', 'joint_a2', 'joint_a3', 'joint_a4', 'joint_a5', 'joint_a6', 'joint_a7']
            msg.position = [tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8]]
            msg.effort = [tmp[9],tmp[10],tmp[11],tmp[12],tmp[13],tmp[14],tmp[15]]

            if (tmp[0] + tmp[1]/1e9) != (TMP_PREV[0] + TMP_PREV[1]/1e9):
                joint_state_pub.publish(msg)
            TMP_PREV = tmp
        except Exception as exception_e:
            rospy.logerr("%s", exception_e)

        try:
            seconds_and_nano_now = tmp[0] + tmp[1]/1e9
            if (seconds_and_nano_now-seconds_and_nano_prev) > 0.000000:
                rate_avg = 0.5*rate_avg + (1-0.5)*(seconds_and_nano_now-seconds_and_nano_prev)
            seconds_and_nano_prev = seconds_and_nano_now

            t_now = time.time()
            delta_t_avg = 0.5*delta_t_avg + (1-0.5)*(t_now-t_prev)
            t_prev = t_now

            fri_sys_diff = seconds_and_nano_now - t_now
            disp_i = disp_i+1
            if disp_i > 700:
                print(1/rate_avg, 1/delta_t_avg, fri_sys_diff)
                disp_i = 0
                
        except Exception as exception_e:
            rospy.logerr("%s", exception_e)

if __name__ == '__main__':
    MYARGV = rospy.myargv(argv=sys.argv)

    print("args I don't care about: ", MYARGV)
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
