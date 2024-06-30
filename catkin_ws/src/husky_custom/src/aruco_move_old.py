#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
from time import sleep

rospy.init_node("aruco_move")

rover = rospy.Publisher("/rover_control", String, queue_size=10)
status = rospy.Publisher("/status", String, queue_size=10)
status_led = rospy.Publisher("/status_indicator", String, queue_size=10)
rover.publish("2")
rate = rospy.Rate(5)

img_res = (640, 480)

aruco_state, distance, x, y, id = 0, 0, 0, 0, 0

def aruco_callback(msg):
    global aruco_state, distance, x, y, id
    data = msg.data.split()
    aruco_state = int(data[0])
    if aruco_state:
        distance = float(data[1])
        x = int(data[2])
        y = int(data[3])
        id = data[4]
        #print(data)

def status_stuff(status_string):
    print(status_string)
    status.publish(status_string)

aruco_sub = rospy.Subscriber("/aruco_tag_info", String, aruco_callback)


#try:
#sleep(4)
while not rospy.is_shutdown():
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
            if distance == None:
                print(distance)
            elif distance > 1.0:    
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
    #else:  
    #    rover.publish("-")
    #    print("stop")
    aruco_state, distance, x, y, id = None, None, None, None, None
    rate.sleep()
    
#except TypeError:   
#pass