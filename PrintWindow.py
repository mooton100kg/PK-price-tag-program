from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from main import print_code, code_convert, sell_price_cal
from datetime import date
from time import sleep
import os
import numpy as np

class Ui_Print_window(object):
    def __init__(self):
        self.info_input = []
        self.info_view = {'Name':[],'Cost':[],'Quantity':[],'Code':[]}
        self.allinfo = pd.read_csv('allinfo.csv', index_col = 0)
        self.AllName = self.allinfo.index.values
        self.AllSupplier = list(self.allinfo)

    def click_confirm(self):
        if self.info_view['Name'] != []:
            self.allinfo.to_csv('allinfo.csv',encoding="utf-8-sig")
            for i, name in enumerate(self.info_view['Name']):
                self.info_input += [name,self.info_view['Code'][i]]*int(self.info_view['Quantity'][i])
            print_code(self.info_input,'printt.xlsx')
            self.info_input = []
            os.startfile('printt.xlsx')
            self.Warning_label.setText("Done!")
            sys.exit(app.exec_())
        else:
            self.Warning_label.setText("Error : Input is Empty")
            self.Warning_label.setStyleSheet("background-color: red;")
        
    def click_enter(self):
        self.Name_Edit.setFocus()
        Name_input = self.Name_Edit.text()
        SellPrice_input = self.SellPrice_Edit.text()
        Cost_input = self.Cost_Edit.text()
        Quantity_input = self.Quantity_Edit.text()
        Supplier_input = self.Supplier_Edit.text()
        if Quantity_input.isnumeric() == True and SellPrice_input.isnumeric() == True and Cost_input.isnumeric() == True and len(Name_input) != 0 and len(Supplier_input) != 0:
            if Supplier_input not in self.AllSupplier:
                self.allinfo[Supplier_input] = np.nan
                if Name_input not in self.AllName:
                    self.allinfo.loc[Name_input] = np.nan
                    self.AllName = self.allinfo.index.values
                self.allinfo.loc[Name_input, Supplier_input] = str(Cost_input) + "|" + str(SellPrice_input)
                self.AllSupplier = list(self.allinfo)
            elif Name_input not in self.AllName:
                self.allinfo.loc[Name_input] = np.nan
                self.AllName = self.allinfo.index.values
                self.allinfo.loc[Name_input, Supplier_input] = str(Cost_input) + "|" + str(SellPrice_input)
            else:
                self.allinfo.loc[Name_input, Supplier_input] = str(Cost_input) + "|" + str(SellPrice_input)
            self.Name_Edit.setCompleter(QtWidgets.QCompleter(self.AllName))
            self.Supplier_Edit.setCompleter(QtWidgets.QCompleter(self.AllSupplier))

            Code_input = code_convert(Cost_input, SellPrice_input, Supplier_input, date.today().strftime('%y'), date.today().strftime('%m'), '3')
            self.Quantity_Edit.clear()
            self.Name_Edit.clear()
            self.Cost_Edit.clear()
            self.SellPrice_Edit.clear()
            self.info_view['Name'].append(Name_input)
            self.info_view['Cost'].append(Cost_input)
            self.info_view['Quantity'].append(Quantity_input)
            self.info_view['Code'].append(Code_input)
            self.setDataInTable()
            self.Warning_label.setStyleSheet("background-color: ;")
            self.Warning_label.setText('')
        elif len(Name_input) == 0 and len(Supplier_input) == 0:
            self.Warning_label.setText("Error : Input is Empty")
            self.Warning_label.setStyleSheet("background-color: red;")
        elif Quantity_input.isnumeric() == False or SellPrice_input.isnumeric() == False or Cost_input.isnumeric() == False:
            self.Warning_label.setText("Error : Incorrect type input")
            self.Warning_label.setStyleSheet("background-color: red;")


    def click_delete(self):
        if self.showinfo.currentRow() >= 0:
            num_del = self.showinfo.currentRow()
        elif self.showinfo.currentRow() < 0:
            num_del = 0
        if len(self.info_view['Name'])-1 < num_del:
            self.Warning_label.setText("Error : No data to delete")
            self.Warning_label.setStyleSheet("background-color: red;")
        else:
            self.info_view['Name'].pop(num_del)
            self.info_view['Cost'].pop(num_del)
            self.info_view['Quantity'].pop(num_del)
            self.info_view['Code'].pop(num_del)
            self.setDataInTable()

    def CostFinishInput(self):
        if len(self.Cost_Edit.text()) != 0 and self.Cost_Edit.text().isnumeric() == True:
            self.Warning_label.setStyleSheet("background-color: ;")
            self.Warning_label.setText('')
            Cost_input = self.Cost_Edit.text()
            SellPrice = sell_price_cal(int(Cost_input))
            self.SellPrice_Edit.setText(str(SellPrice))
            self.SellPrice_Edit.setFocus()           
        else:
            self.Warning_label.setText("Error : No cost input")
            self.Warning_label.setStyleSheet("background-color: red;")

    def CompleterCost(self):
        if len(self.Name_Edit.text()) == 0:
            self.Name_Edit.setFocus()
        elif len(self.Supplier_Edit.text()) != 0 and len(self.Name_Edit.text()) != 0 and self.Name_Edit.text() in self.AllName and self.Supplier_Edit.text() in self.AllSupplier:
            if str(self.allinfo.loc[self.Name_Edit.text(), self.Supplier_Edit.text()]) != 'nan':
                Cost_completer = self.allinfo.loc[self.Name_Edit.text(), self.Supplier_Edit.text()].split("|")[0]
                SellPrice_completer = self.allinfo.loc[self.Name_Edit.text(), self.Supplier_Edit.text()].split("|")[1]
                self.Cost_Edit.setText(str(int(Cost_completer)))
                self.SellPrice_Edit.setText(str(int(SellPrice_completer)))
                self.Quantity_Edit.setFocus()
            else:
                self.Cost_Edit.setFocus()
        elif len(self.Supplier_Edit.text()) != 0 and len(self.Name_Edit.text()) != 0:
            self.Cost_Edit.setFocus()
        

    def setupUi(self, Print_window):
        Print_window.resize(594, 522)
        self.gridLayoutWidget = QtWidgets.QWidget(Print_window)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 0, 441, 351))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setObjectName("gridLayout")

        self.showinfo = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.showinfo.setFrameShape(QtWidgets.QFrame.Box)
        self.showinfo.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.showinfo.setLineWidth(1)
        self.showinfo.setMidLineWidth(0)
        header = self.showinfo.horizontalHeader()       
        self.showinfo.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.showinfo.setObjectName("showinfo")
        self.gridLayout.addWidget(self.showinfo, 0, 1, 5, 2)
        
        self.Confirm_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: self.click_confirm())
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Confirm_Button.setFont(font)
        self.Confirm_Button.setObjectName("Confirm_Button")
        self.gridLayout.addWidget(self.Confirm_Button, 12, 0, 2, 3)
        self.Confirm_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.Warning_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Warning_label.setFont(font)
        self.Warning_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Warning_label.setStyleSheet("background-color: ;")
        self.Warning_label.setObjectName("Warning_label")
        self.gridLayout.addWidget(self.Warning_label, 14, 0, 1, 3)
        
        self.Name_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Name_label.setFont(font)
        self.Name_label.setObjectName("Name_label")
        self.Name_label.setAlignment(QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.Name_label, 6, 0, 1, 1)

        self.Cost_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Cost_label.setFont(font)
        self.Cost_label.setObjectName("Cost_label")
        self.Cost_label.setAlignment(QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.Cost_label, 8, 0, 1, 1)

        self.SellPrice_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.SellPrice_label.setFont(font)
        self.SellPrice_label.setObjectName("SellPrice_label")
        self.SellPrice_label.setText("Sell Price :")
        self.SellPrice_label.setAlignment(QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.SellPrice_label, 9, 0, 1, 1)

        self.SellPrice_Edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.SellPrice_Edit.setFont(font)
        self.SellPrice_Edit.setObjectName("SellPrice_Edit")
        self.SellPrice_Edit.editingFinished.connect(lambda: self.Quantity_Edit.setFocus())
        self.gridLayout.addWidget(self.SellPrice_Edit, 9, 1, 1, 1)

        self.Cost_Edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Cost_Edit.setFont(font)
        self.Cost_Edit.setObjectName("Cost_Edit")
        self.Cost_Edit.editingFinished.connect(lambda: self.CostFinishInput())
        self.gridLayout.addWidget(self.Cost_Edit, 8, 1, 1, 1)

        self.Name_Edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Name_Edit.setFont(font)
        self.Name_Edit.setObjectName("Name_Edit")
        self.Name_Edit.setMaxLength(20)
        self.gridLayout.addWidget(self.Name_Edit, 6, 1, 1, 1)
        self.Name_Edit.setFocus()
        self.Name_Edit.editingFinished.connect(lambda: self.Supplier_Edit.setFocus())
        self.Name_Edit.setCompleter(QtWidgets.QCompleter(self.AllName))
        
        self.Quantity_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Quantity_label.setFont(font)
        self.Quantity_label.setObjectName("Quantity_label")
        self.Quantity_label.setAlignment(QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.Quantity_label, 10, 0, 1, 1)

        self.Quantity_Edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Quantity_Edit.setFont(font)
        self.Quantity_Edit.setObjectName("Quantity_Edit")
        self.Quantity_Edit.editingFinished.connect(lambda: self.Name_Edit.setFocus())
        self.gridLayout.addWidget(self.Quantity_Edit, 10, 1, 1, 1)

        self.Supplier_label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Supplier_label.setFont(font)
        self.Supplier_label.setObjectName("Supplier_label")
        self.Supplier_label.setAlignment(QtCore.Qt.AlignRight)
        self.gridLayout.addWidget(self.Supplier_label, 7, 0, 1, 1)

        self.Supplier_Edit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Supplier_Edit.setFont(font)
        self.Supplier_Edit.setObjectName("Supplier_Edit")
        self.Supplier_Edit.setCompleter(QtWidgets.QCompleter(self.AllSupplier))
        self.Supplier_Edit.editingFinished.connect(lambda: self.CompleterCost())
        self.gridLayout.addWidget(self.Supplier_Edit, 7, 1, 1, 1)

        self.Enter_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: self.click_enter())
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Enter_Button.setFont(font)
        self.Enter_Button.setObjectName("Enter_Button")
        self.Enter_Button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)       
        self.gridLayout.addWidget(self.Enter_Button, 6, 2, 5, 1)

        self.Delete_Button = QtWidgets.QPushButton(self.gridLayoutWidget, clicked = lambda: self.click_delete())
        font = QtGui.QFont()
        font.setPointSize(24)
        self.Delete_Button.setFont(font)
        self.Delete_Button.setObjectName("Delete_Button")
        self.Delete_Button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addWidget(self.Delete_Button, 0, 0, 4, 1)

        Print_window.setCentralWidget(self.gridLayoutWidget)
        self.menubar = QtWidgets.QMenuBar(Print_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 594, 21))

        self.menubar.setObjectName("menubar")
        Print_window.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(Print_window)
        self.statusbar.setObjectName("statusbar")
        Print_window.setStatusBar(self.statusbar)

        self.retranslateUi(Print_window)
        self.setDataInTable()
        QtCore.QMetaObject.connectSlotsByName(Print_window)
    
    def setDataInTable(self):
        self.showinfo.setColumnCount(4)
        self.showinfo.setRowCount(len(self.info_view['Name']))
        Header = []
        for n,key in enumerate(self.info_view.keys()):
            Header.append(key)
            for m, item in enumerate(self.info_view[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.showinfo.setItem(m, n, newitem)
            self.showinfo.setHorizontalHeaderLabels(Header)
            
    def retranslateUi(self, Print_window):
        _translate = QtCore.QCoreApplication.translate
        Print_window.setWindowTitle(_translate("Print_window", "MainWindow"))
        self.Confirm_Button.setText(_translate("Print_window", "Confirm"))
        self.Name_label.setText(_translate("Print_window", " Name :"))
        self.Cost_label.setText(_translate("Print_window", " Cost :"))
        self.Quantity_label.setText(_translate("Print_window", " Quantity :"))
        self.Enter_Button.setText(_translate("Print_window", "Enter"))
        self.Delete_Button.setText(_translate("Print_window", "Delete"))
        self.Supplier_label.setText(_translate("Print_window", " Supplier :"))
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Print_window = QtWidgets.QMainWindow()
    ui = Ui_Print_window()
    ui.setupUi(Print_window)
    Print_window.show()
    sys.exit(app.exec_())
    
