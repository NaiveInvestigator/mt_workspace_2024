#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry

def talker():
    pub = rospy.Publisher('odometry/gps', Odometry, queue_size=10)
    rospy.init_node('dummy_gps', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        dummy_odom = Odometry()
        dummy_odom.header.stamp = rospy.Time.now()
        dummy_odom.header.frame_id = 'odom'
        dummy_odom.child_frame_id = 'base_link'
        dummy_odom.pose.pose.position.x = 0.0
        dummy_odom.pose.pose.position.y = 0.0
        dummy_odom.pose.pose.position.z = 0.0
        dummy_odom.twist.twist.linear.x = 0.0
        dummy_odom.twist.twist.linear.y = 0.0
        dummy_odom.twist.twist.angular.z = 0.0

        dummy_odom.pose.pose.orientation.x = 0.0
        dummy_odom.pose.pose.orientation.y = 0.0
        dummy_odom.pose.pose.orientation.z = 1.0
        dummy_odom.pose.pose.orientation.w = 1.0

        # Publish the dummy Odometry message
        pub.publish(dummy_odom)
        rate.sleep()

if __name__ == '__main__':
    print("Dummy gps started")
    try:
        talker()
    except rospy.ROSInterruptException:
        pass