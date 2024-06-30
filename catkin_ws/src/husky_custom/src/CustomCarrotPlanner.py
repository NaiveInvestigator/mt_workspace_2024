#!/usr/bin/env python3

import rospy
from nav_core.base_global_planner import BaseGlobalPlanner
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import math

class CustomCarrotPlanner(BaseGlobalPlanner):
    def __init__(self):
        super(CustomCarrotPlanner, self).__init__()
        rospy.init_node('custom_carrot_planner')

    def plan(self, start, goal):
        path = Path()
        path.header.frame_id = 'map'
        path.poses.append(start)  # Start position
        path.poses.append(goal)   # Goal position

        # Calculate distance and heading
        start_x, start_y = start.pose.position.x, start.pose.position.y
        goal_x, goal_y = goal.pose.position.x, goal.pose.position.y
        distance_to_goal = math.sqrt((goal_x - start_x) ** 2 + (goal_y - start_y) ** 2)
        heading_to_goal = math.atan2(goal_y - start_y, goal_x - start_x)

        # Set a carrot goal some distance ahead of the start
        carrot_goal = PoseStamped()
        carrot_goal.header.frame_id = 'map'
        carrot_goal.pose.position.x = start_x + 0.5 * distance_to_goal * math.cos(heading_to_goal)
        carrot_goal.pose.position.y = start_y + 0.5 * distance_to_goal * math.sin(heading_to_goal)
        carrot_goal.pose.orientation.w = 1.0
        path.poses.append(carrot_goal)

        return path

    def initialize(self, name, costmap, footprint):
        pass

if __name__ == '__main__':
    try:
        planner = CustomCarrotPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
