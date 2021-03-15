import OrderLogic
from OrderLogic import Order
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QVBoxLayout, QDesktopWidget


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        #Creating GUI on MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.button1 = QtWidgets.QPushButton("Новая запись в таблице")
        self.button2 = QtWidgets.QPushButton("Информация о заказе")
        self.button3 = QtWidgets.QPushButton("Удалить базу данных")
        self.button4 = QtWidgets.QPushButton("Открыть таблицу заказов")
        self.Vbox = QVBoxLayout(self.centralwidget)
        self.ButtonGroup = QtWidgets.QButtonGroup(self.centralwidget)
        self.Vbox.addWidget(self.button1)
        self.Vbox.addWidget(self.button2)
        self.Vbox.addWidget(self.button3)
        self.Vbox.addWidget(self.button4)
        self.button1.clicked.connect(self.addnum)
        self.button2.clicked.connect(self.infocheck)
        self.button3.clicked.connect(self.clearall)
        self.button4.clicked.connect(self.createtable)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 624, 24))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("action1")
        self.action2 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("action2")
        self.action3 = QtWidgets.QAction(MainWindow)
        self.action3.setObjectName("action3")
        self.action4 = QtWidgets.QAction(MainWindow)
        self.action4.setObjectName("action4")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menufile.addAction(self.action1)
        self.menufile.addAction(self.action2)
        self.menufile.addSeparator()
        self.menufile.addAction(self.action3)
        self.menufile.addAction(self.action4)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionClose)
        self.menubar.addAction(self.menufile.menuAction())
        self.action1.triggered.connect(self.addnum)
        self.action2.triggered.connect(self.infocheck)
        self.action3.triggered.connect(self.clearall)
        self.action4.triggered.connect(self.createtable)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def addnum(self):
        #Add new order to databse
        global ok1
        dialog = QInputDialog()
        '''Exception processing'''
        while True:

            try:
                num, ok1 = dialog.getInt(dialog, "Номер заказа", "Введите номер заказа:", QLineEdit.Normal)
                if ok1:
                    QMSG = QMessageBox()
                    QMSG.setWindowTitle("Ошибка")
                    QMSG.setText('Заказ уже существует, введите другой номер')
                    QMSG.exec_()
                else:
                    break

            except IndexError:
                if ok1:
                    name, ok2 = dialog.getText(dialog, "Данные заказчика", "Введите данные заказчика:",
                                               QLineEdit.Normal)
                    if ok2:
                        cost, ok3 = dialog.getDouble(dialog, 'Стоимость заказа', "Введите стоимость заказа:",
                                                     QLineEdit.Normal)
                        if ok3:
                            args, ok4 = dialog.getText(dialog, 'Номера заказов', 'Введите заказы', QLineEdit.Normal)
                            if ok4:
                                OrderLogic.adder(num, name, cost=cost, flag=False, args=args)
                break

    def infocheck(self):
        #Checking database for an order
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
        #Проверка статуса заказа
        data = OrderLogic.loaddb('order', num)
        global SeparData
        SeparData = OrderLogic.Order.separator(data)
        if SeparData['flag']:
            QMSG = QMessageBox()
            QMSG.setWindowTitle("Информация о заказчике")
            QMSG.setText('Заказ уже забран, узнать информацию все равно?')
            QMSG.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            QMSG.buttonClicked.connect(self.stact)

            QMSG.exec_()
        else:
            self.infomessagebox()

    def stact(self, btn):
        #Chech button in MessageBox "Checkstatus"'''
        if btn.text() == 'OK':
            global SeparData
            self.infomessagebox()

    def infomessagebox(self):

        global SeparData
        qmsg = QMessageBox()
        qmsg.setWindowTitle("Информация о заказчике")

        qmsg.setText(
            f"Имя заказчика:{SeparData['name']}\nСтоимость заказа:{SeparData['cost']} рублей\n"
            f"Номера заказов:{SeparData['order']}"
        )
        qmsg.setIcon(QMessageBox.Information)
        chb = QtWidgets.QCheckBox(qmsg)
        chb.setText("Заказ отдан")
        chb.setGeometry(QtCore.QRect(65, 70, 100, 20))

        chb.stateChanged.connect(self.checkboxisclicked)
        if SeparData['flag']:  # Костыль для закрепления чекбокса во включенном состоянии
            chb.setChecked(True)
            Order.changeflag(SeparData['num'])
        qmsg.exec_()

    def checkboxisclicked(self):
        #Checkbox clicked to change flag'''
        global SeparData
        Order.changeflag(SeparData['num'])

    def rowTableCount(self):
        N = OrderLogic.checkcount('order')
        return N

    def clearall(self):
        #Dialogbox to clear all data
        really = QMessageBox()
        really.setIcon(QMessageBox.Question)
        really.setText('Вы действительно хотите удалить все данные?')
        really.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        really.buttonClicked.connect(self.clearaction)
        really.exec_()

    def clearaction(self, btn):
        #ChechButton "ClearAll"
        if btn.text() == 'OK':
            OrderLogic.cleardb()
        else:
            pass

    def createtable(self):
        #Creating table of orders
        TableWindow = QtWidgets.QDialog()
        WinGeom = QDesktopWidget().availableGeometry()
        TableWindow.setGeometry(0, 0, WinGeom.width(), WinGeom.height()-30)
        self.tableWidget = QtWidgets.QTableWidget(TableWindow)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, WinGeom.width(), WinGeom.height()-30))
        self.tableWidget.setRowCount(self.rowTableCount())
        items = 20
        self.tableWidget.setColumnCount(items + 3)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        _translate = QtCore.QCoreApplication.translate
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Заказчик"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Стоимость"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Состояние"))
        for x in range(self.rowTableCount()):
            data = OrderLogic.loaddb('order', x)
            SeparData = OrderLogic.Order.separator(data)
            separOrders = OrderLogic.Order.separateOrders(data)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(SeparData['num'] - 1, 0, item)
            item = self.tableWidget.item(SeparData['num'] - 1, 0)
            item.setText(_translate("MainWindow", f"{SeparData['name']}"))
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(SeparData['num'] - 1, 1, item)
            item = self.tableWidget.item(SeparData['num'] - 1, 1)
            item.setText(_translate("MainWindow", f"{SeparData['cost']}"))
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(SeparData['num'] - 1, 2, item)
            item = self.tableWidget.item(SeparData['num'] - 1, 2)
            if SeparData['flag']:
                item.setText(_translate("MainWindow", "Отдан"))
            else:
                item.setText(_translate("MainWindow", "Не отдан"))
            for i in range(items):
                flag = False
                for p in separOrders.keys():
                    if int(p) == i + 1:
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(SeparData['num'] - 1, i + 3, item)
                        item = self.tableWidget.item(SeparData['num'] - 1, i + 3)
                        item.setText(_translate("MainWindow", f"{separOrders[f'{i + 1}']}"))
                        flag = True
                if not flag:
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(SeparData['num'] - 1, i + 3, item)
                    item = self.tableWidget.item(SeparData['num'] - 1, i + 3)
                    item.setText(_translate("MainWindow", f"0"))
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i + 3, item)
                item = self.tableWidget.horizontalHeaderItem(i + 3)
                item.setText(_translate("MainWindow", f"{i + 1}"))

        TableWindow.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление заказами v 0.9"))
        self.menufile.setTitle(_translate("MainWindow", "Файл"))
        self.action1.setText(_translate("MainWindow", "Новая запись в таблице"))
        self.action2.setText(_translate("MainWindow", "Инфо о записи"))
        self.action3.setText(_translate("MainWindow", "Удалить базу данных"))
        self.action4.setText(_translate("MainWindow", "Показать таблицу"))
        self.actionClose.setText(_translate("MainWindow", "Close"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

