import OrderLogic
from OrderLogic import Order
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QVBoxLayout, QDesktopWidget, QFileDialog
file_name = 'order'

class Ui_MainWindow(object):


    def setupui(self, MainWindow):
        # Creating GUI on MainWindow

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
        self.button3 = QtWidgets.QPushButton("Открыть таблицу заказов")
        self.Vbox = QVBoxLayout(self.centralwidget)
        self.ButtonGroup = QtWidgets.QButtonGroup(self.centralwidget)
        self.Vbox.addWidget(self.button1)
        self.Vbox.addWidget(self.button2)
        self.Vbox.addWidget(self.button3)
        self.button1.clicked.connect(self.addnum)
        self.button2.clicked.connect(self.infocheck)
        self.button3.clicked.connect(self.createtable)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 624, 24))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        MainWindow.setMenuBar(self.menubar)
        self.actionMenu1 = QtWidgets.QAction(MainWindow)
        self.actionMenu1.setObjectName("actionMenu1")
        self.actionMenu2 = QtWidgets.QAction(MainWindow)
        self.actionMenu2.setObjectName("actionMenu2")
        self.actionMenu3 = QtWidgets.QAction(MainWindow)
        self.actionMenu3.setObjectName("actionMenu3")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menufile.addAction(self.actionMenu1)
        self.menufile.addAction(self.actionMenu2)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionMenu3)
        self.menubar.addAction(self.menufile.menuAction())
        self.actionMenu1.triggered.connect(self.loadfile)
        self.actionMenu2.triggered.connect(self.savefile)
        self.actionMenu3.triggered.connect(self.clearall)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def addnum(self):
        # Add new order to databse
        global ok1, file_name
        dialog = QInputDialog()

        '''Exception processing'''
        while True:

            try:
                num, ok1 = dialog.getInt(dialog, "Номер заказа", "Введите номер заказа:", QLineEdit.Normal)
                if ok1:
                    data=OrderLogic.loaddb(file_name, num)
                    qmsg = QMessageBox()
                    qmsg.setWindowTitle("Ошибка")
                    qmsg.setText('Заказ уже существует, введите другой номер')
                    qmsg.exec_()
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
                                OrderLogic.adder(file_name,num, name, cost=cost, flag=False, args=args)
                break

    def ramfile(self):
        OrderLogic.cleardb()
        global file_name
        file_name = 'order'

    def infocheck(self):
        # Checking database for an order
        dialog = QInputDialog()
        num, ok = dialog.getInt(dialog, 'Номер заказа', 'Введите номер заказа:', QLineEdit.Normal)

        while True:
            try:
                if ok:
                    self.checkstatus(num)
                break
            except IndexError:
                qmsg = QMessageBox()
                qmsg.setWindowTitle("Ошибка")
                qmsg.setText('Такого заказа нету в базе, попробуйте еще раз?')
                qmsg.exec_()
                num, ok = dialog.getInt(dialog, 'Номер заказа', 'Введите номер заказа:', QLineEdit.Normal)

    def checkstatus(self, num):
        # Проверка статуса заказа
        global file_name
        data = OrderLogic.loaddb(file_name, num)
        global SeparData
        SeparData = OrderLogic.Order.separator(data)
        if SeparData['flag']:
            qmsg = QMessageBox()
            qmsg.setWindowTitle("Информация о заказчике")
            qmsg.setText('Заказ уже забран, узнать информацию все равно?')
            qmsg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            qmsg.buttonClicked.connect(self.stact)

            qmsg.exec_()
        else:
            self.infomessagebox()

    def stact(self, btn):
        # Chech button in MessageBox "Checkstatus"'''
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
            Order.changeflag(SeparData['num'], file_name)
        qmsg.exec_()

    def loadfile(self):
        file_name, ok = QFileDialog.getOpenFileName(caption='Open File')
        if ok:
            OrderLogic.loadfile(file_name)
    def savefile(self):
        file_name, ok =QFileDialog.getSaveFileName(caption='Save File')
        if ok:
            OrderLogic.savefile(file_name)

    def checkboxisclicked(self):
        # Checkbox clicked to change flag
        global SeparData
        Order.changeflag(SeparData['num'], file_name)

    def rowtablecount(self):
        n = OrderLogic.checkcount(file_name)
        return n

    def clearall(self):
        # Dialogbox to clear all data
        really = QMessageBox()
        really.setIcon(QMessageBox.Question)
        really.setText('Вы действительно хотите создать новый документ?')
        really.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        really.buttonClicked.connect(self.clearaction)
        really.exec_()

    def clearaction(self, btn):
        # ChechButton "ClearAll"
        if btn.text() == 'OK':
            self.ramfile()
        else:
            pass

    def createtable(self):
        # Creating table of orders
        tablewindow = QtWidgets.QDialog()
        WinGeom = QDesktopWidget().availableGeometry()
        tablewindow.setGeometry(0, 0, WinGeom.width(), WinGeom.height() - 30)
        self.tableWidget = QtWidgets.QTableWidget(tablewindow)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, WinGeom.width(), WinGeom.height() - 30))
        self.tableWidget.setRowCount(self.rowtablecount())
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
        for x in range(self.rowtablecount()):
            data = OrderLogic.loaddb(file_name, x)
            separdata = OrderLogic.Order.separator(data)
            separOrders = OrderLogic.Order.separateOrders(data)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(separdata['num'] - 1, 0, item)
            item = self.tableWidget.item(separdata['num'] - 1, 0)
            item.setText(_translate("MainWindow", f"{separdata['name']}"))
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(separdata['num'] - 1, 1, item)
            item = self.tableWidget.item(separdata['num'] - 1, 1)
            item.setText(_translate("MainWindow", f"{separdata['cost']}"))
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(separdata['num'] - 1, 2, item)
            item = self.tableWidget.item(separdata['num'] - 1, 2)
            if separdata['flag']:
                item.setText(_translate("MainWindow", "Отдан"))
            else:
                item.setText(_translate("MainWindow", "Не отдан"))
            for i in range(items):
                flag = False
                for p in separOrders.keys():
                    if int(p) == i + 1:
                        item = QtWidgets.QTableWidgetItem()
                        self.tableWidget.setItem(separdata['num'] - 1, i + 3, item)
                        item = self.tableWidget.item(separdata['num'] - 1, i + 3)
                        item.setText(_translate("MainWindow", f"{separOrders[f'{i + 1}']}"))
                        flag = True
                if not flag:
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(separdata['num'] - 1, i + 3, item)
                    item = self.tableWidget.item(separdata['num'] - 1, i + 3)
                    item.setText(_translate("MainWindow", f"0"))
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(i + 3, item)
                item = self.tableWidget.horizontalHeaderItem(i + 3)
                item.setText(_translate("MainWindow", f"{i + 1}"))

        tablewindow.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Управление заказами"))
        self.menufile.setTitle(_translate("MainWindow", "Файл"))
        self.actionMenu1.setText(_translate("MainWindow", "Загрузить файл"))
        self.actionMenu2.setText(_translate("MainWindow", "Сохранить файл"))
        self.actionMenu3.setText(_translate("MainWindow", "Новый файл"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
