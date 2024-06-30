from witmotion import IMU
from time import sleep

def callback(data):
    #sleep()
    try:
        print(data.yaw)
    except AttributeError:
        pass

imu = IMU()
imu.subscribe(callback)
#sleep(0.5)