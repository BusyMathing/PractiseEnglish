import json
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(592, 418)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.choose_test = QtWidgets.QComboBox(self.centralwidget)
        self.choose_test.setGeometry(QtCore.QRect(190, 90, 131, 21))
        self.choose_test.setObjectName("choose_test")
        self.add_test()
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 571, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(340, 90, 75, 23))
        self.start.setObjectName("start")
        self.start.clicked.connect(self.start_test)
        self.choice1 = QtWidgets.QPushButton(self.centralwidget)
        self.choice1.setGeometry(QtCore.QRect(170, 210, 261, 21))
        self.choice1.setObjectName("choice1")
        self.choice4 = QtWidgets.QPushButton(self.centralwidget)
        self.choice4.setGeometry(QtCore.QRect(170, 330, 261, 21))
        self.choice4.setObjectName("choice4")
        self.choice3 = QtWidgets.QPushButton(self.centralwidget)
        self.choice3.setGeometry(QtCore.QRect(170, 290, 261, 21))
        self.choice3.setObjectName("choice3")
        self.choice2 = QtWidgets.QPushButton(self.centralwidget)
        self.choice2.setGeometry(QtCore.QRect(170, 250, 261, 21))
        self.choice2.setObjectName("choice2")
        self.text = QtWidgets.QLabel(self.centralwidget)
        self.text.setGeometry(QtCore.QRect(10, 130, 571, 21))
        self.text.setObjectName("text")
        self.ans = QtWidgets.QLineEdit(self.centralwidget)
        self.ans.setGeometry(QtCore.QRect(170, 170, 261, 20))
        self.ans.setObjectName("ans")
        self.submit_button = QtWidgets.QPushButton(self.centralwidget)
        self.submit_button.setGeometry(QtCore.QRect(440, 170, 75, 23))
        self.submit_button.setObjectName("submit_button")
        self.submit_button.setText("提交")
        self.submit_button.clicked.connect(self.check_answer)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 592, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.score = 0

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 连接选择按钮的点击事件
        self.choice1.clicked.connect(lambda: self.check_answer(0))
        self.choice2.clicked.connect(lambda: self.check_answer(1))
        self.choice3.clicked.connect(lambda: self.check_answer(2))
        self.choice4.clicked.connect(lambda: self.check_answer(3))

        # 连接 QLineEdit 的回车键事件
        self.ans.returnPressed.connect(self.check_answer)

        # 初始化时禁用选项按钮
        self.disable_choices()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PractiseEnglish"))
        self.label.setText(_translate("MainWindow", "    Let\'s Practise English!"))
        self.start.setText(_translate("MainWindow", "Start!"))
        self.choice1.setText(_translate("MainWindow", "A..."))
        self.choice4.setText(_translate("MainWindow", "D..."))
        self.choice3.setText(_translate("MainWindow", "C..."))
        self.choice2.setText(_translate("MainWindow", "B..."))
        self.text.setText(_translate("MainWindow", "Your test here..."))

    def add_test(self):
        files = os.listdir('tests')
        for file in files:
            if file.endswith('.json'):
                file_name = os.path.splitext(file)[0]  # 去掉 .json 后缀
                self.choose_test.addItem(file_name)

    def start_test(self):
        self.data = []
        try:
            with open("tests/" + self.choose_test.currentText() + '.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.current_question_index = 0
            self.score = 0
            self.show_question()
            self.enable_choices()  # 启用选项按钮

            # 禁用 start 按钮和 choose_test 下拉菜单
            self.start.setEnabled(False)
            self.choose_test.setEnabled(False)
        except FileNotFoundError:
            self.label.setText("Test file not found!")
        except json.JSONDecodeError:
            self.label.setText("Error decoding JSON file!")
        except Exception as e:
            self.label.setText(f"An error occurred: {str(e)}")

    def show_question(self):
        if self.current_question_index < len(self.data):
            question = self.data[self.current_question_index]
            self.text.setText(question['text'])
            if question['type'] == 'choose':
                self.choice1.setText(question['choices'][0])
                self.choice2.setText(question['choices'][1])
                self.choice3.setText(question['choices'][2])
                self.choice4.setText(question['choices'][3])
                self.ans.setVisible(False)
                self.choice1.setVisible(True)
                self.choice2.setVisible(True)
                self.choice3.setVisible(True)
                self.choice4.setVisible(True)
                self.submit_button.setEnabled(False)  # 禁用提交按钮
            elif question['type'] == 'blank':
                self.choice1.setVisible(False)
                self.choice2.setVisible(False)
                self.choice3.setVisible(False)
                self.choice4.setVisible(False)
                self.ans.setVisible(True)
                self.ans.setText("")  # 重置 QLineEdit 内容
                self.submit_button.setEnabled(True)  # 启用提交按钮
        else:
            # 检查最后一道题的答案
            self.check_answer()
            self.show_final_result()

    def check_answer(self, choice_index=None):
        if not hasattr(self, 'data') or not self.data:
            self.label.setText("请先开始测试！")
            return

        question = self.data[self.current_question_index]
        if question['type'] == 'choose':
            if choice_index is not None and choice_index == question['answer']:
                self.label.setText("正确！")
                self.score += 1
            else:
                correct_answer = question['choices'][question['answer']]
                self.label.setText(f"错误！正确答案是：{correct_answer}")
        elif question['type'] == 'blank':
            user_answer = self.ans.text().strip()
            if user_answer == question['answer']:
                self.label.setText("正确！")
                self.score += 1
            else:
                self.label.setText(f"错误！正确答案是：{question['answer']}")

        self.current_question_index += 1

        if self.current_question_index < len(self.data):
            self.show_question()
        else:
            # 检查最后一道题的答案
            self.show_final_result()

    def show_final_result(self):
        self.label.setText("测试结束，你的正确率是：" + str(self.score / len(self.data) * 100) + "%" +
                           " (" + str(self.score) + "/" + str(len(self.data)) + ")")
        self.disable_choices()
        # 启用 start 按钮和 choose_test 下拉菜单
        self.start.setEnabled(True)
        self.choose_test.setEnabled(True)

    def disable_choices(self):
        self.choice1.setEnabled(False)
        self.choice2.setEnabled(False)
        self.choice3.setEnabled(False)
        self.choice4.setEnabled(False)
        self.ans.setEnabled(False)
        self.submit_button.setEnabled(False)

    def enable_choices(self):
        self.choice1.setEnabled(True)
        self.choice2.setEnabled(True)
        self.choice3.setEnabled(True)
        self.choice4.setEnabled(True)
        self.ans.setEnabled(True)
        self.submit_button.setEnabled(False)  # 初始化时禁用提交按钮


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
