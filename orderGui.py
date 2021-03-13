FLAG_CONST=False
import OrderLogic
from OrderLogic import Order
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QDialogButtonBox


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        '''Creating GUI om MainWindow'''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(624, 319)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(100, 130, 113, 32))
        self.pushButton.setObjectName("addOrder")
        self.pushButton.clicked.connect(self.addnum)
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(450, 130, 113, 32))
        self.pushButton1.setObjectName("infoOrder")
        self.pushButton1.clicked.connect(self.infocheck)
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(200, 130, 180, 32))
        self.pushButton2.setObjectName("clearallOrders")
        self.pushButton2.clicked.connect(self.clearall)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 624, 24))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("actionNew_table")
        self.action2 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("actionOpen")
        self.actionSave_us = QtWidgets.QAction(MainWindow)
        self.actionSave_us.setObjectName("actionSave_us")
        self.actionPrint_table = QtWidgets.QAction(MainWindow)
        self.actionPrint_table.setObjectName("actionPrint_table")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menufile.addAction(self.action1)
        self.menufile.addAction(self.action2)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionSave_us)
        self.menufile.addAction(self.actionPrint_table)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionClose)
        self.menubar.addAction(self.menufile.menuAction())
        self.action1.triggered.connect(self.addnum)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def addnum(self):
        '''Add new order to databse'''
        global ok1
        dialog = QInputDialog()
        '''Exception processing'''
        while True:

            try:
                num, ok1 = dialog.getInt(dialog, "Номер заказа", "Введите номер заказа:", QLineEdit.Normal)
                if ok1:
                    data = OrderLogic.loaddb('order', num)

                    QMSG = QMessageBox()
                    QMSG.setWindowTitle("Ошибка")
                    QMSG.setText('Заказ уже существует, введите другой номер')
                    QMSG.exec_()
                else: break

            except IndexError:
                if ok1:
                    name, ok2 = dialog.getText(dialog, "Данные заказчика", "Введите данные заказчика:", QLineEdit.Normal)
                    if ok2:
                        cost, ok3 = dialog.getDouble(dialog, 'Стоимость заказа', "Введите стоимость заказа:", QLineEdit.Normal)
                        if ok3:
                            args, ok4 = dialog.getText(dialog, 'Номера заказов', 'Введите заказы', QLineEdit.Normal)
                            if ok4:
                                OrderLogic.adder(num, name, cost=cost, flag=False, args=args)
                break
    def infocheck(self):
        '''Checking database for an order'''
        dialog = QInputDialog()
        num, ok = dialog.getInt(dialog, 'Номер заказа', 'Введите номер заказа:', QLineEdit.Normal)

        while True:
            try:
                if ok:
                    self.checkstatus(num)
                break
            except IndexError:
                QMSG = QMessageBox()
                QMSG.setWindowTitle("Ошибка")
                QMSG.setText('Такого заказа нету в базе, попробуйте еще раз?')
                QMSG.exec_()
                num, ok = dialog.getInt(dialog, 'Номер заказа', 'Введите номер заказа:', QLineEdit.Normal)





    def checkstatus(self, num):
        data = OrderLogic.loaddb('order', num)
        global SeparData
        SeparData = OrderLogic.Order.separator(data)

        if SeparData['flag']:
            QMSG = QMessageBox()
            QMSG.setWindowTitle("Информация о заказчике")
            QMSG.setText('Заказ уже забран, узнать информацию все равно?')
            QMSG.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            QMSG.buttonClicked.connect(self.StAct)

            QMSG.exec_()
        else:
            self.QMB(SeparData)

    def StAct(self, btn):
        if btn.text() == 'OK':
            global SeparData
            self.QMB(SeparData)

    def QMB(self, SeparData):
        QMSG = QMessageBox()
        QMSG.setWindowTitle("Информация о заказчике")
        QMSG.setText(
            f"Имя заказчика:{SeparData['name']}\nСтоимость заказа:{SeparData['cost']} рублей\n"
            f"Номера заказов:{SeparData['args']}"
        )
        QMSG.setIcon(QMessageBox.Information)
        CHB = QtWidgets.QCheckBox(QMSG)
        CHB.setText("Заказ отдан")
        CHB.setGeometry(QtCore.QRect(100, 70, 100, 20))

        if CHB.isChecked:

            if not SeparData['flag']:
                CHB.setChecked(True)
                Order.changeflag(SeparData['num'])
        QMSG.exec_()

    def clearall(self):
        really = QMessageBox()
        really.setIcon(QMessageBox.Question)
        really.setText('Вы действительно хотите удалить все данные?')
        really.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        really.buttonClicked.connect(self.clearaction)
        really.exec_()

    def clearaction(self, btn):
        if btn.text() == 'OK':
            OrderLogic.cleardb()
        else:
            pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление заказами v 0.0.2"))
        self.pushButton.setText(_translate("MainWindow", "Добавить"))
        self.pushButton1.setText(_translate("MainWindow", "Информация"))
        self.pushButton2.setText(_translate("MainWindow", "Удалить базу данных"))
        self.menufile.setTitle(_translate("MainWindow", "Файл"))
        self.action1.setText(_translate("MainWindow", "Новая запись в таблице"))
        self.action2.setText(_translate("MainWindow", "Инфо о записи"))
        self.actionSave_us.setText(_translate("MainWindow", "Save us"))
        self.actionPrint_table.setText(_translate("MainWindow", "Print table"))
        self.actionClose.setText(_translate("MainWindow", "Close"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
