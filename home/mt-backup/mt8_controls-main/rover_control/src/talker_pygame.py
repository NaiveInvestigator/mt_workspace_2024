#! /usr/bin/env python3

import pygame
from time import sleep 
import rospy
from std_msgs.msg import String

rospy.init_node("base_station")
pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("controller")

base = rospy.Publisher("/rover", String, queue_size=10)

up = 119
down = 115
left = 97
right = 100

directions = [up, down, left, right]
dir_states = [False, False, False, False]
#outputs = ["up", "down", "left", "right"]
outputs = ["w", "s", "a", "d"]

def controller():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pressed = directions.index(event.key)
                dir_states[pressed] = True
            elif event.type == pygame.KEYUP:
                released = directions.index(event.key)
                dir_states[released] = False
        for dir in dir_states:
            if dir == True:
                print(outputs[dir_states.index(dir)])
                base.publish(outputs[dir_states.index(dir)])
        sleep(0.05)
            
if __name__ == "__main__":
    controller()
