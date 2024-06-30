#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Imu
from std_msgs.msg import Header

def talker():
    pub = rospy.Publisher('imu/data', Imu, queue_size=10)
    rospy.init_node('dummy_imu', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        imu_msg = Imu()
        imu_msg.header = Header(stamp=rospy.Time.now(), frame_id='base_link')
        imu_msg.orientation.x = 0.0
        imu_msg.orientation.y = 0.0
        imu_msg.orientation.z = 0.0
        imu_msg.orientation.w = 1.0

        imu_msg.angular_velocity.x = 0.0
        imu_msg.angular_velocity.y = 0.0
        imu_msg.angular_velocity.z = 0.0

        imu_msg.linear_acceleration.x = 0.0
        imu_msg.linear_acceleration.y = 0.0
        imu_msg.linear_acceleration.z = 0.0  # Earth's gravity

        # Publish the dummy IMU message
        pub.publish(imu_msg)
        rate.sleep()

if __name__ == '__main__':
    print("Dummy imu started")
    try:
        talker()
    except rospy.ROSInterruptException:
        pass