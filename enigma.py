import sys

from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt5 import QtMultimedia, QtCore, QtGui
from PyQt5.QtCore import QTimer
from random import choice, randrange
from PyQt5 import uic


class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        screen_size = [1500, 900]
        self.setGeometry(100, 50, *screen_size)
        self.setFixedSize(*screen_size)

        self.pixmap = QPixmap('inter/orig.jpg')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(1500, 900)
        self.image.setPixmap(self.pixmap)

        uic.loadUi('inter/enigma.ui', self)
        self.setWindowTitle('ENIGMA')

        self.pixmap_1 = QPixmap('inter/git.jpg')
        self.image_1 = QLabel(self)
        self.image_1.resize(100, 100)
        self.image_1.move(1350, 780)
        self.image_1.setPixmap(self.pixmap_1)

        self.rot_comb_1.setValue(1)
        self.rot_comb_2.setValue(1)
        self.rot_comb_3.setValue(1)
        self.rot_comb_1.valueChanged.connect(self.spin_value_rim)
        self.rot_comb_2.valueChanged.connect(self.spin_value_rim)
        self.rot_comb_3.valueChanged.connect(self.spin_value_rim)
        self.number_rotor_rim = {1: "Ⅰ", 2: "Ⅱ", 3: 'Ⅲ', 4: 'Ⅳ', 5: 'Ⅴ'}

        self.text_1.setReadOnly(True)
        self.text_2.setReadOnly(True)
        self.display_1.setReadOnly(True)
        self.display_2.setReadOnly(True)
        self.display_3.setReadOnly(True)
        self.fast_encrypting = False

        self.rotor_1 = [[23, 10], [0, 4], [19, 12], [7, 22], [2, 21], [11, 17], [3, 25], [16, 24], [9, 14], [20, 1],
                        [8, 6], [15, 5], [13, 18], [18, 13], [5, 15], [6, 8], [1, 20], [14, 9], [24, 16], [25, 3],
                        [17, 11], [21, 2], [22, 7], [12, 19], [4, 0], [10, 23]]

        self.rotor_2 = [[16, 11], [10, 7], [20, 6], [4, 3], [2, 0], [15, 18], [22, 13], [8, 9], [1, 14], [12, 5],
                        [23, 25], [17, 19], [21, 24], [24, 21], [19, 17], [25, 23], [5, 12], [14, 1], [9, 8],
                        [13, 22], [18, 15], [0, 2], [3, 4], [6, 20], [7, 10], [11, 16]]

        self.rotor_3 = [[1, 3], [16, 20], [25, 22], [11, 23], [9, 14], [13, 6], [19, 8], [10, 4], [24, 18], [12, 0],
                        [21, 5], [15, 2], [7, 17], [17, 7], [2, 15], [5, 21], [0, 12], [18, 24], [4, 10], [8, 19],
                        [6, 13], [14, 9], [23, 11], [22, 25], [20, 16], [3, 1]]

        self.rotor_4 = [[7, 17], [3, 20], [13, 16], [24, 9], [18, 2], [6, 14], [4, 5], [12, 8], [15, 1], [19, 21],
                        [23, 10], [25, 0], [22, 11], [11, 22], [0, 25], [10, 23], [21, 19], [1, 15], [8, 12],
                        [5, 4], [14, 6], [2, 18], [9, 24], [16, 13], [20, 3], [17, 7]]

        self.rotor_5 = [[1, 0], [22, 16], [13, 7], [2, 11], [17, 10], [3, 20], [9, 6], [19, 8], [14, 23], [25, 15],
                        [18, 12], [24, 5], [4, 21], [21, 4], [5, 24], [12, 18], [15, 25], [23, 14], [8, 19],
                        [6, 9], [20, 3], [10, 17], [11, 2], [7, 13], [16, 22], [0, 1]]

        self.reflector = [[4, 9], [0, 11], [19, 24], [16, 20], [8, 6], [14, 3], [1, 2], [13, 5], [25, 23], [22, 12],
                          [17, 18], [10, 21], [15, 7], [7, 15], [21, 10], [18, 17], [12, 22], [23, 25], [5, 13],
                          [2, 1], [3, 14], [6, 8], [20, 16], [24, 19], [11, 0], [9, 4]]

        self.all_rotors = {1: self.rotor_1, 2: self.rotor_2, 3: self.rotor_3, 4: self.rotor_4, 5: self.rotor_5}

        self.dict_of_switchboard = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H',
                                    'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P',
                                    'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X',
                                    'Y': 'Y', 'Z': 'Z'}
        self.style_default_switchboard = 'font-size:14px; background-color: rgb(88, 103, 109);border-style: outset;' \
                                         'border-radius:20px;border-width: 5px;border-color:rgb(102, 119, 109);'

        self.btn_keyboard_style_default = 'font-size:20px;background-color:rgb(139, 119, 101);border-style:outset;' \
                                          'border-radius:30px;border-width: 5px;border-color:rgb(169, 149, 131);'

        self.btn_light_style_default = 'background-color: rgb(205, 205, 193);border-style: outset;border-radius:30px;' \
                                       'border-width: 5px;border-color:rgb(159, 159, 151);font-size:18px;'

        self.btn_light_style_clicked = 'background-color: rgb(255, 250, 205);border-style: outset;border-radius:30px;' \
                                       'border-width: 5px;border-color:rgb(205, 200, 205);font-size:18px;'

        self.btn_keyboard_style_clicked = 'background-color: rgb(238, 203, 173);border-style:outset;' \
                                          'border-radius:30px;border-width: 5px;border-color:rgb(205, 175, 149);' \
                                          'font-size:20px;'
        self.btn_fix_style_on = 'background-color: rgb(109, 95, 97);border-style: outset;border-radius:5px;' \
                                ' border-width: 5px;border-color:rgb(149, 145, 163);font-size:20px;'

        self.btn_fix_style_off = 'background-color: rgb(139, 125, 123);border-style: outset;border-radius:5px;' \
                                 ' border-width: 5px;border-color:rgb(149, 145, 163);font-size:20px;'

        self.keyboard_keys_list = []
        self.light_keys_list = []

        self.rotor_1_on = []
        self.rotor_2_on = []
        self.rotor_3_on = []

        self.rotor_1_on_copy = []
        self.rotor_2_on_copy = []
        self.rotor_3_on_copy = []

        self.text_prow_text = ''
        self.btn_send = ''
        self.player = ''
        self.elem = ''
        self.style = ''
        self.sender_1 = ''
        self.find_1 = ''
        self.btn_sender_light = ''

        self.rot_combination = [None, None, None]
        self.timer_count = False
        self.timer_count_2 = False

        self.count_color = -1
        self.styles_btn = ['rgb(162, 205, 90)', 'rgb(238, 99, 99)', 'rgb(238, 121, 66)', 'rgb(139, 71, 137)',
                           'rgb(137, 104, 205)', 'rgb(238, 154, 0)', 'rgb(54, 100, 139)', 'rgb(205, 173, 0)',
                           'rgb(69, 139, 116)', 'rgb(238, 220, 130)', 'rgb(122, 197, 205)', 'rgb(139, 123, 139)',
                           'rgb(238, 162, 173)']

        self.sound_list = ['btn_sounds/btn_sound_1.wav', 'btn_sounds/btn_sound_2.wav', 'btn_sounds/btn_sound_3.wav',
                           'btn_sounds/btn_sound_4.wav', 'btn_sounds/btn_sound_5.wav']
        self.x = 450
        self.y = 500
        self.size_keyboard = 60
        self.size_switchboard = 40
        self.english_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                                 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        self.switchboard_key_on = False
        self.count_3 = 1
        self.count_2 = 1
        self.count_1 = 1

        for i in range(0, self.size_keyboard * len(self.english_alphabet), self.size_keyboard):
            if i // self.size_keyboard == 20:
                self.x += 120
            self.btn = QPushButton(self.english_alphabet[i // self.size_keyboard], self)
            self.btn.setGeometry(self.x + (i % (self.size_keyboard * 10)),
                                 self.y + (self.size_keyboard * (i // (self.size_keyboard * 10))), self.size_keyboard,
                                 self.size_keyboard)
            self.btn.resize(self.size_keyboard, self.size_keyboard)
            self.btn.setStyleSheet(self.btn_keyboard_style_default)
            self.btn.clicked.connect(self.button_pushed)
        self.x = 450

        for i in range(0, self.size_keyboard * len(self.english_alphabet), self.size_keyboard):
            if i // self.size_keyboard == 20:
                self.x += 120
            self.btn = QPushButton(self.english_alphabet[i // self.size_keyboard], self)
            self.btn.setGeometry(self.x + (i % (self.size_keyboard * 10)),
                                 self.y - 200 + (self.size_keyboard * (i // (self.size_keyboard * 10))),
                                 self.size_keyboard, self.size_keyboard)
            self.btn.resize(self.size_keyboard, self.size_keyboard)
            self.btn.setStyleSheet(self.btn_light_style_default)
            self.light_keys_list.append(self.btn)
        self.x = 450

        for i in range(0, self.size_switchboard * len(self.english_alphabet), self.size_switchboard):
            self.btn = QPushButton(self.english_alphabet[i // self.size_switchboard], self)
            self.btn.setGeometry(self.x + 40 + (i % (self.size_switchboard * 13)),
                                 self.y + 200 + (self.size_switchboard * (i // (self.size_switchboard * 13))),
                                 self.size_switchboard, self.size_switchboard)
            self.btn.resize(self.size_switchboard, self.size_switchboard)
            self.btn.setStyleSheet(self.style_default_switchboard)
            self.btn.clicked.connect(self.switchboard)
            self.keyboard_keys_list.append(self.btn)

        self.spinBox.setValue(1)
        self.spinBox_2.setValue(1)
        self.spinBox_3.setValue(1)
        self.spinBox.valueChanged.connect(self.spin_value)
        self.spinBox_2.valueChanged.connect(self.spin_value)
        self.spinBox_3.valueChanged.connect(self.spin_value)
        self.pushButton.clicked.connect(self.fast_encrypt)
        self.pushButton_2.clicked.connect(self.fixed_on)
        self.pushButton_3.clicked.connect(self.clear)
        self.pushButton_4.clicked.connect(self.save)
        self.fixed = False
        self.encrypt_possible = True

    def save(self):
        name = QFileDialog.getSaveFileName(self, "Save File", '/', "Text (*.txt)")[0]
        if name != '':
            file = open(name, mode='wt', encoding='UTF-8')
            text = self.text_2.toPlainText()
            file.write(text)
            file.close()

    def clear(self):
        self.display_1.setText("Ⅰ")
        self.display_2.setText("Ⅰ")
        self.display_3.setText("Ⅰ")

        self.rot_comb_1.setValue(1)
        self.rot_comb_2.setValue(1)
        self.rot_comb_3.setValue(1)

        self.spinBox.setValue(1)
        self.spinBox_2.setValue(1)
        self.spinBox_3.setValue(1)
        self.text_1.clear()
        self.text_2.clear()
        self.lineEdit.clear()
        self.fixed = False
        self.pushButton_2.setStyleSheet(self.btn_fix_style_off)
        self.count_1 = 1
        self.count_2 = 1
        self.count_3 = 1
        self.rotor_1_on = [i[:] for i in self.rotor_1_on_copy][:]
        self.rotor_2_on = [i[:] for i in self.rotor_2_on_copy][:]
        self.rotor_3_on = [i[:] for i in self.rotor_3_on_copy][:]

        self.spinBox.setReadOnly(False)
        self.spinBox_2.setReadOnly(False)
        self.spinBox_3.setReadOnly(False)

        self.rot_comb_1.setReadOnly(False)
        self.rot_comb_2.setReadOnly(False)
        self.rot_comb_3.setReadOnly(False)

    def fixed_on(self):
        self.rot_comb_1.setReadOnly(True)
        self.rot_comb_2.setReadOnly(True)
        self.rot_comb_3.setReadOnly(True)

        self.rot_combination = [self.rot_comb_1.value(), self.rot_comb_2.value(), self.rot_comb_3.value()]
        self.display_1.setText(self.number_rotor_rim[self.rot_comb_1.value()])
        self.display_2.setText(self.number_rotor_rim[self.rot_comb_2.value()])
        self.display_3.setText(self.number_rotor_rim[self.rot_comb_3.value()])

        self.rotor_1_on = self.all_rotors[self.rot_combination[0]][:]
        self.rotor_2_on = self.all_rotors[self.rot_combination[1]][:]
        self.rotor_3_on = self.all_rotors[self.rot_combination[2]][:]

        self.rotor_1_on_copy = []
        self.rotor_2_on_copy = []
        self.rotor_3_on_copy = []

        [self.rotor_1_on_copy.append(i[:]) for i in self.rotor_1_on]
        [self.rotor_2_on_copy.append(i[:]) for i in self.rotor_2_on]
        [self.rotor_3_on_copy.append(i[:]) for i in self.rotor_3_on]

        self.fixed = True
        self.pushButton_2.setStyleSheet(self.btn_fix_style_on)
        self.rotor_1_on = [i[:] for i in self.rotor_1_on_copy][:]
        self.rotor_2_on = [i[:] for i in self.rotor_2_on_copy][:]
        self.rotor_3_on = [i[:] for i in self.rotor_3_on_copy][:]

        for i in range(self.spinBox.value() - 1):
            self.spin_rotors_lists(self.rotor_1_on)

        for i in range(self.spinBox_2.value() - 1):
            self.spin_rotors_lists(self.rotor_2_on)

        for i in range(self.spinBox_3.value() - 1):
            self.spin_rotors_lists(self.rotor_3_on)

        self.count_1 = self.spinBox.value()
        self.count_2 = self.spinBox_2.value()
        self.count_3 = self.spinBox_3.value()

        self.spinBox.setReadOnly(True)
        self.spinBox_2.setReadOnly(True)
        self.spinBox_3.setReadOnly(True)
        self.encrypt_possible = True

    def fast_encrypt(self):
        if self.fixed:
            for i in range(len(self.lineEdit.text())):
                if self.lineEdit.text()[i].upper() not in self.english_alphabet:
                    self.encrypt_possible = False

            if self.encrypt_possible:
                self.fast_encrypting = True
                self.text_prow_text = self.lineEdit.text()
                for i in range(len(self.text_prow_text)):
                    self.switchboard(self.text_prow_text[i].upper())
                    self.text_1.setText(self.text_1.toPlainText() + self.text_prow_text[i].upper())
                    if i == len(self.text_prow_text) - 1:
                        self.fast_encrypting = False
            else:
                self.lineEdit.setText('ERROR')
                self.encrypt_possible = True

    def spin_value_rim(self):
        if self.sender().value() > 5:
            self.sender().setValue(1)
        elif self.sender().value() < 1:
            self.sender().setValue(5)

        if self.sender() == self.rot_comb_1:
            self.display_1.setText(self.number_rotor_rim[self.rot_comb_1.value()])
        elif self.sender() == self.rot_comb_2:
            self.display_2.setText(self.number_rotor_rim[self.rot_comb_2.value()])
        else:
            self.display_3.setText(self.number_rotor_rim[self.rot_comb_3.value()])

    def spin_value(self):
        if self.sender().value() > 26:
            self.sender().setValue(1)
        elif self.sender().value() < 1:
            self.sender().setValue(26)

    def button_pushed(self):
        for i in self.light_keys_list:
            if i.styleSheet() != self.btn_light_style_default:
                i.setStyleSheet(self.btn_light_style_default)
        if self.fixed:
            self.text_1.setText(self.text_1.toPlainText() + self.sender().text())
            self.btn_send = self.sender()
            self.timer_count = True
            self.style_of_btn()

            media = QtCore.QUrl.fromLocalFile(choice(self.sound_list))
            content = QtMultimedia.QMediaContent(media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(content)
            self.player.play()
            self.switchboard(self.sender().text())

    def style_of_btn(self):
        if self.timer_count:
            self.btn_send.setStyleSheet(self.btn_keyboard_style_clicked)
            self.timer_count = False
            QTimer().singleShot(100, self.style_of_btn)
        else:
            self.btn_send.setStyleSheet(self.btn_keyboard_style_default)

    def style_of_light_btn(self):
        if self.timer_count_2:
            self.btn_sender_light.setStyleSheet(self.btn_light_style_clicked)
            self.timer_count_2 = False
            QTimer().singleShot(1000, self.style_of_light_btn)
        else:
            self.btn_sender_light.setStyleSheet(self.btn_light_style_default)

    def switchboard(self, pushed_button=0):
        if self.sender() in self.keyboard_keys_list:
            if not self.switchboard_key_on and self.dict_of_switchboard[self.sender().text()] != self.sender().text():
                if len(self.styles_btn) == self.count_color:
                    self.styles_btn.append(
                        'rgb(' + str(randrange(50, 200)) + ',' + str(randrange(50, 200)) + ',' + str(
                            randrange(50, 200)) + ')')
                self.sender().setStyleSheet(self.style_default_switchboard)
                for i in self.keyboard_keys_list:
                    if i.text() == self.dict_of_switchboard[self.sender().text()]:
                        self.elem = self.keyboard_keys_list.index(i)
                self.keyboard_keys_list[self.elem].setStyleSheet(self.style_default_switchboard)

                self.dict_of_switchboard[self.keyboard_keys_list[self.elem].text()] = \
                    self.keyboard_keys_list[self.elem].text()
                self.dict_of_switchboard[self.sender().text()] = self.sender().text()

            elif not self.switchboard_key_on:
                self.count_color += 1
                if self.count_color == len(self.styles_btn):
                    self.styles_btn.append(
                        'rgb(' + str(randrange(50, 200)) + ',' + str(randrange(50, 200)) + ',' + str(
                            randrange(50, 200)) + ')')

                self.style = self.styles_btn[self.count_color]
                self.sender().setStyleSheet('background-color: ' + self.style + ';'
                                            'border-style: outset;'
                                            'border-radius:20px;'
                                            'border-width: 5px;'
                                            'border-color:' + self.style + ';' +
                                            'font-size:12px;')
                self.switchboard_key_on = True
                self.sender_1 = self.sender()

            elif self.switchboard_key_on and self.sender().text() == self.sender_1.text():
                self.switchboard_key_on = False
                self.sender().setStyleSheet(self.style_default_switchboard)

            elif self.sender().styleSheet() == self.style_default_switchboard:
                self.sender().setStyleSheet('background-color: '
                                            + self.style + ';'
                                                           'border-style: outset;'
                                                           'border-radius:20px;'
                                                           'border-width: 5px;'
                                                           'border-color:' + self.style + ';' +
                                            'font-size:12px;')

                self.dict_of_switchboard[self.sender_1.text()] = self.sender().text()
                self.dict_of_switchboard[self.sender().text()] = self.sender_1.text()
                self.switchboard_key_on = False

        if pushed_button != 0:
            self.rotors(self.dict_of_switchboard[pushed_button])

    def spin_rotors_lists(self, list_name):
        for i in list_name:
            if i[0] + 1 > 25:
                i[0] = -1
            if i[1] + 1 > 25:
                i[1] = -1
            i[0], i[1] = i[0] + 1, i[1] + 1

    def spin_rotors(self):
        self.count_1 += 1
        self.spin_rotors_lists(self.rotor_1_on)
        if self.count_3 == 27:
            self.count_3 = 1

        elif self.count_2 == 27:
            self.spin_rotors_lists(self.rotor_3_on)
            self.count_3 += 1
            self.count_2 = 1

        elif self.count_1 == 27:
            self.spin_rotors_lists(self.rotor_2_on)
            self.count_2 += 1
            self.count_1 = 1

    def coding(self, list_name):
        for i in range(26):
            if list_name[i][0] == self.find_1:
                self.find_1 = list_name[i][1]
                break

    def rotors(self, pushed_button):
        self.find_1 = self.rotor_1_on[self.english_alphabet.index(pushed_button)][0]
        self.coding(self.rotor_2_on)
        self.coding(self.rotor_3_on)
        self.coding(self.reflector)
        self.coding(self.rotor_3_on)
        self.coding(self.rotor_2_on)

        for i in range(26):
            if self.rotor_1_on[i][0] == self.find_1:
                self.find_1 = i
                break

        if not self.fast_encrypting:
            self.timer_count_2 = True
            for i in self.light_keys_list:
                if i.text() == self.dict_of_switchboard[self.english_alphabet[self.find_1]]:
                    self.btn_sender_light = i
                    self.style_of_light_btn()

        self.spinBox.setValue(self.count_1)
        self.spinBox_2.setValue(self.count_2)
        self.spinBox_3.setValue(self.count_3)
        self.text_2.setText(self.text_2.toPlainText() + self.dict_of_switchboard[self.english_alphabet[self.find_1]])
        self.spin_rotors()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('inter/en_mini.png'))
    ex = Example()
    ex.show()
    sys.exit(app.exec())
