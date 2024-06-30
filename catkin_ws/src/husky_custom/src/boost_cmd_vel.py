#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist


def twist_callback(msg):

    boosted_twist = Twist()
    boosted_twist.linear.x = msg.linear.x * 1
    boosted_twist.linear.y = msg.linear.y * 1
    boosted_twist.linear.z = msg.linear.z * 1

    boosted_twist.angular.x = msg.angular.x * 1
    boosted_twist.angular.y = msg.angular.y * 1
    boosted_twist.angular.z = msg.angular.z * 1

    pub.publish(boosted_twist)


if __name__ == '__main__':
    rospy.init_node('boost_cmd_vel', anonymous=True)

    twist_topic = '/raw_cmd_vel' 

    rospy.Subscriber(twist_topic, Twist, twist_callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.spin()