#! /usr/bin/env python3

import rospy
from std_msgs.msg import String, Float32
from sensor_msgs.msg import Imu, NavSatFix
from tf import transformations
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from time import sleep
from sbg_driver.msg import SbgGpsPos, SbgEkfEuler
import numpy as np
import time
import math

rospy.init_node("gps_goto")
status = rospy.Publisher("/status", String, queue_size=10)

yaw = 0.0
lat = 0.0
lon = 0.0

lin_vel = 60
ang_vel = 10

forward = Twist()
left = Twist()
right = Twist()
backward = Twist()
stop = Twist()

forward.linear.x = lin_vel
left.angular.z = ang_vel
right.angular.z = -ang_vel
backward.linear.x = -lin_vel

rate = rospy.Rate(5)

distance_threshold = 1.5
aruco_state = 0.0

coords = [
    [23.768117803, 90.45166206],
    [23.768347348, 90.45154665],
    [23.768503124, 90.451401091]
]

class Callbacks():
    def sbg_euler(self, msg: SbgEkfEuler):
        global yaw
        yaw = degrees(msg.angle.z)

    def gps_callback(self, msg: SbgGpsPos):
        global lat, lon
        lat = msg.latitude
        lon = msg.longitude

    def status_stuff(self, status_string):
        print(status_string)
        status.publish(status_string)

    def obstacle_presence_callback(self, msg):
        global obstacle_presence 
        obstacle_presence = msg.data

    # def aruco_reached_callback(self, msg):
    #     global aruco_reached 
    #     aruco_reached = msg.data

    def aruco_tag_info_callback(self, msg):
        global aruco_state
        data = msg.data.split()
        aruco_state = int(data[0])

