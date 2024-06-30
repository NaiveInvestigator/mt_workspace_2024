#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import random
import time

def publish_random_float():
    # Initialize the ROS node
    rospy.init_node('random_float_publisher', anonymous=True)
    
    # Create a publisher for the /uv topic with Float32 message type
    pub = rospy.Publisher('/nitrogen', Float32, queue_size=10)
    pub2 = rospy.Publisher('/phosphorus', Float32, queue_size=10)
    pub3 = rospy.Publisher('/potassium', Float32, queue_size=10)
    
    # Set the loop rate (in Hz)
    rate = rospy.Rate(1)  # 1 Hz
    
    while not rospy.is_shutdown():
        
        # Publish the random float value
        pub.publish(random.uniform(0.0, 100.0))
        pub2.publish(random.uniform(0.0, 100.0))
        pub3.publish(random.uniform(0.0, 100.0))
        
        # Log the published value
        # rospy.loginfo("Published random float value: %.2f", random_float)
        
        # Sleep to maintain the loop rate
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_random_float()
    except rospy.ROSInterruptException:
        pass
