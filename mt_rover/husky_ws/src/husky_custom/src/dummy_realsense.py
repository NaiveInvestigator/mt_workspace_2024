#!/usr/bin/env python3

import rospy
import std_msgs.msg
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField

def publish_dummy_pointcloud():
    # Initialize ROS node
    rospy.init_node('dummy_realsense', anonymous=True)

    # Create a publisher for the sensor_msgs/PointCloud2 topic
    pub = rospy.Publisher('/realsense/depth/color/points', PointCloud2, queue_size=10)

    # Set the rate at which to publish the point cloud (e.g., 1 Hz)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        # Create a dummy point cloud data (x, y, z)
        points = [(1.0, 2.0, 3.0), (4.0, 5.0, 6.0), (7.0, 8.0, 9.0)]

        # Create the fields for the PointCloud2 message
        fields = [
            PointField(name="x", offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name="y", offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name="z", offset=8, datatype=PointField.FLOAT32, count=1),
        ]

        # Create the PointCloud2 message
        header = std_msgs.msg.Header(frame_id="base_link")
        pc_data = pc2.create_cloud_xyz32(header, points)
        # Publish the dummy point cloud
        pub.publish(pc_data)

        # Sleep to maintain the desired publishing rate
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_dummy_pointcloud()
    except rospy.ROSInterruptException:
        pass
