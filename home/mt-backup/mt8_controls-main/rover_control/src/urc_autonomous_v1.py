#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu, NavSatFix
from rover_control.msg import ArucoInfo
from tf import transformations

from math import radians, cos, sin, asin, sqrt, atan2, degrees
from time import sleep

rospy.init_node("autonomous")

rover = rospy.Publisher("/rover", String, queue_size=10)
status = rospy.Publisher("/status", String, queue_size=10)

img_res = (1280, 720)

yaw = None
lat = None
lon = None

aruco_state, distance, x, y, id = None, None, None, None, None

def distance_from_gps(lat1, lat2, lon1, lon2):
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

    return c * r
     

def haversine_distance(curr_lat, curr_lon, target_lat, target_lon):
    radius_earth = 6371000.0
    target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
    
    a = (sin((target_lat - curr_lat) / 2) ** 2) + cos(curr_lat) * cos(target_lat) * (sin((target_lon - curr_lon) / 2)) ** 2
    return radius_earth * 2.0 * asin(sqrt(a))  

def bearing(curr_lat, curr_lon, target_lat, target_lon): #Bearing to waypoint (degrees)
    target_lat, target_lon, curr_lat, curr_lon = map(radians, [target_lat, target_lon, curr_lat, curr_lon])
    d_lon = target_lon - curr_lon
    return atan2(sin(d_lon) * cos(target_lat), cos(curr_lat) * sin(target_lat) - (sin(curr_lat) * cos(target_lat) * cos(d_lon)))


# Pythagorean distance
# def distance_from_gps(lat1, lat2, lon1, lon2):
#     dist = sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
#     return dist


def imu_callback(msg: Imu):
    global yaw
    yaw = int(msg.data)

def gps_callback(msg):
    global lat, lon
    coords = msg.data.split()
    lat = int(coords[0])
    lon = int(coords[1])

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

def moveTo(target_lat, target_lon):
    y = target_lat - lat
    x = target_lon - lon

    target_yaw = np.arctan2(y, x)

def moveTo(coords, yaw_threshold = 10):  # coords = {"longitude": 0, "latitude": 0}
    global yaw
    target_lat = coords["latitude"]
    target_lon = coords["longitude"]

    # while distance_from_gps(lat, target_lat, 0, 0) > 3 or distance_from_gps(0, 0, lon, target_lon) > 3:
    # while lat > target_lat - 0.000005 and lon > target_lon - 0.000005:
    print("GPS: ", end="")
    print((lon, lat), distance_from_gps(lat, target_lat, lon, target_lon))
    while distance_from_gps(lat, target_lat, lon, target_lon) > 2:
        # control_pub.publish("-") # Needed for Real Rover

        distance = haversine_distance(lat, lon, target_lat, target_lon)
        bearing_thing = bearing(lat, lon, target_lat, target_lon)

        x = distance * cos(bearing_thing)
        y = distance * sin(bearing_thing)

        target_yaw = degrees(np.arctan2(y, x))
        target_yaw = 90 - target_yaw
        if x < 0 and y > 0:
            target_yaw = 270 - target_yaw
        target_yaw = - target_yaw + 180

        upper_limit = target_yaw + yaw_threshold
        lower_limit = target_yaw - yaw_threshold

        d_yaw = abs(target_yaw - yaw)

        print("GPS: ", end="")
        print((lon, lat), distance_from_gps(lat, target_lat, lon, target_lon), '    ', yaw, target_yaw)

        print("   ", abs(target_yaw - yaw))

        print("    ", end="")
        
        if d_yaw > 180:
            d_yaw = 360 - d_yaw

        if d_yaw > 5:
            if yaw > upper_limit:
                control_pub.publish("a")
                print("turning left")
            elif yaw < lower_limit:
                control_pub.publish("d")
                print("turning right")
            else:
                control_pub.publish("w")
                print("forward")

        else:
            control_pub.publish("w")
            print("forward")
                
        # if yaw > upper_limit:
        #     control_pub.publish("a")
        #     print("turning left")
        # elif yaw < lower_limit:
        #     control_pub.publish("d")
        #     print("turning right")
        # else:
        #     control_pub.publish("w")
        #     print("forward")
        rate.sleep()

    print("Reached Target Coords")


def mission(coords, post=False, gate=False):
    global aruco_state, id, distance, x, y
    moveTo(coords)
    if post:
        publish_status("Looking for Aruco Tag")
        while not aruco_state:
            control_pub.publish("a")
        control_pub.publish("-")
        publish_status("Found tag!")
        publish_status(f"ID: {id}")
        
        while distance != None and (distance > 2000 or distance == 0):
            control_pub.publish("-")
            if x == None:
                control_pub.publish("-")
                print("stop")
                rate.sleep()
                continue
            print("Aruco: ", end="")
            if x > ((img_res[0] / 2) + 50):
                control_pub.publish("d")
                publish_status("going right")
            elif x < ((img_res[1] / 2) - 50):
                control_pub.publish("a")
                publish_status("going left")
            elif x < ((img_res[0] / 2) + 50) and x > ((img_res[1] / 2) - 50):
                control_pub.publish("w")
                publish_status("going straight")
            else:
                rover.publish("w")
                #print("going straight")
            
        status_stuff("Reached destination, task completed!")
            

        publish_status("Reached destination, task completed!")
        control_pub.publish("-")
        # for i in range(10):
        #     light.write(b'g')
        #     sleep(0.5)


if __name__ == "__main__":
    # light.write(b'r')
    mission({"longitude": 90.48849806913114, "latitude": 23.84081398801373}, post=True)

# 90.48849806913114, 23.84081398801373
