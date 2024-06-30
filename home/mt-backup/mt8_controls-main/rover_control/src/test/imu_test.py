import pyrealsense2 as rs
import numpy as np
class DepthCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.accel)
        config.enable_stream(rs.stream.gyro)


        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        data_frame = frames.get_data()


        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        #accel = self.accel_data(frames[0].as_motion_frame().get_motion_data())
        #gyro = self.gyro_data(frames[1].as_motion_frame().get_motion_data())
        
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image #, accel, gyro
    
    def gyro_data(self): #gyro):
        frames = self.pipeline.wait_for_frames()
        for frame in frames:
            print(frame.as_motion_frame().get_motion_data())
        #return np.asarray([gyro.x, gyro.y, gyro.z])

    def accel_data(self):#, accel):
        frames = self.pipeline.wait_for_frames()
        for frame in frames:
            print(frame.as_motion_frame().get_motion_data())
        #return np.asarray([accel.x, accel.y, accel.z])
    
    def release(self):
        self.pipeline.stop()


p = DepthCamera()

try:
    while True:
        state, depth_frame, img= p.get_frame()
        p.accel_data()
        p.gyro_data()

finally:
    p.release()