#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from importlib import reload
import geonav_transform.geonav_conversions as gc
from sensor_msgs.msg import NavSatFix
from time import sleep
import roslaunch
import rospkg
from std_msgs.msg import String
from std_srvs.srv import Empty
from std_srvs.srv import SetBool
from actionlib_msgs.msg import GoalID
reload(gc)

if __name__ == '__main__':
    rospy.init_node('patrol_2')
    
    pub = rospy.Publisher('/cancel_msg', String, queue_size=10)

    
