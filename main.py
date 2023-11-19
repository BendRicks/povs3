import re
from pynput.keyboard import Key, Controller
import keyboard
import serial
from serial import SerialException

JOYSTICK_CENTER_Y = 1950
JOYSTICK_CENTER_X = 1850
buffer = ''


if __name__ == '__main__':
    try:
        ser = serial.Serial('COM6', 115200, timeout=110)
        kbd = Controller()
        while True:
            data = ser.readline().decode('utf8').strip()
            if len(data) > 0:
                buffer += data
            datagram_match = re.search('<\\d+,\\d+,\\w*>', buffer)
            if datagram_match is not None:
                datagram = datagram_match.group()
                buffer = buffer.replace(datagram, '')
                data = datagram[1:len(datagram)-1].split(',')
                x = int(data[0])
                x_rel = x - JOYSTICK_CENTER_X
                y = int(data[1])
                y_rel = y - JOYSTICK_CENTER_Y
                buttons = data[2]
                if x_rel > 100:
                    kbd.tap("d")
                elif x_rel < -100:
                    kbd.tap("a")
                if y_rel > 100:
                    kbd.tap("w")
                elif y_rel < -100:
                    kbd.tap("s")

                if 'l' in buttons:
                    kbd.tap(Key.left)
                elif 'r' in buttons:
                    kbd.tap(Key.right)
                if 'u' in buttons:
                    kbd.tap(Key.up)
                elif 'd' in buttons:
                    kbd.tap(Key.down)
                if 'sc' in buttons:
                    JOYSTICK_CENTER_X = x
                    JOYSTICK_CENTER_Y = y
                    print(f'Calibrated joystick: X=${x} Y=${y}')
                elif 's' in buttons:
                    kbd.tap(Key.space)
                elif 'c' in buttons:
                    kbd.tap(Key.ctrl)
    except SerialException:
        print("Error connecting to com5 port")