#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

a = 0

def twist_callback(msg):

    global a

    boosted_twist = Twist()
    boosted_twist.linear.x = msg.linear.x * 100
    boosted_twist.linear.y = msg.linear.y * 100
    boosted_twist.linear.z = msg.linear.z * 100

    boosted_twist.angular.x = msg.angular.x * 10
    boosted_twist.angular.y = msg.angular.y * 10
    boosted_twist.angular.z = msg.angular.z * 10

    pub.publish(boosted_twist)

twist_topic = '/raw_cmd_vel'
rospy.Subscriber(twist_topic, Twist, twist_callback)
if __name__ == '__main__':
    rospy.init_node('boost_cmd_vel', anonymous=True)

    #twist_topic = '/raw_cmd_vel' 

    #rospy.Subscriber(twist_topic, Twist, twist_callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.spin()
