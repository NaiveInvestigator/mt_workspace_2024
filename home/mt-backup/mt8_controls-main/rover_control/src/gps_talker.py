#! /usr/bin/env python3

from ublox_gps import UbloxGps
import serial
import rospy
from std_msgs.msg import String
import random
# Can also use SPI here - import spidev
# I2C is not supported

rospy.init_node("gps_talker")

port = serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00', baudrate=38400, timeout=1)
gps = UbloxGps(port)

gps_node = rospy.Publisher("/gps", String, queue_size=10)

def run():
    try: 
        #with open(f"/home/bleep_bloop/Desktop/gps_{int(random.random()*1000000)}.csv", 'w') as fi:
        
        print("Listenting for UBX Messages.")
        while not rospy.is_shutdown():
            try: 
                coords = gps.geo_coords()
                #print(coords.lon, coords.lat, file=fi)
                print("longitude", coords.lon, "lattitude", coords.lat)
                gps_node.publish(str(coords.lon) + " " + str(coords.lat))

            except (ValueError, IOError) as err:
                pass
            except AttributeError:
                pass
    finally:
        port.close()

if __name__ == '__main__':
    run()