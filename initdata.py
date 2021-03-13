'''self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 621, 271))
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)'''

item = self.tableWidget.verticalHeaderItem(0)
item.setText(_translate("MainWindow", "New Row"))
item = self.tableWidget.horizontalHeaderItem(0)
item.setText(_translate("MainWindow", "Номер заказа"))
item = self.tableWidget.horizontalHeaderItem(1)
item.setText(_translate("MainWindow", "Заказчик"))
item = self.tableWidget.horizontalHeaderItem(2)
item.setText(_translate("MainWindow", "Стоимость"))
item = self.tableWidget.horizontalHeaderItem(3)
item.setText(_translate("MainWindow", "Заказ"))
item = self.tableWidget.horizontalHeaderItem(4)
item.setText(_translate("MainWindow", "Состояние"))
__sortingEnabled = self.tableWidget.isSortingEnabled()
self.tableWidget.setSortingEnabled(False)
item = self.tableWidget.item(0, 0)
item.setText(_translate("MainWindow", "Лол"))
self.tableWidget.setSortingEnabled(__sortingEnabled)





K = '1, 67, 87, 90, 82'
    num = 0
    num2 = 0
    for x in K:
        num += 1
        if x != ',':
            continue
        else:
            L = K[num2:num - 1]
            num2 = num
            print(int(L))


def separator(data):
    num1 = 0
    num2 = 0
    par = 0
    b = []
    name = 0
    cost = 0
    for x in data:
        num1 += 1
        str(data)
        if x != ',':
            continue
        else:
            L = data[num2:num1 - 1]
            if (par) == 0:
                name = L
                par += 1
            elif par == 1:
                cost = int(L)
            else:
                b.append(int(L))
            num2 = num1
            K = dict(name=name, cost=cost, args=b)
            return K
labelCost= QLabel(QMSG)
        labelCost.setText(f"{SeparData['cost']}")
        labelOrders = QLabel(QMSG)
        labelOrders.setText(f"{SeparData['orders']}")

    QMSG.setIcon(QMessageBox.Information)



if SeparData['flag']:
    QMSG = QMessageBox()
    QMSG.setWindowTitle("Информация о заказчике")
    QMSG.setText('Заказ уже забран, узнать информацию все равно?')
    QMSG.setStandardButtons(QMessageBox.Ok)

    QMSG.exec_()
else:
    self.QMB(SeparData)
