import serial
import time
from pynput import keyboard
from time import sleep
import sys


is_pressed = {
    'n' : False,
    'm' : False,
    'r' : False,
    'f' : False,
    't' : False,
    'g' : False,
    'y' : False,
    'h' : False,
    'v' : False,
    'b' : False,
    'o' : False,
    'p' : False,
    'w' : False,
    's' : False,
    'd' : False,
    'a' : False
}


global arduino
for i in range(10):
    try:
        arduino = serial.Serial(port='/dev/ttyACM{}'.format(i), baudrate=9600, timeout = 0.5)
        break
    except serial.serialutil.SerialException:
        print('/dev/ttyUSB{} Failed'.format(i))
else:
    print('No port Connected. Exiting')
    sys.exit()


def on_press(key):
    try:
        if not is_pressed[str(key.char)]:
            is_pressed[str(key.char)] = True
            write_read(str(key.char))
            print(str(key.char))
    except AttributeError:
        pass


def on_release(key):
    is_pressed[str(key.char)] = False
    stop_char = '-'
    write_read(stop_char)
    print(stop_char)
    if key == keyboard.Key.esc:
        return False


def write_read(x):
    arduino.write(bytes(x, 'UTF-8'))
    time.sleep(0.01)
    data = arduino.readline()
    return data

while True:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    sleep(0.01)
