import sys
import pandas as pd
import os
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QListWidget, QComboBox, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate
class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the window
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 400, 400)

        # Expense data storage
        self.expenses = []
        self.file_name = "trans.csv"

        # Initialize UI components
        self.initUI()
        self.apply_theme()

    def log_transaction(self,file_name,transaction_data,headers):

        file_exits = os.path.exists(file_name)

        with open(file_name,mode='a',newline='',encoding='utf-8') as file:
            writer = csv.DictWriter(file,fieldnames=headers)
            if not file_exits:
                writer.writeheader()

            writer.writerow(transaction_data)


    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()

        # Labels and fields for input
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit(self)
        self.category_label = QLabel("Category:")
        self.category_input = QComboBox(self)
        self.category_input.addItems(["Food", "Transport", "Entertainment", "Utilities", "Others"])

        self.date_label = QLabel("Date:")
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)  # Enable calendar popup
        self.date_input.setDate(QDate.currentDate())

        # Buttons
        self.add_button = QPushButton("Add Expense", self)
        self.view_button = QPushButton("View Expenses", self)
        self.summary_button = QPushButton("Summary", self)
        self.generate_reports_button = QPushButton("Generate Reports",self)

        # Expense List Display
        self.expense_list = QListWidget(self)

        # Add widgets to the input layout
        input_layout.addWidget(self.amount_label)
        input_layout.addWidget(self.amount_input)
        input_layout.addWidget(self.category_label)
        input_layout.addWidget(self.category_input)
        input_layout.addWidget(self.date_label)
        input_layout.addWidget(self.date_input)
        input_layout.addWidget(self.add_button)

        # Add widgets to the main layout
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.view_button)
        main_layout.addWidget(self.summary_button)
        main_layout.addWidget(self.expense_list)
        main_layout.addWidget(self.generate_reports_button)

        # Set the layout for the main window
        self.setLayout(main_layout)

        # Connect buttons to their functions
        self.add_button.clicked.connect(self.add_expense)
        self.view_button.clicked.connect(self.view_expenses)
        self.summary_button.clicked.connect(self.view_summary)

    def add_expense(self):
        # Get the input values
        amount_text = self.amount_input.text()
        category = self.category_input.currentText()
        date = self.date_input.date().toString("yyyy-MM-dd")

        try:
            amount = float(amount_text)
            headers = ["Date", "Amount", "Category"]
            transaction = {"Date": date,"Amount": amount,"Category": category}

            self.log_transaction(self.file_name,transaction_data=transaction,headers=headers)
            
            #self.expenses.append({"amount": amount, "category": category, "date": date})
            QMessageBox.information(self, "Success", f"Added expense: {amount} for {category}")
            self.amount_input.clear()  # Clear the input field
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid amount!")

    def view_expenses(self):

        self.expense_list.clear()  # Clear the list before displaying
        path_exists = os.path.exists(self.file_name)


        #if not self.expenses:
        if not path_exists:
            QMessageBox.warning(self, "No Data", "No expenses added yet!")
            return
        with open(self.file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Iterate through rows
            for row in reader:
                print(row)  # Each row is a dictionary
                expense_text = f"{row['Date']} - {row['Category']}: {float(row['Amount']):.2f}"
                self.expense_list.addItem(expense_text)

        #for i, expense in enumerate(self.expenses, start=1):
        #    expense_text = f"{i}. {expense['date']} - {expense['category']}: {expense['amount']:.2f}"
        #    self.expense_list.addItem(expense_text)

    def view_summary(self):
        if not self.expenses:
            QMessageBox.warning(self, "No Data", "No expenses to summarize!")
            return

        summary = {}
        for expense in self.expenses:
            category = expense["category"]
            summary[category] = summary.get(category, 0) + expense["amount"]

        summary_text = "\n".join([f"{category}: ${total:.2f}" for category, total in summary.items()])
        QMessageBox.information(self, "Summary by Category", summary_text)

    def apply_theme(self):
        """Apply a monochromatic theme (shades of blue)"""
        theme_stylesheet = """
            QWidget {
                background-color: #E3F2FD; /* Lightest blue background */
                color: #0D47A1; /* Dark blue text */
            }
            QLabel {
                font-weight: bold;
                color: #1565C0; /* Medium blue for labels */
            }
            QLineEdit, QComboBox, QDateEdit {
                background-color: #BBDEFB; /* Lighter blue input fields */
                border: 1px solid #64B5F6; /* Medium blue border */
                color: #0D47A1; /* Dark blue text */
            }
            QPushButton {
                background-color: #2196F3; /* Primary blue button */
                border: none;
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2; /* Darker blue on hover */
            }
            QListWidget {
                background-color: #E3F2FD; /* Light blue list background */
                border: 1px solid #64B5F6; /* Medium blue border */
                color: #0D47A1; /* Dark blue text */
            }
            QMessageBox {
                background-color: #E3F2FD; /* Match message box with theme */
            }
        """
        self.setStyleSheet(theme_stylesheet)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tracker = ExpenseTracker()
    tracker.show()
    sys.exit(app.exec_())
