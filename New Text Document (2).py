# import PyQt5 module
import pyautogui
import pywhatkit
from PyQt5.QtCore import QStringListModel, QDate, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QHeaderView, QMessageBox, QAction, \
    QMainWindow, QLabel, QTableWidgetItem, QVBoxLayout, QCompleter
from PyQt5.uic import loadUiType

# import pandas as pd
import sqlite3
import sys
from os import path
import winsound
import time

# import UI file
FORM_CLASS, _ = loadUiType(path.join(path.dirname('untitled.ui'), 'untitled.ui'))


class mainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        # QMainWindow.__init__(self)
        self.n = 0  # ch1
        self.redu = ""
        self.additional_text = None
        self.amoun = 0
        self.s_name = None
        self.setupUi(self)
        self.ui_changes()
        self.controllers()
        self.set_date_from_device()

        # self.send_message()

    def ui_changes(self):
        # make tableWidget extend with window
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 125)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 40)
        self.tableWidget.setColumnWidth(6, 40)
        self.tableWidget.setColumnWidth(7, 40)
        self.tableWidget.setColumnWidth(8, 60)

        # make tableWidget for detailed window
        self.tableWidget_3.setColumnWidth(0, 120)
        self.tableWidget_3.setColumnWidth(1, 100)
        self.tableWidget_3.setColumnWidth(2, 120)
        self.tableWidget_3.setColumnWidth(4, 120)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

        # make tableWidget_2 for detailed window
        self.tableWidget_2.setColumnWidth(0, 400)
        self.tableWidget_2.setColumnWidth(1, 100)

        # make tableWidget for detailed window
        self.tableWidget_4.setColumnWidth(0, 670)
        self.tableWidget_4.setRowCount(0)

        ### fill the factories combo
        self.fill_facCombo_from_database()

    def controllers(self):
        ### main interface controllers
        # fill the table of main face
        self.fill_main_table()
        # search in main window table
        self.lineEdit.textChanged.connect(self.check_text)
        # search in main window table
        self.lineEdit_4.textChanged.connect(self.search_in_tableWidget_4)
        # click on table cell
        self.tableWidget.cellDoubleClicked.connect(self.double_clickonTable)

        # when comboBox_5 changes
        self.comboBox_5.currentIndexChanged.connect(self.auto_change_combobox)

        # set months for reduce search
        self.lineEdit_203.editingFinished.connect(self.red_set)
        self.lineEdit_197.editingFinished.connect(self.add_set)
        self.lineEdit_199.editingFinished.connect(self.debt_set)

        # menubar events
        self.menu.triggered[QAction].connect(self.menu_function)
        self.menu_2.triggered[QAction].connect(self.menu2_function)

        ### fill daily table
        self.comboBox_2.currentIndexChanged.connect(self.filer_names)
        ### add shift
        self.pushButton.clicked.connect(self.add_shift)
        ### applay salary
        self.pushButton_8.clicked.connect(self.apply_taking_salary)
        # exit button
        self.tableWidget_2.cellClicked.connect(self.btn_exit)

        ### add new person controller
        self.pushButton_2.clicked.connect(self.add_person)
        ### edit person
        self.auto_compelete_for_edit()
        self.pushButton_5.clicked.connect(self.get_data_to_edit)
        self.pushButton_6.clicked.connect(self.edit_person)
        ### delete person
        self.pushButton_7.clicked.connect(self.delete_person)

        ### additional controllers
        self.pushButton_11.clicked.connect(self.get_data_to_additional)
        self.pushButton_13.clicked.connect(self.sum_in_additional)
        self.pushButton_3.clicked.connect(self.additional_to_database)

        ### reduce controllers
        self.pushButton_14.clicked.connect(self.get_data_to_reduce)
        self.pushButton_10.clicked.connect(self.sum_in_reduced)
        self.pushButton_9.clicked.connect(self.reduce_to_database)

        ### debt controllers
        self.pushButton_12.clicked.connect(self.get_data_to_debt)
        self.pushButton_15.clicked.connect(self.sum_in_debt)
        self.pushButton_4.clicked.connect(self.debt_to_database)

    ########################################################################################################################
    # gerneral function
    def set_date_from_device(self):
        device_time = time.localtime()
        self.dateEdit.setDate(QDate(device_time[0], device_time[1], device_time[2]))
        self.dateEdit_2.setDate(QDate(device_time[0], device_time[1], device_time[2]))

        if device_time[6] == 0:
            self.comboBox_3.setCurrentIndex(2)
        elif device_time[6] == 1:
            self.comboBox_3.setCurrentIndex(3)
        elif device_time[6] == 2:
            self.comboBox_3.setCurrentIndex(4)
        elif device_time[6] == 3:
            self.comboBox_3.setCurrentIndex(5)
        elif device_time[6] == 4:
            self.comboBox_3.setCurrentIndex(6)
        elif device_time[6] == 5:
            self.comboBox_3.setCurrentIndex(0)
        else:
            self.comboBox_3.setCurrentIndex(1)

    # produce sound when click
    def click_voice(self):
        winsound.PlaySound(r"voices\click-voice.wav", winsound.SND_FILENAME)

    # menubar function
    def menu_function(self, q):
        if q.text() == 'الصفحة الرئيسة':
            self.stackedWidget.setCurrentIndex(0)
        if q.text() == 'صفحة تسجيل الحضور':
            self.stackedWidget.setCurrentIndex(1)
        if q.text() == 'صفحة إضافة وتعديل شخص':
            self.stackedWidget.setCurrentIndex(2)
        if q.text() == 'إضافة مصنع':
            self.add_factory()

    # menubar function
    def menu2_function(self, q):
        self.stackedWidget.setCurrentIndex(4)
        if q.text() == 'الإضافي':
            # addtional controllers
            self.auto_compelete_additional()
            self.stackedWidget_2.setCurrentIndex(0)
        if q.text() == 'الخصومات':
            # reduce controllers
            self.auto_compelete_reduce()
            self.stackedWidget_2.setCurrentIndex(1)
        if q.text() == 'السلف':
            # debt controllers
            self.auto_compelete_debt()
            self.stackedWidget_2.setCurrentIndex(2)

    def btn_exit(self, row, column):
        if column == 1:
            # delete value from table
            items = self.tableWidget_2.item(row, 0).text()
            self.tableWidget_2.removeRow(row)
            self.tableWidget_4.insertRow(self.tableWidget_4.rowCount())
            self.tableWidget_4.setItem(self.tableWidget_4.rowCount() - 1, 0, QTableWidgetItem(items))

    def fill_month_combos(self, persn_name):
        db = sqlite3.connect('database.db')
        cr1 = db.cursor()
        cr1.execute('''SELECT DISTINCT month FROM attendance WHERE name='{}' '''.format(persn_name))
        mnths = cr1.fetchall()
        db.commit()
        db.close()
        # return mnths for specific person
        return mnths

    def debt_set(self):
        t1 = self.lineEdit_199.text()
        items = self.fill_month_combos(t1)
        self.comboBox_8.clear()
        for i in items:
            self.comboBox_8.addItem(str(i[0]))

    def add_set(self):
        t2 = self.lineEdit_197.text()
        items = self.fill_month_combos(t2)
        self.comboBox_7.clear()
        for i in items:
            self.comboBox_7.addItem(str(i[0]))

    def red_set(self):
        t3 = self.lineEdit_203.text()
        items = self.fill_month_combos(t3)
        self.comboBox_6.clear()
        for i in items:
            self.comboBox_6.addItem(str(i[0]))

    ################################################################## add factory functions ###########################
    ####### fill_facCombo_from_database
    def fill_facCombo_from_database(self):
        # get factories names
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute('''SELECT name FROM factName''')
        facNames = cr.fetchall()
        db.close()

        # add the factories names to combobox
        for i in facNames:
            self.comboBox.addItem(i[0])
            self.comboBox_9.addItem(i[0])
            self.comboBox_10.addItem(i[0])
            self.comboBox_19.addItem(i[0])
            self.comboBox_15.addItem(i[0])
            self.comboBox_12.addItem(i[0])

    def add_factory(self):
        self.widg = QWidget()
        self.widg.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.widg.setStyleSheet('''background-color:rgb(73, 69, 200);''')

        self.line1 = QLineEdit()
        self.line1.setPlaceholderText('أدخل أسم المصنع')
        self.line1.setStyleSheet('''background-color:white;''')

        self.line2 = QLineEdit()
        self.line2.setPlaceholderText('أدخل سعر اليومية')
        self.line2.setStyleSheet('''background-color:white;''')

        self.btn = QPushButton('موافق')
        self.btn.setStyleSheet('''background-color:green;''')
        self.btn.clicked.connect(self.add_new_factory)

        self.Vbox = QVBoxLayout(self.widg)
        self.Vbox.addWidget(self.line1)
        self.Vbox.addWidget(self.line2)
        self.Vbox.addWidget(self.btn)
        self.widg.setLayout(self.Vbox)

        self.widg.resize(400, 170)
        self.widg.show()

    def add_new_factory(self):
        # get from new window lineEdits
        n_fac = self.line1.text()
        n_salary = int(self.line2.text())
        # # add to database
        db = sqlite3.connect("database.db")
        cr = db.cursor()
        cr.execute('''INSERT INTO factName(name, salary) VALUES('{}',{}) '''.format(n_fac, n_salary))
        db.commit()
        db.close()

        # clean combo before addition
        self.comboBox.clear()
        self.comboBox_9.clear()
        self.comboBox_10.clear()

        # update combobox factories
        self.fill_facCombo_from_database()

        # close window after addition
        self.widg.close()

    ################################### Add and edit and delete person ###############################################
    #### add new person to database
    def add_person(self):
        try:
            self.click_voice()
            ###fetch data from LineEdits
            p_name = self.lineEdit_179.text()
            p_phone = self.lineEdit_181.text()
            p_national = self.lineEdit_180.text()
            p_factoryName = self.comboBox_9.currentText()
            p_factoryNight = self.comboBox_4.currentText()

            ###insert data into database
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            cr.execute('''INSERT INTO workers(name, phone, national, fac_name, fac_night) VALUES('{}', '{}','{}','{}',
            '{}')'''.format(p_name, p_phone, p_national, p_factoryName, p_factoryNight))
            db.commit()
            db.close()

            # delete cells after record
            self.lineEdit_179.setText("")
            self.lineEdit_180.setText("")
            self.lineEdit_181.setText("")
            self.comboBox_9.setCurrentText(self.comboBox_9.itemText(0))
            self.comboBox_4.setCurrentText(self.comboBox_4.itemText(0))

            # update the lineEdit after adding
            self.auto_compelete_for_edit()

            # refresh the main table
            self.fill_main_table()

            # show ensure message
            self.statusBar().showMessage("تم إضافة {}".format(p_name), 5000)
        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText('هذا الأسم موجود بالفعل لديك من قبل,فقط قم بتعديل بياناته')
            msg.exec_()

    ######################################## edit&delete methods#######################
    def auto_compelete_for_edit(self):
        self.names_list = []
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        names = cr.execute('''select name from workers''')
        all = names.fetchall()
        for n in all:
            self.names_list.append(n[0])

        # create Qcompeleter and add it to Widget
        completer = QCompleter()
        self.lineEdit_191.setCompleter(completer)
        # create model and add list to it
        model = QStringListModel()
        model.setStringList(self.names_list)
        # add model to compeleter
        completer.setModel(model)

    #### edit  person to database
    def get_data_to_edit(self):
        # get user data from database
        self.s_name = self.lineEdit_191.text()
        try:
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            names = cr.execute('''select * from workers WHERE name='{}' '''.format(self.s_name))
            all_of_person = names.fetchone()
            db.commit()
            db.close()

            # put the in the cells
            self.lineEdit_183.setText(all_of_person[0])
            self.lineEdit_184.setText(all_of_person[1])
            self.lineEdit_193.setText(all_of_person[2])
            self.comboBox_10.setCurrentText(all_of_person[3])
            self.comboBox_11.setCurrentText(all_of_person[4])
        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText('هذا الأسم غير موجود, ربما قمت بحذفه')
            msg.exec_()

    # function that do the edit task
    def edit_person(self):
        # get the data from the cells after editing
        a_name = self.lineEdit_183.text()
        a_phone = self.lineEdit_184.text()
        a_national = self.lineEdit_193.text()
        a_factorName = self.comboBox_10.currentText()
        a_factoryNight = self.comboBox_11.currentText()

        # put the modified data into the database
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''UPDATE workers SET name='{}',phone='{}',national='{}',fac_name='{}',fac_night='{}' WHERE 
        name='{}' '''.format(a_name, a_phone, a_national, a_factorName, a_factoryNight, self.s_name))
        db.commit()
        db.close()

        # clear the cells after edit process
        self.lineEdit_183.setText("")
        self.lineEdit_184.setText("")
        self.lineEdit_193.setText("")
        self.comboBox_10.setCurrentText(self.comboBox_10.itemText(0))
        self.comboBox_11.setCurrentText(self.comboBox_11.itemText(0))
        # clear search cell
        self.lineEdit_191.setText("")

        # update the search lineEdit after edit data
        self.auto_compelete_for_edit()

        # refresh the main table
        self.fill_main_table()

        # show ensure message
        self.statusBar().showMessage("تم تعديل {}".format(a_name), 5000)

    def delete_person(self):
        # get the data from the cells after editing
        d_name = self.lineEdit_191.text()
        d_national = self.lineEdit_193.text()
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''DELETE FROM workers WHERE national='{}' '''.format(d_national))
        db.commit()
        db.close()

        # clear the cells after edit process
        self.lineEdit_183.setText("")
        self.lineEdit_184.setText("")
        self.lineEdit_193.setText("")
        self.comboBox_10.setCurrentText(self.comboBox_10.itemText(0))
        self.comboBox_11.setCurrentText(self.comboBox_11.itemText(0))
        # clear search cell
        self.lineEdit_191.setText("")

        # update search lineEdit after delete
        self.auto_compelete_for_edit()

        # refresh the main table
        self.fill_main_table()

        # show ensure message
        self.statusBar().showMessage("تم حذف {}".format(d_name), 5000)

    ################################################ functions of record shifts ###########################################
    ######## filer by factory_name and factory_shift
    def filer_names(self, t):
        factory_name = self.comboBox.currentText()
        if factory_name != 'أختر أسم المصنع':
            # get factory name, shift from combo
            fShift = self.comboBox_2.itemText(t)
            ### get data from database
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            cr.execute(
                '''SELECT name FROM workers WHERE fac_name='{}' and fac_night='{}' ORDER BY name ASC'''.format(
                    factory_name, fShift))
            data = cr.fetchall()
            db.commit()
            db.close()

            ## fill table
            self.tableWidget_2.setRowCount(0)
            for row, row_data in enumerate(data):
                self.tableWidget_2.insertRow(row)
                for column, column_data in enumerate(row_data):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(column_data)))

            # add labels to tables
            for i, _ in enumerate(data):
                # add pushbutton to table widget
                self.lbl = QLabel('إضافة', self)
                self.lbl.setAlignment(Qt.AlignCenter)
                self.lbl.setStyleSheet(
                    'QLabel{background-color:rgb(0,255,0);color:red;font-size:15px;border-radius:0.5px;}'
                    'QLabel::hover{color:blue;background-color:rgb(255,255,0);}')
                self.tableWidget_2.setCellWidget(i, 1, self.lbl)

        if factory_name == 'أختر أسم المصنع' and self.comboBox_2.currentIndex() != 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('ملاحظة')
            msg.setInformativeText('يجب إختيار أسم المصنع أولا')
            msg.exec_()

            # set comboBox_2 to default "أختر أسم الوردية"
            self.comboBox_2.setCurrentIndex(0)

    def add_shift(self):
        row_number = self.tableWidget_4.rowCount()
        mon = int(str(self.dateEdit.date().toPyDate())[5:7])
        data = []
        for row in range(row_number):
            items = self.tableWidget_4.item(row, 0)
            data.append(items.text())

        # data that will added to attendance
        g_datehistory = str(self.dateEdit.date().toPyDate())
        g_dayName = self.comboBox_3.currentText()
        g_factoryname = self.comboBox.currentText()
        g_shift = self.comboBox_2.currentText()

        # get all attendance from databse to check if he attend before
        db = sqlite3.connect('database.db')
        cr1 = db.cursor()
        cr1.execute('''SELECT name,factory,shift FROM attendance WHERE date='{}' '''.format(g_datehistory))
        previous = cr1.fetchall()
        db.commit()
        db.close()

        # # add the people who addtend to database
        for i in data:
            for j in previous:
                if i == j[0]:
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("تنبيه")
                    msg.setInformativeText(
                        "هذا الأسم:{0} متكرر\n تم تسجيل حضوره في نفس اليوم:{1}\n  من قبل في عربية:{2} "
                        " وردية:{3}\n   لذلك لن يسجله البرنامج في هذه المصنع".format(j[0],
                                                                                     g_datehistory,
                                                                                     j[1],
                                                                                     j[2]))
                    msg.exec_()

                    # exit from the loop if name repeated
                    break
            else:
                # record today_names
                db = sqlite3.connect('database.db')
                cr = db.cursor()
                cr.execute(
                    '''INSERT INTO attendance VALUES('{}','{}','{}','{}','{}', {})'''.format(i, g_datehistory,
                                                                                             g_dayName,
                                                                                             g_factoryname, g_shift,
                                                                                             mon))
                db.commit()
                db.close()

                # clear the table after adding the shift
                self.tableWidget_4.setRowCount(0)

                # clear cells and table rows
                self.comboBox.setCurrentIndex(0)
                self.comboBox_2.setCurrentIndex(0)

                # refresh the table after adding the shift
                self.fill_main_table()

                # show ensure message
                self.statusBar().showMessage("تم إضافة الوردية بنجاح", 5000)

        # clear the table after adding the shift
        self.tableWidget_4.setRowCount(0)

        # clear cells and table rows
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)

    def apply_taking_salary(self):
        try:
            # get the name and month from interface
            nn_name = self.label_2.text()
            nn_month = self.comboBox_5.currentText()
            print(nn_name, nn_month)
            # delete the month data from attendance
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            # delete from attendance
            cr.execute('''DELETE FROM attendance WHERE name='{}' and month={} '''.format(nn_name, nn_month))
            # delete from attendance
            cr.execute('''DELETE FROM additional WHERE namev='{}' and add_month={} '''.format(nn_name, nn_month))
            # delete from debt
            cr.execute('''DELETE FROM debt WHERE name='{}' and debt_month={} '''.format(nn_name, nn_month))
            # delete from attendance
            cr.execute('''DELETE FROM reduced WHERE name='{}' and red_month={} '''.format(nn_name, nn_month))
            # commit after delete process
            db.commit()
            db.close()

            ### refresh main table after apply salary
            self.fill_main_table()

            #### clear cells after apply salary
            # clear the cells after edit process
            self.lineEdit_3.setText("")
            self.lineEdit_2.setText("")
            self.tableWidget_3.setRowCount(0)
            items = self.fill_month_combos(nn_name)
            print(items)
            # self.comboBox_5.clear()
            # for i in items:
            #     self.comboBox_5.addItem(str(i[0]))
            #
            self.statusBar().showMessage("لقد قبض :{0} مرتب شهر {1} بنجاح".format(nn_name, nn_month), 5000)
        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText(
                'تنبيه هذا الشخص ليس له حضور\n مما يعني أنه قد قبض مرتبه بالفعل في هذا الشهر أو لم يحضر هذا الشهر')
            msg.exec_()

    # changing the comboBox value
    def auto_change_combobox(self):
        if self.n == 3:  # ch2
            manth = self.comboBox_5.currentText()
            nmn_name = self.label_2.text()

            # get data about salay
            n_days, s_salary, d1, d2, d3 = self.get_salary(nmn_name, manth)
            # get the net salary
            net_salary = s_salary - int(d1) + int(d2) - int(d3)
            self.lineEdit_2.setText(str(net_salary))  # salary
            self.lineEdit_3.setText(str(n_days))  # no_of days

            db = sqlite3.connect('database.db')
            cr = db.cursor()
            cr.execute(
                '''SELECT date,dayname,factory,shift FROM attendance WHERE name='{}' and month={} '''.format(nmn_name,
                                                                                                             manth))
            data = cr.fetchall()
            db.commit()
            db.close()

            self.tableWidget_3.setRowCount(0)
            for row_number, row_data in enumerate(data):
                self.tableWidget_3.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    self.tableWidget_3.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
            # reduced value in this month
            self.tableWidget_3.setItem(0, 4, QTableWidgetItem(d3))
        self.n = self.stackedWidget.currentIndex()  # ch3

    # search in attendance tableWidget
    def search_in_tableWidget_4(self):
        fact = self.comboBox.currentText()
        shift = self.comboBox_2.currentText()

        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''SELECT name FROM workers WHERE name LIKE '{}%' and fac_name='{}' and fac_night='{}' ORDER BY name 
        ASC'''.format(self.lineEdit_4.text(), fact, shift))
        all_data = cr.fetchall()
        db.commit()
        db.close()

        # get the data from right table of attendance
        arry = []
        for row in range(self.tableWidget_4.rowCount()):
            items = self.tableWidget_4.item(row, 0).text()
            arry.append(items)

        # remove names exists in right table from left table
        for a in all_data:
            if a[0] in arry:
                all_data.remove(a)

        # fill table while search
        self.tableWidget_2.setRowCount(0)
        for row_number, row_data in enumerate(all_data):
            self.tableWidget_2.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.tableWidget_2.setItem(row_number, column_number, QTableWidgetItem(column_data))

        # add labels to tables
        for i, _ in enumerate(all_data):
            # add pushbutton to table widget
            self.lbl = QLabel('إضافة', self)
            self.lbl.setAlignment(Qt.AlignCenter)
            self.lbl.setStyleSheet(
                'QLabel{background-color:rgb(0,255,0);color:red;font-size:15px;border-radius:0.5px;}'
                'QLabel::hover{color:blue;background-color:rgb(255,255,0);}')
            self.tableWidget_2.setCellWidget(i, 1, self.lbl)

    #################################################السلف والخصومات والإضافي #####################################################
    ##################################################################
    def auto_compelete_additional(self):
        self.names_list = []
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        names = cr.execute('''select name from workers''')
        all = names.fetchall()
        for n in all:
            self.names_list.append(n[0])

        # create Qcompeleter and add it to Widget
        completer = QCompleter()
        self.lineEdit_197.setCompleter(completer)
        # create model and add list to it
        model = QStringListModel()
        model.setStringList(self.names_list)
        # add model to compeleter
        completer.setModel(model)

    #### get reduced person to database
    def get_data_to_additional(self):
        # get user data from database
        o_name = self.lineEdit_197.text()
        monthk = int(self.comboBox_7.currentText())
        try:
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            workersdata = cr.execute(
                '''select name, fac_name, fac_night from workers WHERE name='{}' '''.format(o_name))
            cr1 = db.cursor()
            debtdata = cr1.execute(
                '''select amountv, datesv from additional WHERE namev='{}' and add_month={} '''.format(o_name, monthk))
            all_of_person = workersdata.fetchone()
            all_of_person1 = debtdata.fetchone()
            db.commit()
            db.close()

            # put the in the cells
            self.lineEdit_186.setText(all_of_person[0])
            self.comboBox_12.setCurrentText(all_of_person[1])
            self.comboBox_13.setCurrentText(all_of_person[2])

            if all_of_person1 == None:
                db = sqlite3.connect('database.db')
                cr = db.cursor()
                cr.execute(
                    '''INSERT INTO additional(namev, add_month) VALUES('{}', {})'''.format(all_of_person[0], monthk))
                db.commit()
                db.close()

                # old additional dates
                self.plainTextEdit_2.setPlainText(
                    "\n\nلم يتم وضع إضافي لهذا الشخص من قبل                                                   ")

            else:
                self.amoun = int(all_of_person1[0])
                self.additional_text = all_of_person1[1]

        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText('هذا الأسم غير موجود, ربما قمت بحذفه')
            msg.exec_()

    def sum_in_additional(self):
        # get the data from the cells after editing
        numberofhours = self.lineEdit_187.text()
        onehourprice = self.lineEdit_188.text()
        sum_red = int(numberofhours) * int(onehourprice)
        self.lineEdit_190.setText(str(sum_red))
        new_additional = sum_red + self.amoun
        self.lineEdit_198.setText(str(new_additional))

        additional_date = str(self.dateEdit.date().toPyDate())
        # add new additional
        if self.additional_text == None:
            additional_date = str(self.dateEdit.date().toPyDate())
            self.plainTextEdit_2.setPlainText(
                'قيمة الإضافي هي {0} وتاريخ إضافته هو {1}'.format(str(sum_red), additional_date))
        else:
            self.plainTextEdit_2.setPlainText(
                '                                   {0}\nقيمة الإضافي هي {1} وتاريخ إضافته هو {2}'.format(
                    self.additional_text, str(sum_red), additional_date))

    # function that do the edit task
    def additional_to_database(self):
        # get the data from the cell before updating
        n_name = self.lineEdit_186.text()
        sum_additional = self.lineEdit_198.text()
        old_dates = self.plainTextEdit_2.toPlainText()
        mnn = int(self.comboBox_7.currentText())
        # put the modified data into the database
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''UPDATE additional SET amountv='{}',datesv='{}' WHERE
        namev='{}' and add_month={}'''.format(sum_additional, old_dates, n_name, mnn))
        db.commit()
        db.close()

        # clear the cells after edit process
        self.lineEdit_197.setText("")
        self.lineEdit_208.setText("")
        self.comboBox_12.setCurrentText(self.comboBox_12.itemText(0))
        self.comboBox_13.setCurrentText(self.comboBox_13.itemText(0))
        self.comboBox_7.setCurrentText(self.comboBox_7.itemText(0))
        self.lineEdit_186.setText("")
        self.lineEdit_187.setText("")
        self.lineEdit_188.setText("")
        self.lineEdit_190.setText("")
        self.lineEdit_198.setText("")

        # refresh the table after adding additional hours
        self.fill_main_table()

        # show ensure message
        self.statusBar().showMessage("تم تسجيل الساعات الإضافية بنجاح للضخص :{}".format(n_name), 5000)

    ######################################################################################################################################
    ###################### reduce part ##################################
    def auto_compelete_reduce(self):
        names_list = []
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        names = cr.execute('''select name from workers''')
        all = names.fetchall()
        for n in all:
            names_list.append(n[0])

        # create Qcompeleter and add it to Widget
        completer = QCompleter()
        self.lineEdit_203.setCompleter(completer)
        # create model and add list to it
        model = QStringListModel()
        model.setStringList(self.names_list)
        # add model to compeleter
        completer.setModel(model)

    #### get reduced person to database
    def get_data_to_reduce(self):
        # get user data from database
        o_name = self.lineEdit_203.text()
        mnth = self.comboBox_6.currentText()
        try:
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            workersdata = cr.execute(
                '''select name, fac_name, fac_night from workers WHERE name='{}' '''.format(o_name))
            cr1 = db.cursor()
            debtdata = cr1.execute(
                '''select amount,reason from reduced WHERE name='{}' and red_month={} '''.format(o_name, mnth))
            all_of_person = workersdata.fetchone()
            all_of_person1 = debtdata.fetchone()
            db.commit()
            db.close()

            # put the in the cells
            self.lineEdit_192.setText(all_of_person[0])
            self.comboBox_19.setCurrentText(all_of_person[1])
            self.comboBox_18.setCurrentText(all_of_person[2])

            if all_of_person1 == None:
                db = sqlite3.connect('database.db')
                cr = db.cursor()
                cr.execute('''INSERT INTO reduced(name, red_month) VALUES('{}', {})'''.format(all_of_person[0], mnth))
                db.commit()
                db.close()
                self.lineEdit_206.setText('0')
            else:
                self.lineEdit_206.setText(all_of_person1[0])
                self.plainTextEdit_3.setPlainText(all_of_person1[1])

        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText('هذا الأسم غير موجود, ربما قمت بحذفه')
            msg.exec_()

    def sum_in_reduced(self):
        # get the data from the cells after editing
        new_red = self.lineEdit_207.text()
        previous_red = self.lineEdit_206.text()
        sum_red = str(int(new_red) + int(previous_red))
        self.lineEdit_208.setText(sum_red)

    # function that do the edit task
    def reduce_to_database(self):
        # get the data from the cell before updating
        n_name = self.lineEdit_192.text()
        sum_reduced = self.lineEdit_208.text()
        d_details = self.plainTextEdit_3.toPlainText()
        mn = int(self.comboBox_6.currentText())
        # put the modified data into the database
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''UPDATE reduced SET amount='{}',reason='{}' WHERE
        name='{}' and red_month={} '''.format(sum_reduced, d_details, n_name, mn))
        db.commit()
        db.close()
        # clear the cells after edit process
        self.lineEdit_203.setText("")
        self.lineEdit_192.setText("")
        self.comboBox_19.setCurrentText(self.comboBox_19.itemText(0))
        self.comboBox_18.setCurrentText(self.comboBox_18.itemText(0))
        self.comboBox_6.setCurrentText(self.comboBox_6.itemText(0))
        self.lineEdit_207.setText("")
        self.lineEdit_206.setText("")
        self.lineEdit_208.setText("")
        self.plainTextEdit_3.setPlainText("")
        # show ensure message
        self.statusBar().showMessage("تم إضافة الخصم علي {1} بنجاح في شهر {0}".format(str(mn), n_name), 5000)

        # refresh the table after adding reduced value
        self.fill_main_table()

    ######################## debt part #############################
    def auto_compelete_debt(self):
        self.names_list = []
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        names = cr.execute('''select name from workers''')
        all = names.fetchall()
        for n in all:
            self.names_list.append(n[0])
        # create Qcompeleter and add it to Widget
        completer = QCompleter()
        self.lineEdit_199.setCompleter(completer)
        # create model and add list to it
        model = QStringListModel()
        model.setStringList(self.names_list)
        # add model to compeleter
        completer.setModel(model)

    #### get reduced person from database
    def get_data_to_debt(self):
        # get user data from database
        o_name = self.lineEdit_199.text()
        mnth = self.comboBox_8.currentText()
        try:
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            workersdata = cr.execute(
                '''select name, fac_name, fac_night from workers WHERE name='{}' '''.format(o_name))
            cr1 = db.cursor()
            debtdata = cr1.execute(
                '''select total,detail from debt WHERE name='{}' and debt_month={} '''.format(o_name, mnth))
            all_of_person = workersdata.fetchone()
            all_of_person1 = debtdata.fetchone()
            db.commit()
            db.close()

            # put the in the cells
            self.lineEdit_189.setText(all_of_person[0])
            self.comboBox_15.setCurrentText(all_of_person[1])
            self.comboBox_14.setCurrentText(all_of_person[2])

            if all_of_person1 == None:
                db = sqlite3.connect('database.db')
                cr = db.cursor()
                cr.execute('''INSERT INTO debt(name, debt_month) VALUES('{}', {})'''.format(all_of_person[0], mnth))
                db.commit()
                db.close()

                self.lineEdit_204.setText(str(0))
            else:
                self.lineEdit_204.setText(all_of_person1[0])
                self.plainTextEdit.setPlainText(all_of_person1[1])

        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText('هذا الأسم غير موجود, ربما قمت بحذفه')
            msg.exec_()

    def sum_in_debt(self):
        # get the data from the cells after editing
        new_red = self.lineEdit_200.text()
        previous_red = self.lineEdit_204.text()
        sum_red = str(int(new_red) + int(previous_red))
        self.lineEdit_205.setText(sum_red)

    # function that do the edit task
    def debt_to_database(self):
        # get the data from the cell before updating
        n_name = self.lineEdit_189.text()
        sum_debt = self.lineEdit_205.text()
        d_details = self.plainTextEdit.toPlainText()

        # put the modified data into the database
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''UPDATE debt SET total='{}',detail='{}' WHERE
        name='{}' and debt_month={} '''.format(sum_debt, d_details, n_name, int(self.comboBox_8.currentText())))
        db.commit()
        db.close()

        # clear the cells after edit process
        self.lineEdit_199.setText("")
        self.lineEdit_189.setText("")
        self.comboBox_15.setCurrentText(self.comboBox_15.itemText(0))
        self.comboBox_14.setCurrentText(self.comboBox_14.itemText(0))
        self.comboBox_8.setCurrentText(self.comboBox_8.itemText(0))
        self.lineEdit_200.setText("")
        self.lineEdit_204.setText("")
        self.lineEdit_205.setText("")
        self.plainTextEdit.setPlainText("")
        # show ensure message
        self.statusBar().showMessage("تم إضافة السلفة بنجاح", 5000)

        # refresh the table after taking debt
        self.fill_main_table()

    ##########################################################################################
    ### get salary
    def get_salary(self, per_namee, moth):
        # number of days
        # get the factory names for each person
        db = sqlite3.connect('database.db')
        cr1 = db.cursor()
        cr2 = db.cursor()
        cr3 = db.cursor()
        cr4 = db.cursor()
        cr1.execute('''SELECT factName.salary FROM attendance LEFT JOIN factName 
            ON attendance.factory=factName.name WHERE attendance.name='{}' and month={} '''.format(per_namee, moth))

        cr2.execute('''SELECT total FROM debt WHERE name='{}' and debt_month={} '''.format(per_namee, moth))
        cr3.execute('''SELECT amountv FROM additional WHERE namev='{}' and add_month={} '''.format(per_namee, moth))
        cr4.execute('''SELECT amount FROM reduced WHERE name='{}' and red_month={} '''.format(per_namee, moth))

        factories_list = cr1.fetchall()
        debt_1 = cr2.fetchall()
        add_1 = cr3.fetchall()
        reduced_1 = cr4.fetchall()
        db.close()
        # full salary for person
        summ = 0
        for i in factories_list:
            summ += i[0]

        # send data to store variable of the call
        no_of_dayss = len(factories_list)
        v1 = (0 if debt_1 == [] else debt_1[0][0])
        v2 = (0 if add_1 == [] else add_1[0][0])
        v3 = (0 if reduced_1 == [] else reduced_1[0][0])
        return no_of_dayss, summ, v1, v2, v3

    ### fill main_table
    def fill_main_table(self):
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''SELECT name,phone,national,fac_name,fac_night FROM workers  ORDER BY name ASC''')
        data = cr.fetchall()
        db.commit()
        db.close()

        # month of the data on main table at start
        mon = time.localtime()[1] - 1

        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
            # get salrary and put it into table
            n_days, s_salary, d1, d2, d3 = self.get_salary(self.tableWidget.item(row_number, 0).text(), mon)
            self.tableWidget.setItem(row_number, 5, QTableWidgetItem(str(d1)))
            self.tableWidget.setItem(row_number, 6, QTableWidgetItem(str(d2)))
            self.tableWidget.setItem(row_number, 7, QTableWidgetItem(str(d3)))
            self.tableWidget.setItem(row_number, 8, QTableWidgetItem(str(n_days)))
            self.tableWidget.setItem(row_number, 9, QTableWidgetItem(str(s_salary)))

    def check_text(self):
        data = []
        if self.comboBox_16.currentIndex() == 0:
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            cr.execute('''SELECT * FROM workers WHERE name LIKE '{}%' ORDER BY name ASC'''.format(self.lineEdit.text()))
            data = cr.fetchall()
            db.commit()
            db.close()
        else:
            db = sqlite3.connect('database.db')
            cr = db.cursor()
            cr.execute(
                '''SELECT * FROM workers WHERE fac_name LIKE '{}%' ORDER BY name ASC'''.format(self.lineEdit.text()))
            data = cr.fetchall()
            db.commit()
            db.close()

        # month of the data on main table at start
        mon = time.localtime()[1] - 1

        # fill table while search
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.tableWidget.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))
            # get salrary and put it into table
            n_days, s_salary, d1, d2, d3 = self.get_salary(self.tableWidget.item(row_number, 0).text(), mon)
            self.tableWidget.setItem(row_number, 5, QTableWidgetItem(str(d1)))
            self.tableWidget.setItem(row_number, 6, QTableWidgetItem(str(d2)))
            self.tableWidget.setItem(row_number, 7, QTableWidgetItem(str(d3)))
            self.tableWidget.setItem(row_number, 8, QTableWidgetItem(str(n_days)))
            self.tableWidget.setItem(row_number, 9, QTableWidgetItem(str(s_salary)))

    def double_clickonTable(self, row, column):
        self.n = self.stackedWidget.currentIndex()  # ch4
        self.stackedWidget.setCurrentIndex(3)
        per_name = self.tableWidget.item(row, 0).text()
        self.label_2.setText(per_name)
        mon = time.localtime()[1]

        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr1 = db.cursor()
        # get data from database to tableWidget_3
        cr.execute(
            '''SELECT date,dayname,factory,shift FROM attendance WHERE name='{}' and month={}'''.format(per_name, mon))
        cr1.execute('''SELECT DISTINCT month FROM attendance WHERE name='{}' '''.format(per_name))

        cr2 = db.cursor()
        cr2.execute('''SELECT amount,reason FROM reduced WHERE name='{}' and red_month={}'''.format(per_name, mon))
        redu = cr2.fetchall()

        data = cr.fetchall()
        listed_month = cr1.fetchall()
        db.commit()
        db.close()

        # fill monthes for each person
        self.comboBox_5.clear()
        for i in listed_month:
            self.comboBox_5.addItem(str(i[0]))
        # put the current last month as current
        self.comboBox_5.setCurrentText(str(mon))

        # fill days for each person
        self.tableWidget_3.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.tableWidget_3.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.tableWidget_3.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        # fill reduced for each person page
        if bool(redu):
            self.tableWidget_3.setItem(0, 4, QTableWidgetItem(str(redu[0][0])))
            self.tableWidget_3.setItem(0, 5, QTableWidgetItem(str(redu[0][1])))

        # number of days and net_salary
        n_days, s_salary, d1, d2, d3 = self.get_salary(per_name, mon)
        self.lineEdit_3.setText(str(n_days))

        # get the net salary
        net_salary = s_salary - int(d1) + int(d2) - int(d3)
        self.lineEdit_2.setText(str(net_salary))

    def send_message(self):
        # get the month number
        manth = time.localtime()[1]-1

        # get the names and its phones from database
        db = sqlite3.connect('database.db')
        cr = db.cursor()
        cr.execute('''SELECT name,phone,national,fac_name,fac_night FROM workers''')
        fetch = cr.fetchall()
        db.commit()
        db.close()

        # loop through all names in the database
        for each in fetch:
            # the number of days and salary, ......
            n_days, s_salary, d1, d2, d3 = self.get_salary(each[0], manth)
            # the dates that this person work
            db = sqlite3.connect('database.db')
            cr1 = db.cursor()
            cr1.execute('''SELECT date,dayname FROM attendance WHERE name='{}' and month={} '''.format(each[0], manth))
            data = cr1.fetchall()
            db.commit()
            db.close()

            message = "شركة النور إدارة أ/وليد جبارة:\n" \
                      "تعلم صاحب الأسم:{0} والرقم القومي:{1} اللذي يعمل في مصنع:{2} وردية:{3}\n" \
                      "أن مرتبه:{4} وعدد أيامه:{5} والسلف:{6} والإضافي:{7} والخصومات:{8}\n" \
                      "\n:وأن الأيام اللتي ختضرتها هي كالتالي\n".format(each[0], each[2], each[3], each[4], s_salary,n_days, d1, d2, d3)

            if bool(data):
                # send the message
                for v in data:
                    days_msg = "يوم:{1} بتاريخ:{0}\n".format(v[0], v[1])
                    pywhatkit.sendwhatmsg_instantly("+20{}".format(int(each[1])), message+days_msg, 10)
                    pyautogui.press('enter')
                    time.sleep(10)
                    pyautogui.hotkey('ctrl', 'w')
                    pyautogui.press('enter')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainApp()
    window.showMaximized()
    app.exec_()
