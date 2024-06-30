#! /usr/bin/env python3
import rospy
from std_msgs.msg import String
import numpy as np
from math import radians, cos, sin, asin, sqrt, degrees

rospy.init_node("move_to")

rover = rospy.Publisher("/rover_control", String, queue_size=10)
status = rospy.Publisher("/status", String, queue_size=10)

yaw = 0.0
lat = 0.0
lon = 0.0

def imu_callback(msg):
    global current_yaw
    current_yaw = float(msg.data)

def gps_callback(msg):
    global lat, lon
    coords = msg.data.split()
    lat = float(coords[0])
    lon = float(coords[1])

imu_sub = rospy.Subscriber("/imu", String, imu_callback)
gps_sub = rospy.Subscriber("/gps", String, gps_callback)

def haversine_distance(curr_lat, curr_lon, target_lat, target_lon):
    radius_earth = 6371000.0
    target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
    
    a = (sin((target_lat - curr_lat) / 2) ** 2) + cos(curr_lat) * cos(target_lat) * (sin((target_lon - curr_lon) / 2)) ** 2
    return radius_earth * 2.0 * asin(sqrt(a))  

def bearing(curr_lat, curr_lon, target_lat, target_lon): #Bearing to waypoint (degrees)
    target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
    d_lon = target_lon - curr_lon
    return np.atan2(sin(d_lon) * cos(target_lat), cos(curr_lat) * sin(target_lat) - (sin(curr_lat) * cos(target_lat) * cos(d_lon)))


def moveTo(target_lat, target_lon, yaw_threshold = 3): #, gps_threshold=0.0000007):
    global lon, lat, current_yaw
    #finding the orientation to rotate to
    distance = haversine_distance(lat, lon, target_lat, target_lon)
    bearing_thing = bearing(lat, lon, target_lat, target_lon)
    #we assume our position to be (0, 0)
    #so the change in position will be x and y
    x = distance * cos(bearing_thing)
    y = distance * sin(bearing_thing)

    target_yaw = degrees(np.arctan2(y, x))
    target_yaw = 90 - target_yaw
    if x < 0 and y > 0:
        target_yaw = 270 - target_yaw
    target_yaw = - target_yaw + 180

    #rotating to the orientation found
    upper_limit = target_yaw + yaw_threshold
    lower_limit = target_yaw - yaw_threshold
    reached = False
    while not reached:
        if current_yaw > upper_limit:
            rover.publish("a")
        elif current_yaw < lower_limit:
            rover.publish("d")
        else:
            if haversine_distance(lat, lon, target_lat, target_lon) > 1.5:
                rover.publish("w")
            else:
                reached = True
                print("Position reached!")

