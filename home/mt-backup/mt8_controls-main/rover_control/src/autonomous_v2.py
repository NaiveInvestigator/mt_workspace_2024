#! /usr/bin/env python3
import rospy
from std_msgs.msg import String
import numpy as np
from math import radians, cos, sin, asin, sqrt, degrees
from time import sleep

rospy.init_node("autonomous")

rover = rospy.Publisher("/rover_control", String, queue_size=10)
status = rospy.Publisher("/status", String, queue_size=10)
status_led = rospy.Publisher("/status_indicator", String, queue_size=10)
rate = rospy.Rate(5)

rover.publish("4")

yaw = 0.0
lat = 0.0
lon = 0.0

current_yaw = 0
img_res = (640, 480)
aruco_state, distance, x, y, id = 0, 0, 0, 0, 0

def imu_callback(msg):
    global current_yaw
    current_yaw = float(msg.data)

def gps_callback(msg):
    global lat, lon
    coords = msg.data.split()
    lon = float(coords[0])
    lat = float(coords[1])

def aruco_callback(msg):
    global aruco_state, distance, x, y, id
    data = msg.data.split()
    aruco_state = int(data[0])
    if aruco_state:
        distance = float(data[1])
        x = int(data[2])
        y = int(data[3])
        id = data[4]

def status_stuff(status_string):
    print(status_string)
    status.publish(status_string)

imu_sub = rospy.Subscriber("/imu", String, imu_callback)
gps_sub = rospy.Subscriber("/gps", String, gps_callback)
aruco_sub = rospy.Subscriber("/aruco_tag_info", String, aruco_callback)

def haversine_distance(curr_lat, curr_lon, target_lat, target_lon):
    radius_earth = 6371000.0
    target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
    
    a = (sin((target_lat - curr_lat) / 2) ** 2) + cos(curr_lat) * cos(target_lat) * (sin((target_lon - curr_lon) / 2)) ** 2
    return radius_earth * 2.0 * asin(sqrt(a))  

def bearing(curr_lat, curr_lon, target_lat, target_lon): #Bearing to waypoint (degrees)
    target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
    d_lon = target_lon - curr_lon
    print("first term:", sin(d_lon) * cos(target_lat))
    print("second term:", cos(curr_lat) * sin(target_lat) - (sin(curr_lat) * cos(target_lat) * cos(d_lon)))

    return np.arctan2(sin(d_lon) * cos(target_lat), cos(curr_lat) * sin(target_lat) - (sin(curr_lat) * cos(target_lat) * cos(d_lon)))


def moveTo(target_lat, target_lon, yaw_threshold = 7): #, gps_threshold=0.0000007):
    global lon, lat, current_yaw
    reached = False
    while not reached:
        #finding the orientation to rotate to
        print("target lat", target_lat)
        print("target lon", target_lon)
        print("lat", lat)
        print("lon", lon)
        distance = haversine_distance(lat, lon, target_lat, target_lon)
        bearing_thing = degrees(bearing(lat, lon, target_lat, target_lon))

        print("Distance to be travelled: ", distance)
        print("Bearing Angle: ", bearing_thing)
        print("Current Heading: ", current_yaw)

        #rotarightting to the orientation found
        upper_limit = bearing_thing + yaw_threshold
        lower_limit = bearing_thing - yaw_threshold
        #print(lat, lon, target_yaw)
        if haversine_distance(lat, lon, target_lat, target_lon) < 1.0:
            reached = True
            print("Position reached!")
        else:
            if current_yaw < upper_limit and current_yaw > lower_limit:
                rover.publish("s")
                print("stright")

            if current_yaw > upper_limit:
                rover.publish("a")
                print("left")    

            elif current_yaw < lower_limit:
                rover.publish("d")
                print("right")

        #rover.publish("-")
        rate.sleep()

def mission(target_lat, target_lon, post=False):
    global aruco_state, distance, x, y, id, lon, lat, current_yaw
    moveTo(target_lat, target_lon)
    if post == True:
        post_state = False
        while not post_state:
            if aruco_state == 0:
                rover.publish("a")
                print("looking for tag")
                rate.sleep()
            else:
            
            #if x == None:
                #rover.publish("a")
            #    rover.publish("-")
            #    print("looking for tag")
            #    rate.sleep()
            #    continue
                if x > ((img_res[0]/2) + 50):
                    rover.publish("d")
                    status_stuff("going right")
                elif x < ((img_res[0]/2) - 50):
                    rover.publish("a")
                    status_stuff("going left")
                elif x < ((img_res[0]/2) + 50) and x > ((img_res[0]/2) - 50):
                    if distance > 1.0:    
                        rover.publish("s")
                        status_stuff("going straight")
                    else:
                        if distance == 0.0:
                            pass
                        else:
                            rover.publish("-")
                            print(distance)
                            status_stuff("Within 75 cm of tag")
                            post_state = True
                            status_led.publish("g")
                            sleep(2)
                            status_led.publish("g")
                            break
                #rover.publish("-")
                rate.sleep()

if __name__ == "__main__":
    rover.publish("4")
    coords = [[90.4090382, 23.7752259, 1]]
             # [90.409118, 23.774902, 1],
              #[90.408928, 23.774916, 1, 0],
              #[90.408882, 23.775116, 0, 0],
              #[90.408881, 23.775208, 0, 0],
              ##[90.409081, 23.775224, 0, 0],
              #[90.409296, 23.775331, 0, 0]]
    #mission(target_lat, target_lon, post = False)
    for coord in coords:
        mission(target_lon=coord[0], target_lat=coord[1], post=bool(coord[2]))
    # target_lon = 90.4084602
    # target_lat = 23.7751482


    # target_lon = 90.4086416
    # target_lat = 23.7750943
