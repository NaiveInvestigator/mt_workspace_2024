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
      [(23.761641061,90.361271509), (0.0, 0.0, 0.0, 1.0)], # the goal on ayats roof

      # [(23.761584059, 90.361292699), (0.0, 0.0, 0.0, 1.0)],

    # [(49.90000002316203, 8.900138219798626), (0.0, 0.0, 0.0, 1.0)],
    # [(49.90008921739303, 8.900038095765511), (0.00019772838047951615, 0.00022398924668489507, 0.3762643805695495, 0.9265122916869036)]

    #  [(49.90007048483718, 8.900112803835821), (0.00019772838047951615, 0.00022398924668489507, 0.3762643805695495, 0.9265122916869036)],

    #  [(49.90033209986483, 8.900137446256416), (0.0, 0.0, 0.0, 1.0)],

    #[(49.9003918098503, 8.900446367629215), (0.0, 0.0, 0.0, 1.0)],
    # [(49.900209819263665, 8.900366114225527), (-2.941541948518941e-05, -0.00016291166626070358, 0.33604936980655764, 0.9418443574429575)], #corner in sim but farther
    # [(49.899909078258815, 8.899860248020227), (0.0, 0.0, 0.0, 1.0)], #opposite corner in sim 
    # [(49.90001443293687,8.899868073027013), (0.0, 0.0, 0.0, 1.0)], #behind the rover in sim 
    # [(49.90002111967998, 8.899700114542261), (0.0, 0.0, 0.0, 1.0)], #behind the rover in sim but farther
    # [(49.900077484388156,8.90012160444783), (0.0 , 0.0, 0.0, 1.0)], #corner in sim
    # [(49.90002111967998,8.899700114542261), (0.0, 0.0, 0.0, 1.0)], #behind the rover in sim but farther
    
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

    # rospack = rospkg.RosPack()
    # package_path = rospack.get_path("husky_custom")
    # launch_move_base = roslaunch.parent.ROSLaunchParent(rospy.get_param('/run_id'), [f"{package_path}/launch/move_base_fr.launch"])
    # launch_move_base.start()
    # launch_move_base.spin()

    gps_sub = rospy.Subscriber("/navsat/fix", NavSatFix, gps_callback)
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    print("Obtaining origin gps coords")
    sleep(3)
    olat = lat
    olon = lon
    print("look here", lat, lon)
    print("Obtained")

    # for pose in waypoints:
    #     goal = goal_pose(pose)
    #     client.send_goal(goal)
    #     client.wait_for_result()

    #for intermediate sampling during long journeys

    while True:

        # inp_lat = float(input("Enter target latitude: "))
        # inp_lon = float(input("Enter target longitude: "))

        try:
            inp_lat, inp_lon = list(map(float, input("Enter target latitude, longitude: ").split(",")))
        except:
            print("Session complete.")
            break

        if inp_lat is None or inp_lon is None:
            print("Session complete.")
            break

        sampling_factor = 1 
        sampled_waypoints = []
        del_lat = inp_lat - lat 
        del_lon = inp_lon - lon

        next_lat, next_lon = lat, lon 
        for _ in range(sampling_factor):
            next_lat += float(1/sampling_factor) * del_lat
            next_lon += float(1/sampling_factor) * del_lon
            goal = goal_pose([ (next_lat, next_lon), (0.0, 0.0, 0.0, 1.0) ])

            clear_global_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
            clear_global_costmap()
            
            client.send_goal(goal)
            client.wait_for_result()

        clear_global_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        clear_global_costmap()

    # for pose in waypoints:
        
    #     sampling_factor = 1 
    #     sampled_waypoints = []
    #     del_lat = pose[0][0] - lat 
    #     del_lon = pose[0][1] - lon

    #     next_lat, next_lon = lat, lon 
    #     for _ in range(sampling_factor):
    #         next_lat += float(1/sampling_factor) * del_lat
    #         next_lon += float(1/sampling_factor) * del_lon
    #         goal = goal_pose([ (next_lat, next_lon), (0.0, 0.0, 0.0, 1.0) ])
    #         client.send_goal(goal)
    #         client.wait_for_result()

    #     clear_global_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
    #     clear_global_costmap()

        
