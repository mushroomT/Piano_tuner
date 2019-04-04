import sys
from touch_screen_UI_V2 import *
import time
import threading
import serial
# from pitch_detect_algo_V3 import *


def motor_driver():
    precision = 1.0
    ser = serial.Serial('COM3', 9600)  # define port of arduino
    while (1):
        # print(ex.get_status())
        if ex.get_status():
            # print(ex.get_standard_frequency())
            # print(ex.get_current_frequency())
            diff_freq = ex.get_standard_frequency()-ex.get_current_frequency()
            if abs(diff_freq) > precision:
                # print("twist degree:",diff_freq)
                ser.write(str(diff_freq).encode())
                # print(str(diff_freq).encode())
                # line = ser.readline()
                # print(line.strip().decode())
            ex.default_status()
        time.sleep(0.5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI_Class()
    ex.initUI()
    ex.show()
    t = threading.Thread(target=motor_driver)
    t.start()
    sys.exit(app.exec_())
    sys.exit()
