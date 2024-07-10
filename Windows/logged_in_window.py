from PyQt5.QtWidgets import *
from datetime import datetime
from Models.database import Database;
from Controllers.associate_controller import *
from Models.associate import *
from PyQt5 import uic
from Windows.scale_window import ScaleUI
from Controllers.current_week_controller import *
from PyQt5 import QtWidgets
from Controllers.previous_week_controller import *
from Windows.admin_window import AdminWindow


class LoggedInWindow(QMainWindow):
    
    def __init__(self, badgeNum):
        super(LoggedInWindow, self).__init__()
        uic.loadUi("Windows/LoggedIn.ui", self)
        ScaleUI(self, 1.5)
        self.set_labels(badgeNum)
        self.clock_in_out_button.clicked.connect(lambda: self.clock_in_out(badgeNum))
        self.setup_tables()
        self.load_tables_data(badgeNum)
        self.admin_view_button.clicked.connect(lambda: self.admin_log_in(badgeNum))
        self.back_button.clicked.connect(lambda: self.back_to_log_in())
        self.show()
        
    #Set name and department labels
    def set_labels(self, badgeNum):
        database = Database('TimesRecord.db')
        associate_db = Associate(database)

        #Get all associates
        associates = associate_db.get_all_associates()

        #Find employee associated with badge number and set name and department labels
        for item in associates:
            if item[0] == badgeNum:
                self.name_label.setText(str(item[1]))
                self.department_label.setText(str(item[2]))

    #Clocks in employee associated with badgeN number
    def clock_in_out(self, badgeNum):
            current_week_controller = CurrentWeekController('TimesRecord.db')
            
            #Get current date
            date_str = datetime.now().date().isoformat() 
        
            # Get all current week entries
            all_entries = current_week_controller.get_all_entries()

            # Clock in if list is empty or if last 
            if len(all_entries) != 0:
                # Filter list to keep only employee entries associated with badge number
                current_employee_entries = [entry for entry in all_entries if entry[1] == badgeNum]

                # Checks if last entry was left empty for time out
                if current_employee_entries[-1][4] == "0000-00-00 00:00:00":
                    current_week_controller.update_entry(current_employee_entries[-1][0], current_employee_entries[-1][3], datetime.now().strftime('%H:%M:%S'), "None")
                else: 
                    # add employee entry
                    current_week_controller.add_entry(badgeNum, date_str, datetime.now().strftime('%H:%M:%S'), "0000-00-00 00:00:00", "None")
            else:
                current_week_controller.add_entry(badgeNum, date_str, datetime.now().strftime('%H:%M:%S'), "0000-00-00 00:00:00", "None")

            self.load_tables_data(badgeNum)
            
    # Set up format of tables
    def setup_tables(self):
        # Set number of columns
        self.current_week_time_table.setColumnCount(4)
        # Set horizontal labels
        self.current_week_time_table.setHorizontalHeaderLabels(['Date', "Time In", "Time Out", "Notes"])
        self.current_week_time_table.horizontalHeader().setStretchLastSection(True)

    # Load table data for current week entries
    def load_tables_data(self, badgeNum):
        current_week_controller = CurrentWeekController('TimesRecord.db')

        # Get this weeks entries
        all_entries = current_week_controller.get_all_entries()

        # Filter employees list to only include current employee and remove record number and badge number
        current_employee_entries = [entry for entry in all_entries if entry[1] == badgeNum]
        current_employee_entries = [entry[2:] for entry in current_employee_entries]
        
        # Set number of rows 
        self.current_week_time_table.setRowCount(len(current_employee_entries)) 

        # Populate table with data from current_employee_entries list
        for row_index, row_data in enumerate(current_employee_entries):
            for col_index, col_data in enumerate(row_data):
                self.current_week_time_table.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(col_data)))

    # Opens admin window
    def admin_log_in(self, badgeNum):
        self.hide()
        self.deleteLater()
        self.main_window = AdminWindow()
    
    # Opens log in window
    def back_to_log_in(self):
        from Windows.log_in_window import LogInWindow
        self.hide()
        self.deleteLater()
        self.main_window = LogInWindow()
