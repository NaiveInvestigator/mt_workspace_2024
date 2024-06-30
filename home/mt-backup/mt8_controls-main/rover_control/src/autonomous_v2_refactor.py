#! /usr/bin/env python3
import rospy

from std_msgs.msg import String
from sensor_msgs.msg import Imu, NavSatFix

import numpy as np
from math import radians, cos, sin, asin, sqrt, degrees, atan2

rospy.init_node("autonomous")

rover = rospy.Publisher("/rover_control", String, queue_size=10)
status = rospy.Publisher("/status", String, queue_size=10)
rate = rospy.Rate(1)

rover.publish("2")

yaw = 0.0
lat = 0.0
lon = 0.0

current_yaw = 0
img_res = (640, 480)
aruco_state, distance, x, y, id = 0, 0, 0, 0, 0


def imu_callback(msg: Imu):
    global current_yaw

    x, y, z, w = msg.orientation.values()

    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)

    yaw = degrees(atan2(siny_cosp, cosy_cosp)) * -1
    if yaw < 0:
        yaw += 360

    current_yaw = yaw


def gps_callback(msg: NavSatFix):
    global lat, lon
    lat = msg.latitude
    lon = msg.longitude


def aruco_callback(msg):
    global aruco_state, distance, x, y, id
    data = msg.data.split()
    aruco_state = int(data[0])
    if aruco_state:
        distance = float(data[1])
        x = int(data[2])
        y = int(data[3])
        id = data[4]


def publishStatus(status_string):
    print(status_string)
    status.publish(status_string)


imu_sub = rospy.Subscriber("/imu", Imu, imu_callback)
gps_sub = rospy.Subscriber("/gps", NavSatFix, gps_callback)
aruco_sub = rospy.Subscriber("/aruco_tag_info", String, aruco_callback)


def haversine_distance(curr_lat, curr_lon, target_lat, target_lon):
    radius_earth = 6371000.0
    target_lat, target_lon, curr_lat, curr_lon = map(
        radians, [target_lat, target_lon, curr_lat, curr_lon]
    )

    a = (sin((target_lat - curr_lat) / 2) ** 2) + cos(curr_lat) * cos(target_lat) * (
        sin((target_lon - curr_lon) / 2)
    ) ** 2
    return radius_earth * 2.0 * asin(sqrt(a))


def getBearing(curr_coords, target_coords):  # [lat, lon]
    [la2, lo2] = map(radians, target_coords)
    [la1, lo1] = map(radians, curr_coords)

    y = sin(lo2 - lo1) * cos(la2)
    x = cos(la1) * sin(la2) - sin(la1) * cos(la2) * cos(lo2 - lo1)

    bearing = degrees(atan2(y, x))

    if bearing < 0:  # normalise to 0-360
        bearing += 360

    return bearing


def moveTo(target_lat, target_lon, yaw_threshold=7):  # , gps_threshold=0.0000007):
    global lon, lat, current_yaw
    reached = False
    while not reached:
        # finding the orientation to rotate to
        print(f"Position: {lat}, {lon}  Target: {target_lat}, {target_lon}")
        distance = haversine_distance(lat, lon, target_lat, target_lon)
        bearing = getBearing([lat, lon], [target_lat, target_lon])
        # bearing_thing = degrees(bearing(lat, lon, target_lat, target_lon))

        heading_delta = bearing - yaw
        if abs(heading_delta) > 180:
            heading_delta = 360 - abs(heading_delta)

        print(
            f"Distance: {distance}  Bearing: {bearing}  Heading: {current_yaw}  Delta: {heading_delta}"
        )

        if distance < 1.0:
            reached = True
            print("Position reached!")
            break

        if heading_delta > yaw_threshold:
            goRight()
        elif heading_delta < -yaw_threshold:
            goLeft()
        else:
            goStraight()

        rate.sleep()
        rover.publish("-")

def goStraight():
    rover.publish("s")
    publishStatus("Fwrd")

def goLeft():
    rover.publish("a")
    publishStatus("Left")

def goRight():
    rover.publish("d")
    publishStatus("Rght")

def mission(target_lat, target_lon, post=False):
    global aruco_state, distance, x, y, id, lon, lat, current_yaw
    moveTo(target_lat, target_lon)
    if post == True:
        post_state = False
        while not post_state:
            if x == None:
                rover.publish("-")
                print("stop")
                rate.sleep()
                continue
            if x > ((img_res[0] / 2) + 50):
                rover.publish("d")
                publishStatus("going left")
            elif x < ((img_res[1] / 2) - 50):
                rover.publish("a")
                publishStatus("going right")
            elif x < ((img_res[0] / 2) + 50) and x > ((img_res[1] / 2) - 50):
                if distance > 1.5:
                    rover.publish("w")
                    publishStatus("going straight")
                else:
                    rover.publish("-")
                    post_state = True
            else:
                rover.publish("-")
                print("stop")
            aruco_state, distance, x, y, id = None, None, None, None, None
            rate.sleep()


if __name__ == "__main__":
    rover.publish("2")
    target_lat = 23.7750393
    target_lon = 90.4089058
    # mission(target_lat, target_lon, post = False)
    moveTo(target_lon, target_lat)
