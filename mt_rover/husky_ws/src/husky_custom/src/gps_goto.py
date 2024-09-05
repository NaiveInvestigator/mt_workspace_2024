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
reload(gc)

    
waypoints = [
      [(23.7735930,90.4245048), (0.0, 0.0, 0.0, 1.0)], #middle of aftabnagar field
    
]

lat, lon = 0.0, 0.0

def get_xy_based_on_lat_long(lat,lon):    
    xg2, yg2 = gc.ll2xy(lat,lon,olat,olon)

    return xg2, yg2

def gps_callback(msg):
    global lat, lon
    lat = msg.latitude
    lon = msg.longitude

def goal_pose(pose):
    goal_pose = MoveBaseGoal()

    x, y = get_xy_based_on_lat_long(pose[0][0], pose[0][1])
    rospy.loginfo(str(x) + ", " + str(y))

    goal_pose.target_pose.header.frame_id = 'odom'
    goal_pose.target_pose.pose.position.x = x#pose[0][0]#x
    goal_pose.target_pose.pose.position.y = y#pose[0][1]#y
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
        
        sampling_factor = 1 
        sampled_waypoints = []
        del_lat = pose[0][0] - lat 
        del_lon = pose[0][1] - lon

        next_lat, next_lon = lat, lon 
        for _ in range(sampling_factor):
            next_lat += float(1/sampling_factor) * del_lat
            next_lon += float(1/sampling_factor) * del_lon
            goal = goal_pose([ (next_lat, next_lon), (0.0, 0.0, 0.0, 1.0) ])
            client.send_goal(goal)
            client.wait_for_result()

        clear_global_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        clear_global_costmap()

        # clear_global_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        # clear_global_costmap()

        
