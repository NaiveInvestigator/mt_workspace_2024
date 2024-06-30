#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from importlib import reload
import geonav_transform.geonav_conversions as gc
from sensor_msgs.msg import NavSatFix
from time import sleep
reload(gc)

# waypoints = [
#     [(3.0, 5.0, 0.0), (0.0, 0.0, 0.0, 1.0)],
#     [(1.0, 6.0, 0.0), (0.0, 0.0, -0.984047240305, 0.177907360295)]
#     ]
    
waypoints = [
    [(49.90000002316203, 8.900138219798626), (0.0, 0.0, 0.0, 1.0)],
    [(49.90008921739303, 8.900038095765511), (0.0, 0.0, -0.984047240305, 0.177907360295)]
    ]

lat, lon = 0.0, 0.0

def get_xy_based_on_lat_long(lat,lon):    
    xg2, yg2 = gc.ll2xy(lat,lon,olat,olon)
    utmy, utmx, utmzone = gc.LLtoUTM(lat,lon)

    rospy.loginfo("#########   ###########")  
    rospy.loginfo("LAT COORDINATES ==>"+str(lat)+","+str(lon))  
    rospy.loginfo("COORDINATES XYZ ==>"+str(xg2)+","+str(yg2))
    rospy.loginfo("COORDINATES UTM==>"+str(utmx)+","+str(utmy))

    return xg2, yg2

def gps_callback(msg):
    global lat, lon
    lat = msg.latitude
    lon = msg.longitude

def goal_pose(pose):
    goal_pose = MoveBaseGoal()

    x, y = get_xy_based_on_lat_long(pose[0][0], pose[0][1])

    goal_pose.target_pose.header.frame_id = 'odom'
    goal_pose.target_pose.pose.position.x = x
    goal_pose.target_pose.pose.position.y = y
    goal_pose.target_pose.pose.position.z = 0
    goal_pose.target_pose.pose.orientation.x = pose[1][0]
    goal_pose.target_pose.pose.orientation.y = pose[1][1]
    goal_pose.target_pose.pose.orientation.z = pose[1][2]
    goal_pose.target_pose.pose.orientation.w = pose[1][3]
    return goal_pose


if __name__ == '__main__':
    rospy.init_node('patrol')
    gps_sub = rospy.Subscriber("/navsat/fix", NavSatFix, gps_callback)
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    print("Obtaining origin gps coords")
    sleep(3)
    olat = lat
    olon = lon
    print("Obtained")

    for pose in waypoints:
        goal = goal_pose(pose)
        client.send_goal(goal)
        client.wait_for_result()