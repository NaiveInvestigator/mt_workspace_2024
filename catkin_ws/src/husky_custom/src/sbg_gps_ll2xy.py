#!/usr/bin/env python3

import rospy
import geonav_transform.geonav_conversions as gc
from sbg_driver.msg import SbgGpsPos 
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix

lat, lon = 0.0, 0.0

# def get_xy_based_on_lat_long(lat,lon):    
#     xg2, yg2 = gc.ll2xy(lat,lon,olat,olon)
#     return xg2, yg2

def gps_callback(msg):
    global lat, lon

    lat = msg.latitude
    lon = msg.longitude

    navsat_fix_msg = NavSatFix()
    navsat_fix_msg.header.stamp = rospy.Time.now()
    navsat_fix_msg.header.frame_id = "base_link"
    navsat_fix_msg.latitude = lat 
    navsat_fix_msg.longitude = lon 
    navsat_fix_msg.altitude = 0.0 

    pub.publish(navsat_fix_msg)


if __name__ == '__main__':

    rospy.init_node('sbg_gps_ll2xy', anonymous=True)

    rate = rospy.Rate(1) 
    pub = rospy.Publisher('navsat/fix', NavSatFix, queue_size=10)
    rospy.Subscriber("/sbg/gps_pos", SbgGpsPos, gps_callback)

    olat = lat
    olon = lon

    rospy.spin()
    
    

    

    
