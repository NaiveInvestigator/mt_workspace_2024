#! /usr/bin/env python3

from witmotion import IMU
from time import sleep
import rospy
from std_msgs.msg import String

rospy.init_node("witmotion")

witmotion = rospy.Publisher("/imu", String, queue_size=10)

if __name__ == "__main__":  
    port_name = rospy.get_param("~bleeeh", "/dev/ttyUSB0")
    print(port_name)
    imu = IMU(port_name) #"/dev/ttyUSB1")
    while not rospy.is_shutdown():
        yaw = imu.get_angle()[2]
        if yaw == None:
            pass
        else:
            yaw = -yaw
            rospy.loginfo(yaw)
            witmotion.publish(str(yaw))
    imu.close()
