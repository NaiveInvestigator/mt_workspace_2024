#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from importlib import reload
import geonav_transform.geonav_conversions as gc
from sensor_msgs.msg import NavSatFix
from time import sleep
reload(gc)

def goal_pose():
    goal_pose = MoveBaseGoal()

    x, y = 0.0, 10.0
    rospy.loginfo(str(x) + ", " + str(y))

    goal_pose.target_pose.header.frame_id = 'odom'
    goal_pose.target_pose.pose.position.x = x
    goal_pose.target_pose.pose.position.y = y
    goal_pose.target_pose.pose.position.z = 0
    goal_pose.target_pose.pose.orientation.x = 0.0
    goal_pose.target_pose.pose.orientation.y = 0.0
    goal_pose.target_pose.pose.orientation.z = 0.0
    goal_pose.target_pose.pose.orientation.w = 1.0
    return goal_pose


if __name__ == '__main__':
    rospy.init_node('patrol')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    goal = goal_pose()
    client.send_goal(goal)
    client.wait_for_result()
