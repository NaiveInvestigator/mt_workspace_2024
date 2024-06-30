#!/usr/bin/env python3

import rospy
import geonav_transform.geonav_conversions as gc
from sbg_driver.msg import SbgGpsPos 
from nav_msgs.msg import Odometry

lat, lon = 0.0, 0.0

def get_xy_based_on_lat_long(lat,lon):    
    xg2, yg2 = gc.ll2xy(lat,lon,olat,olon)
    return xg2, yg2


def gps_callback(msg):
    global lat, lon
    lat = msg.latitude #23.772564
    lon = msg.longitude# 90.424637

    #converted_x, converted_y = get_xy_based_on_lat_long(lat, lon)

    odom_msg = Odometry()
    odom_msg.header.stamp = rospy.Time.now()
    odom_msg.header.frame_id = 'odom'
    odom_msg.child_frame_id = ''
    odom_msg.pose.pose.position.x = lat#converted_x
    odom_msg.pose.pose.position.y = lon#converted_y
    odom_msg.pose.pose.position.z = 0.0

    odom_msg.pose.pose.orientation.w = 1.0

    odom_msg.twist.twist.linear.x = 0.0 
    odom_msg.twist.twist.linear.y = 0.0
    odom_msg.twist.twist.angular.z = 0.0



    pub.publish(odom_msg)


if __name__ == '__main__':

    rospy.init_node('sbg_gps_ll2xy', anonymous=True)

    rate = rospy.Rate(1) 
    pub = rospy.Publisher('odometry/gps', Odometry, queue_size=10)
    rospy.Subscriber("/sbg/gps_pos", SbgGpsPos, gps_callback)
    

    olat = lat
    olon = lon

    rospy.spin()
    
    

    

    
