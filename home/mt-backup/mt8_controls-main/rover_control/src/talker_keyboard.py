#!/usr/bin/env python3
# license removed for brevity

import rospy
from std_msgs.msg import String
from time import sleep
from pynput import keyboard

def talker():
    global publisher
    rospy.init_node('talker_keyboard')
    rover_topic = rospy.get_param('~topic', "/rover_control")
    publisher = rospy.Publisher(rover_topic, String, queue_size=10)
    print(rover_topic)

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        rate.sleep()


def move(instruction_key):
    rospy.loginfo(instruction_key)
    publisher.publish(instruction_key)


def on_press(key):
    try:
        msg = str(key.char)
        move(msg if msg.isnumeric() else (msg))
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    move('-')


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
