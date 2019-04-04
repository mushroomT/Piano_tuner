import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,QLCDNumber,QSlider,QVBoxLayout,QHBoxLayout,QFrame,QSplitter,
                             QPushButton,QDesktopWidget, QLineEdit,QApplication,QWidget, QLabel,QGridLayout,QVBoxLayout,QGroupBox,QMainWindow)
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets,QtGui, QtCore
from random import randint
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from piano_config import Piano_keyname
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from record import record_sound
from change_bitrate import *
from pitch_detect_algo_V3 import *
from QCandyUi.CandyWindow import colorful
import winsound
key_num = [47,40,44,49]
class UI_Class(QWidget):
    def __init__(self):
        self.key_name = 'G'
        self.key_number = 47
        self.current_frequency = 0
        super().__init__()
        self.initUI()
        self.flag = False
        # self.standard_frequency = 0

    # def difference_detect(self,standard_frequency,current_frequency):

    def change_key_number(self,newkey):
        self.key_number = newkey

    def get_current_node(self):
        key = self.key_number
        Piano = Piano_keyname()
        self.key_name = Piano.Piano[key]
        return self.key_name

    def input_current_frequency(self, freq):
        self.current_frequency = freq

    def get_current_key_number(self):
        return self.key_number

    def get_current_frequency(self):
        return self.current_frequency

    def get_standard_frequency(self):
        key = self.get_current_key_number()
        std_frequency = 440*pow(2,(key-49)/12)
        return round(std_frequency,2)

    def get_status(self):
        return self.flag

    def next_Button(self):
        # self.flag = False
        # self.key_number = (self.key_number + 1) % 88
        self.key_number = key_num[(key_num.index(self.key_number) + 1) % 4]
        self.key_number_display.setText(str(self.key_number))
        self.key_number_display.setGeometry(42, 31, 90, 40)

        self.key_Notation_display.setText(self.get_current_node())
        self.key_Notation_display.setGeometry(42, 101, 90, 40)

        self.std_frequency_display.setText(str(self.get_standard_frequency()))
        self.std_frequency_display.setGeometry(192, 101, 130, 40)

        self.current_frequency = 0
        self.current_frequency_display.setText(str(self.current_frequency))
        self.current_frequency_display.setGeometry(192, 31, 130, 40)

    def back_Button(self):
        # self.flag = False
        # self.key_number = (self.key_number - 1) % 88
        self.key_number = key_num[(key_num.index(self.key_number) - 1) % 4]
        self.key_number_display.setText(str(self.key_number))
        self.key_number_display.setGeometry(42, 31, 90, 40)

        self.key_Notation_display.setText(self.get_current_node())
        self.key_Notation_display.setGeometry(42, 101, 90, 40)

        self.std_frequency_display.setText(str(self.get_standard_frequency()))
        self.std_frequency_display.setGeometry(192, 101, 130, 40)

        self.current_frequency = 0
        self.current_frequency_display.setText(str(self.current_frequency))
        self.current_frequency_display.setGeometry(192, 31, 130, 40)

    def record_Button(self):
        record_sound()
        path = 'output.wav'
        # path = './key_sound_WAV/35-G.wav'
        change_bitrate(path)
        self.current_frequency = signal_process(path)
        self.current_frequency_display.setText(str(round(self.current_frequency,2)))
        self.current_frequency_display.setGeometry(192, 31, 130, 40)
        self.flag = True
        # print(self.flag)

    def play_Button(self):
        path = './key_sound_WAV/'+str(self.key_number)+'-'+str(self.get_current_node())+'.wav'
        winsound.PlaySound(path, winsound.SND_FILENAME)

    def default_status(self):
        self.flag = False

    def move_center(self):
        m_rect = self.frameGeometry();
        w_rect = QDesktopWidget().availableGeometry();
        w_center_point = w_rect.center();
        m_rect.moveCenter(w_center_point);
        self.move(m_rect.topLeft());
    def initUI(self):
        key_number = str(self.get_current_key_number())
        key_node = self.get_current_node()
        current_frequency = str(self.get_current_frequency())
        std_frequency = str(self.get_standard_frequency())
        newfont = QtGui.QFont("Times", 15, QtGui.QFont.Bold)
        textfont = QtGui.QFont("Times", 9)

        self.col = QColor(173,216,230)
        self.bgcol = QColor(242, 250, 250)
        self.textcol = QColor(8, 36, 29)

        self.resize(378, 200)
        self.setWindowTitle('Ukulele tuner UI')
        self.move_center()

        self.main_p = QPalette();
        self.main_p.setColor(QPalette.Background, self.bgcol);
        # self.setAutoFillBackground(True);
        self.setPalette(self.main_p)

        self.square = QFrame(self)
        self.square.setGeometry(40, 33, 90, 40)
        self.square.setStyleSheet("QWidget { background-color: %s ;border-radius:5px}" %
                                  self.col.name())
        lbl1 = QLabel('Key Number', self)
        lbl1.move(40, 10)
        lbl1.setFont(textfont)
        lbl1.setStyleSheet("QWidget { color: %s ;}" %self.textcol.name())
        self.key_number_display = QLabel(key_number, self)
        self.key_number_display.move(42, 33)
        self.key_number_display.setFont(newfont)



        self.square = QFrame(self)
        self.square.setGeometry(40, 103, 90, 40)
        self.square.setStyleSheet("QWidget { background-color: %s ;border-radius:5px}" %
                                  self.col.name())
        lbl2 = QLabel('Key Notation', self)
        lbl2.move(40, 80)
        lbl2.setFont(textfont)
        lbl2.setStyleSheet("QWidget { color: %s ;}" % self.textcol.name())
        self.key_Notation_display = QLabel(key_node, self)
        self.key_Notation_display.move(42, 103)
        self.key_Notation_display.setFont(newfont)


        self.square = QFrame(self)
        self.square.setGeometry(190, 33, 130, 40)
        self.square.setStyleSheet("QWidget { background-color: %s ;border-radius:5px}" %
                                  self.col.name())
        lbl3 = QLabel('Current Frequency', self)
        lbl3.move(190, 10)
        lbl3.setFont(textfont)
        lbl3.setStyleSheet("QWidget { color: %s ;}" % self.textcol.name())
        self.current_frequency_display = QLabel(current_frequency, self)
        self.current_frequency_display.move(192, 33)
        self.current_frequency_display.setFont(newfont)


        self.square = QFrame(self)
        self.square.setGeometry(190, 103, 130, 40)
        self.square.setStyleSheet("QFrame { background-color: %s ;border-radius:5px}" %
                                  self.col.name())
        lbl4 = QLabel('Standard Frequency', self)
        lbl4.move(190, 80)
        lbl4.setFont(textfont)
        lbl4.setStyleSheet("QWidget { color: %s ;}" % self.textcol.name())
        self.std_frequency_display = QLabel(std_frequency, self)
        self.std_frequency_display.move(192, 103)
        self.std_frequency_display.setFont(newfont)

        back_btn = QPushButton('Back', self)
        back_btn.resize(60, 25)
        back_btn.move(30, 155)
        back_btn.clicked.connect(self.back_Button)
        back_btn.setStyleSheet('''QPushButton{background:#7595C4;border-radius:5px;}QPushButton:hover{background:#4885DF;}''')


        next_btn = QPushButton('Next', self)
        next_btn.resize(60,25)
        next_btn.move(110, 155)
        next_btn.clicked.connect(self.next_Button)
        next_btn.setStyleSheet('''QPushButton{background:#A9D388;border-radius:5px;}QPushButton:hover{background:#66C61D;}''')


        record_btn = QPushButton('Record',self)
        record_btn.resize(60, 25)
        record_btn.move(190, 155)
        record_btn.clicked.connect(self.record_Button)
        record_btn.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:#FFC700;}''')

        play_btn = QPushButton('Play', self)
        play_btn.resize(60, 25)
        play_btn.move(270, 155)
        play_btn.clicked.connect(self.play_Button)
        play_btn.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:#F62941;}''')

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = UI_Class()
#     ex.initUI()
#     ex.show()
#     sys.exit(app.exec_())
#     sys.exit()