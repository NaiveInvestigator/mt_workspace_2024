#!/usr/bin/env bash

# Set up the environment for the rover

/opt/ros/melodic/setup.bash
source /home/mt2023/catkin_ws/devel/setup.bash

export ROS_MASTER_URI=http://192.168.1.21:11311/
export ROS_IP=192.168.1.69

exec "$@"
