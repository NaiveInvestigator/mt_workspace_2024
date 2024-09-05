#!/bin/bash
export ROS_WS=~/catkin_ws
source /opt/ros/noetic/setup.bash
source $ROS_WS/devel/setup.bash
export PATH=$ROS_ROOT/bin:$PATH
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:$ROS_WS
export ROS_MASTER_URI=http://192.168.1.69:11311
export ROS_HOSTNAME=192.168.1.69
exec "$@"