class Navigation():
    def distance_from_gps(self, lat1, lat2, lon1, lon2):
        #radius of earth in kilometers
        r = 6371

        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        
        #Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))

        return c * r * 1000
     

    def haversine_distance(self, curr_lat, curr_lon, target_lat, target_lon):
        radius_earth = 6371000.0
        target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
        
        a = (sin((target_lat - curr_lat) / 2) ** 2) + cos(curr_lat) * cos(target_lat) * (sin((target_lon - curr_lon) / 2)) ** 2
        return radius_earth * 2.0 * asin(sqrt(a))  

    def bearing(self, curr_lat, curr_lon, target_lat, target_lon): #Bearing to waypoint (degrees)
        target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
        d_lon = target_lon - curr_lon
        return degrees(atan2(sin(d_lon) * cos(target_lat), cos(curr_lat) * sin(target_lat) - (sin(curr_lat) * cos(target_lat) * cos(d_lon))))
    
    def moveTo(self, coords, yaw_threshold = 10, avoid_obstacles = False, perform_search = False):  # coords = {"longitude": 0, "latitude": 0}
        global yaw, lat, lon, distance_threshold
        target_lat = coords[0]
        target_lon = coords[1]

        callbacks.status_stuff("GPS: ")
        callbacks.status_stuff(f"Distance to target: {navigation.distance_from_gps(lat, target_lat, lon, target_lon)}")

        obstacle_avoidance_turning = False
        while navigation.distance_from_gps(lat, target_lat, lon, target_lon) > distance_threshold:
            if avoid_obstacles:
                if obstacle_presence:
                    rover.publish(left)
                    callbacks.status_stuff("turning left to avoid obstacle")
                    obstacle_avoidance_turning = True
                    obstacle_avoidance_forward_end_time = time.time() + 5.0
                    continue

                if obstacle_avoidance_turning:
                    if time.time() <= obstacle_avoidance_forward_end_time:
                        rover.publish(forward)
                        callbacks.status_stuff("moving forward to avoid obstacle")
                        continue
                    else:
                        obstacle_avoidance_turning = False

            # self.square_search()
            #print("Normal navigation")


            # rover.publish(forward)
            # rover.publish(stop) # Needed for Real Rover

            distance = navigation.haversine_distance(lat, lon, target_lat, target_lon)
            target_yaw = navigation.bearing(lat, lon, target_lat, target_lon)

            upper_limit = target_yaw + yaw_threshold
            lower_limit = target_yaw - yaw_threshold

            d_yaw = abs(target_yaw - yaw)

            callbacks.status_stuff("GPS: ")
            callbacks.status_stuff(f"lat: {lat}, lon: {lon}")
            callbacks.status_stuff(f"Distance to target: {navigation.distance_from_gps(lat, target_lat, lon, target_lon)}")
            callbacks.status_stuff(f"current yaw: {yaw}, target yaw: {target_yaw}")
            callbacks.status_stuff(f"angle left: {abs(target_yaw - yaw)}")
            callbacks.status_stuff("")

            if d_yaw > 180:
                d_yaw = 360 - d_yaw

            if d_yaw > 5:
                if yaw > upper_limit:
                    rover.publish(left)
                    callbacks.status_stuff("turning left")
                elif yaw < lower_limit:
                    rover.publish(right)
                    callbacks.status_stuff("turning right")
                else:
                    rover.publish(forward)
                    callbacks.status_stuff("forward")

            else:
                rover.publish(forward)
                callbacks.status_stuff("forward")
                    
            rate.sleep()

        callbacks.status_stuff("Reached Target Coords")
        rover.publish(stop)

        if perform_search:
            for dist in [4, 8, 12, 16, 20]:
                self.hex_search(lat, lon, dist)

    def square_search(self, lat = None, lon = None, distance = None):
        while aruco_state:
            print("Paused")
            pass
        print("Searching...")
        # callbacks.status_stuff("Searching...")

        R = 6378137

        # Convert distance from meters to degrees
        delta_lat = distance / R * (180 / math.pi)
        delta_lon = distance / (R * math.cos(math.pi * lat / 180)) * (180 / math.pi)

        # North
        new_lat_north = lat + delta_lat
        new_lon_north = lon

        # South
        new_lat_south = lat - delta_lat
        new_lon_south = lon

        # East
        new_lat_east = lat
        new_lon_east = lon + delta_lon

        # West
        new_lat_west = lat
        new_lon_west = lon - delta_lon


        self.moveTo([new_lat_north, new_lon_north])
        sleep(2)
        self.moveTo([new_lat_east, new_lon_east])
        sleep(2)
        self.moveTo([new_lat_south, new_lon_south])
        sleep(2)
        self.moveTo([new_lat_west, new_lon_west])
        sleep(2)

    def hex_search(self, lat = None, lon = None, distance = None):
        while aruco_state:
            print("Paused")
            pass
        print("Searching...")
        # callbacks.status_stuff("Searching...")

        R = 6371.0
    
        points = []

        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)

            delta_lat = ((distance / 1000)  / R) * (180 / math.pi) * math.cos(angle_rad)
            delta_lon = ((distance / 1000)  / R) * (180 / math.pi) * math.sin(angle_rad) / math.cos(math.radians(lat))
            
            vertex_lat = lat + delta_lat
            vertex_lon = lon + delta_lon
        
            points.append([vertex_lat, vertex_lon])
    
        for point in points:
            self.moveTo(point)
            sleep(2)


if __name__ == "__main__":
    navigation = Navigation()
    callbacks = Callbacks()

    obstacle_presence = 0.0

    yaw_sub = rospy.Subscriber("/sbg/ekf_euler", SbgEkfEuler, callbacks.sbg_euler)
    gps_sub = rospy.Subscriber("/sbg/gps_pos", SbgGpsPos, callbacks.gps_callback)
    rover = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    status_led = rospy.Publisher("/status_indicator", String, queue_size=10)
    obstacle_presence_sub = rospy.Subscriber("/obstacle_presence", Float32, callbacks.obstacle_presence_callback)
    # aruco_reached_sub = rospy.Subscriber("/aruco_reached", Float32, callbacks.aruco_reached_callback)
    aruco_tag_info_sub = rospy.Subscriber("/aruco_tag_info", String, callbacks.aruco_tag_info_callback)

    for coord in coords:
        navigation.moveTo(coords=coord, perform_search=True)
        print("next point")
        sleep(2)