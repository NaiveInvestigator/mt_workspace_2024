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
from geometry_msgs.msg import Twist
reload(gc)

class Aruco:
    aruco_found = False
    def aruco_tag_info_callback(self, msg):
        data = msg.data.split()
        aruco_state = int(data[0])

        if not self.aruco_found:
            if aruco_state:
                self.aruco_found = True

                distance = float(data[1])
                x = int(data[2])
                y = int(data[3])
                id = data[4]

                while client.get_state() not in [2, 3]: #2 -> preempted [interrupted], 3 -> reached goal
                    client.cancel_all_goals()

        else:
            if aruco_state:
                self.aruco_found = True

                distance = float(data[1])
                x = int(data[2])
                y = int(data[3])
                id = data[4]

                if x > ((img_res[0]/2) + 50):
                    msg = Twist()
                    msg.angular.x = 20.0
                    rover.publish(msg)
                    # status_stuff("going right")

                elif x < ((img_res[0]/2) - 50):
                    msg = Twist()
                    msg.angular.x = -20.0
                    rover.publish(msg)
                    # status_stuff("going left")
                elif x < ((img_res[0]/2) + 50) and x > ((img_res[0]/2) - 50):
                    if distance == None:
                        print(distance)
                    elif distance > 1.0:    
                        msg = Twist()
                        msg.linear.x = 100.0
                        rover.publish(msg)
                        # status_stuff("going straight")
                    else:
                        if distance == 0.0:
                            pass
                        else:
                            rover.publish("-")
                            print(distance)
                            # status_stuff("Within 75 cm of tag")
                            post_state = True
                            status_led.publish("g")
                            sleep(2)
                            status_led.publish("g")

            else:
                msg = Twist()
                msg.angular.x = 20.0
                rover.publish(msg)
                print("looking for tag")
                rate.sleep()

        
            #print(data)



class Navigation:
    waypoints = [
        [(23.768098, 90.451271), (0.0, 0.0, 0.0, 1.0)], 
        [(23.768191, 90.45139), (0.0, 0.0, 0.0, 1.0)], 
        # [(49.90000002316203, 8.900138219798626), (0.0, 0.0, 0.0, 1.0)], #straight ahead in sim
        # [(49.900209819263665, 8.900366114225527), (-2.941541948518941e-05, -0.00016291166626070358, 0.33604936980655764, 0.9418443574429575)], #corner in sim but farther
        
    ]

    lat, lon = 0.0, 0.0

    def get_xy_based_on_lat_long(self, lat,lon):    
        xg2, yg2 = gc.ll2xy(lat,lon,olat,olon)

        return xg2, yg2


    def gps_callback(self, msg):
        global lat, lon
        lat = msg.latitude
        lon = msg.longitude

    def goal_pose(self, pose):
        goal_pose = MoveBaseGoal()

        x, y = self.get_xy_based_on_lat_long(pose[0][0], pose[0][1])
        rospy.loginfo(str(x) + ", " + str(y))

        goal_pose.target_pose.header.frame_id = 'odom'
        goal_pose.target_pose.pose.position.x = x#pose[0][0]#x
        goal_pose.target_pose.pose.position.y = y#pose[0][1]#y
        goal_pose.target_pose.pose.position.z = 0
        goal_pose.target_pose.pose.orientation.x = pose[1][0]
        goal_pose.target_pose.pose.orientation.y = pose[1][1]
        goal_pose.target_pose.pose.orientation.z = pose[1][2]
        goal_pose.target_pose.pose.orientation.w = pose[1][3]

        # goal_id = GoalID()  
        # goal_id.id = "my_goal" 
        # goal_pose.goal_id = goal_id 

        return goal_pose, x, y

class SearchPattern:
    def search_pattern(self, X, Y):
        deltas = [4, 8, 12, 16, 20]

        for delta in deltas:

            pattern = [(0, delta), (delta, 0), (0, -delta), (-delta, 0), (0, delta)] # north, east, south, west, north

            for del_x, del_y in pattern:
                goal = MoveBaseGoal()
                goal.target_pose.header.frame_id = 'odom'
                goal.target_pose.pose.position.x = X + del_x
                goal.target_pose.pose.position.y = Y + del_y
                goal.target_pose.pose.position.z = 0
                goal.target_pose.pose.orientation.x = 0.0
                goal.target_pose.pose.orientation.y = 0.0
                goal.target_pose.pose.orientation.z = 0.0
                goal.target_pose.pose.orientation.w = 1.0

                client.send_goal(goal)
                while client.get_state() not in [2, 3]: #2 -> preempted [interrupted], 3 -> reached goal
                    pass
                    # client.cancel_all_goals()

                clear_global_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
                clear_global_costmap()

if __name__ == '__main__':
    rospy.init_node('patrol')

    img_res = (640, 480)

    navigation = Navigation()
    search_pattern = SearchPattern()
    # aruco = Aruco()

    gps_sub = rospy.Subscriber("/navsat/fix", NavSatFix, navigation.gps_callback)
    # aruco_tag_info = rospy.Subscriber("/aruco_tag_info", String, aruco.aruco_tag_info_callback)

    rover = rospy.Publisher("/cmd_vel", String, queue_size=10)
    status = rospy.Publisher("/status", String, queue_size=10)
    status_led = rospy.Publisher("/status_indicator", String, queue_size=10)
    rover.publish("2")
    rate = rospy.Rate(5)

    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    print("Obtaining origin gps coords")
    sleep(3)
    olat = lat
    olon = lon
    print("Obtained")

    a = 0

    for pose in navigation.waypoints:
        
        sampling_factor = 1 
        sampled_waypoints = []
        del_lat = pose[0][0] - lat 
        del_lon = pose[0][1] - lon

        next_lat, next_lon = lat, lon 
        center_x, center_y = 0.0, 0.0
        for _ in range(sampling_factor):
            next_lat += float(1/sampling_factor) * del_lat
            next_lon += float(1/sampling_factor) * del_lon
            goal, center_x, center_y = navigation.goal_pose([ (next_lat, next_lon), (0.0, 0.0, 0.0, 1.0) ])
            client.send_goal(goal)

            while client.get_state() not in [2, 3]: #2 -> preempted [interrupted], 3 -> reached goal
                pass
                # client.cancel_all_goals()
            
        clear_global_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', Empty)
        clear_global_costmap()
        # search_pattern.search_pattern(center_x, center_y)

        
