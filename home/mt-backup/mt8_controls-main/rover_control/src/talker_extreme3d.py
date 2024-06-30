#!/usr/bin/env python3


import rospy
from time import sleep
from std_msgs.msg import String
from sensor_msgs.msg import Joy



'''
Installation:
1) "sudo apt-get install ros-<DISTRO>-joy"
2) Check the Joystick Number "js<>": ls /dev/input/"
3) Test the Joystick: "sudo jstest /dev/input/js<>"
4) Give Permission: "sudo chmod a+rw /dev/input/js<>"

Running:
1) Set the Joystick: " "
2) Joy Node Run: "rosrun joy joy_node" / Optional Deadzone: "rosrun joy joy_node _deadzone:=0.001"

Testing:
1) Run Test Node: "rostopic echo joy"
'''

DEADZONE = 0.15 # 10% Deadzone

ACTIVATION_BUTTON = 0
ACTIVATED = False
PWM_INDEX = 0

WHEEL_STOPPED = False
ARM_STOPPED = False

CMD_STRING = ''
LAST_CMD_LEN = 0

BUTTONS = {
    0: '',     # Trigger
    1: '',     # Thumb
    2: 'v',     # 3
    3: 'b',     # 4
    4: 'o',     # 5
    5: 'p',     # 6
    6: 'r',     # 7
    7: 'f',     # 8
    8: 't',      # 9
    9: 'g',     # 10
    10: 'y',    # 11
    11: 'h',     # 12
}

AXES = {
    0: [[+1, -1], ['a', 'd']],  # Joy Horizontal
    1: [[+1, -1], ['w', 's']],  # Joy Vertical
    2: [[+1, -1], ['n', 'm']],  # Joy Twist
    3: [[-1, -0.25, +0.25, +1],
        ['1', '2', '3', '4']],  # Slider
    4: [],                      # Thumbstick Horizontal
    5: [],                      # Thumbstick Vertical
}


# AXES = {
#     0: [2, [], ['v', 'b']],                 # DL DR
#     1: [2, [], ['o', 'p']],                 # DU DD
#     2: [1, [[1, -1]], ['g']],               # LT
#     3: [2, [[0, 1], [0, -1]], ['a', 'd']],  # RSL RSR
#     4: [2, [[0, 1], [0, -1]], ['w', 's']],  # RSU RSD
#     5: [1, [[1, -1]], ['h']],               # RT
#     6: [2, [[0, 1], [0, -1]], ['', '']],    # LSL LSR
#     7: [2, [[0, 1], [0, -1]], ['', '']],    # LSU LSD
# }


is_pressed_button = [False for i in range(12)]
is_pressed_axes = [[0, 0] for i in range(6)]


def talker():
    global control_publisher, joy_subscriber, sensor_msgs_joy
    
    control_publisher = rospy.Publisher('rover_control', String, queue_size=10)
    joy_subscriber = rospy.Subscriber('joy', Joy, joy_callback)

    rospy.init_node('base_station', anonymous=True)

    sensor_msgs_joy = None

    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        move()
        rate.sleep()


def joy_callback(msgs):
    global sensor_msgs_joy
    sensor_msgs_joy = msgs


def move():
    global ACTIVATED
    global ACTIVATION_BUTTON
    global CMD_STRING
    global LAST_CMD_LEN
    global PWM_INDEX
    # global WHEEL_STOPPED
    # global ARM_STOPPED
    global DEADZONE
    global control_publisher

    wheel_cmd_pub = False # Flag to check if wheel command was published
    arm_cmd_pub = False # Flag to check if arm command was published

    buttons = tuple(range(12)) if sensor_msgs_joy == None else sensor_msgs_joy.buttons
    axes = tuple(range(6)) if sensor_msgs_joy == None else sensor_msgs_joy.axes

    for i_button, value_button in enumerate(buttons):
        if not ACTIVATED: # Controller doesn't work until Trigger is pressed. Also needed as controller send id values before input pressed
            if i_button == ACTIVATION_BUTTON and value_button == 1:
                ACTIVATED = True
            continue

        if str(BUTTONS[i_button]) == '': continue # Skip if no mapping

        if value_button == 1:
            key = str(BUTTONS[i_button])
            CMD_STRING += key
            # control_publisher.publish(key)
            # rospy.loginfo('{} Published'.format(key))
            # arm_cmd_pub = True
            # ARM_STOPPED = False

    for i_axis, value_axis in enumerate(axes):
        if not ACTIVATED:
            continue

        if i_axis == 3: # Stop Slider from sending repeated PWM Commands
            if AXES[3][1][snapToClosest(value_axis, AXES[3][0])] == PWM_INDEX:
                continue
            print(PWM_INDEX)
            PWM_INDEX = AXES[3][1][snapToClosest(value_axis, AXES[3][0])]
        
        if (i_axis != 3 and abs(value_axis) < DEADZONE): continue # Avoid deadzone on Slider
        if len(AXES[i_axis]) == 0: continue # Skip if no mapping

        key = str(AXES[i_axis][1][snapToClosest(value_axis, AXES[i_axis][0])])

        CMD_STRING += key

        # control_publisher.publish(key)
        # rospy.loginfo('{} Published'.format(key))
        # wheel_cmd_pub = True
        # WHEEL_STOPPED = False
    
    if ACTIVATED:
        for cmd in CMD_STRING:
            control_publisher.publish(cmd)
            rospy.loginfo('{} Published'.format(cmd))
        
        if len(CMD_STRING) < LAST_CMD_LEN:
            sendStop()

        LAST_CMD_LEN = len(CMD_STRING)
        CMD_STRING = ''

        # if not WHEEL_STOPPED and not wheel_cmd_pub:
        #     sendStop()
        #     WHEEL_STOPPED = True
        # if not ARM_STOPPED and not arm_cmd_pub:
        #     sendStop()
        #     ARM_STOPPED = True

def sendStop():
    global control_publisher
    for _ in range(10):
        control_publisher.publish('-')
        rospy.loginfo('- Published')
        sleep(0.01)

def snapToClosest(value, snapPoints: list): # value = 0.5, snapPoints = [-1, -0.25, 0.25, 1]
    return snapPoints.index(min(snapPoints, key=lambda x: abs(x - value)))

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass