import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QFormLayout,
    QCheckBox,
)

from data import TemplateData
from tex_helper import find_main

# Define constants for the placeholder text
TITLE_HINT = "Enter the document title"
FILE_NAME_HINT = "Enter the file name"
AUTHOR_HINT = "Enter author names (comma-separated)"
LEFT_FOOTER_HINT = "Left Footer"
CENTER_FOOTER_HINT = "Center Footer"
RIGHT_FOOTER_HINT = "Right Footer"
PROM_VALUE_HINT = "Promotion"
SCHOOL_VALUE_HINT = "School name"

DEFAULT_PROM_VALUE = "SEC25"  # Default input for Prom
DEFAULT_CENTER_FOOTER_VALUE = "\\\\thepage"  # Default input for Prom
DEFAULT_SCHOOL_VALUE = "ECN"  # Default input for School

reload: bool = False

class MainWindow(QWidget):
    ui_data = TemplateData()

    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("File Information")

        # Create the main layout
        main_layout = QVBoxLayout()

        # Create a QLabel that looks like a table with HTML formatting
        table_label = QLabel()
        table_label.setText(
            """
            <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%;">
                <tr>
                    <th>Key</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>\\\\thepage</td>
                    <td>Display the current page</td>
                </tr>
                <tr>
                    <td>,</td>
                    <td>Use the comma separator to update author names automatically in the footer<br><b>Note:</b>only available when creating a new project</br></td>
            </table>
        """
        )
        table_label.setTextFormat(Qt.RichText)  # Use rich text (HTML)
        table_label.setAlignment(Qt.AlignTop)  # Align the table at the top
        table_label.setFixedHeight(100)  # Set a fixed height for the table-like text

        # Add the table-like QLabel to the main layout
        main_layout.addWidget(table_label)

        # Create a form layout to hold file info fields
        form_layout = QFormLayout()

        # Title input (replaces file path)
        self.title_input = QLineEdit()
        self.title_input.setText(self.ui_data.title)
        self.title_input.setPlaceholderText(TITLE_HINT)
        form_layout.addRow(QLabel("Title:"), self.title_input)

        # File name input
        self.file_name_input = QLineEdit()
        self.file_name_input.setText(self.ui_data.fname)
        self.file_name_input.setPlaceholderText(FILE_NAME_HINT)
        form_layout.addRow(QLabel("File Name:"), self.file_name_input)

        # Author name input
        self.author_name_input = QLineEdit()
        self.author_name_input.setText(self.ui_data.authors)
        self.author_name_input.setPlaceholderText(AUTHOR_HINT)
        form_layout.addRow(QLabel("Author Name:"), self.author_name_input)

        # Add the form layout to the main layout
        main_layout.addLayout(form_layout)

        if not reload:
            # Row for Subject, Prom, and School
            info_layout = QHBoxLayout()

            self.subject_input = QLineEdit()
            self.subject_input.setPlaceholderText("Enter Subject")

            self.prom_input = QLineEdit()
            self.prom_input.setPlaceholderText(PROM_VALUE_HINT)
            self.prom_input.setText(DEFAULT_PROM_VALUE)  # Set default Prom value

            self.school_input = QLineEdit()
            self.school_input.setPlaceholderText(SCHOOL_VALUE_HINT)
            self.school_input.setText(DEFAULT_SCHOOL_VALUE)  # Set default School value

            # Add these to the row
            info_layout.addWidget(QLabel("Subject:"))
            info_layout.addWidget(self.subject_input)
            info_layout.addWidget(QLabel("Prom:"))
            info_layout.addWidget(self.prom_input)
            info_layout.addWidget(QLabel("School:"))
            info_layout.addWidget(self.school_input)

            # Add the info row to the main layout (above footers)
            main_layout.addLayout(info_layout)

        # Footer layout (left, center, right)
        footer_layout = QHBoxLayout()

        self.left_footer_input = QLineEdit()
        self.left_footer_input.setText(self.ui_data.l_footer)
        self.left_footer_input.setPlaceholderText(LEFT_FOOTER_HINT)

        self.center_footer_input = QLineEdit()
        if not reload:
            self.center_footer_input.setText(DEFAULT_CENTER_FOOTER_VALUE)
        else:
            self.center_footer_input.setText(self.ui_data.c_footer)
        self.center_footer_input.setPlaceholderText(CENTER_FOOTER_HINT)

        self.right_footer_input = QLineEdit()
        self.right_footer_input.setText(self.ui_data.r_footer)
        self.right_footer_input.setPlaceholderText(RIGHT_FOOTER_HINT)

        footer_layout.addWidget(self.left_footer_input)
        footer_layout.addWidget(self.center_footer_input)
        footer_layout.addWidget(self.right_footer_input)

        # Add the footer layout to the main layout
        main_layout.addLayout(footer_layout)

        if not reload:
            # Radio buttons to choose where authors' names should go (Left Footer only)
            footer_selection_layout = QHBoxLayout()
            self.footer_checkbox = QCheckBox("Store authors in left footer")
            self.footer_checkbox_automatic = QCheckBox("Automatically update footers")

            self.footer_checkbox.setChecked(True)  # Default is the left footer
            self.footer_checkbox_automatic.setChecked(True)
            self.footer_checkbox.clicked.connect(self.update_footers)

            # Add radio button to the layout
            footer_selection_layout.addWidget(self.footer_checkbox)
            footer_selection_layout.addWidget(self.footer_checkbox_automatic)

            # Add the footer selection layout to the main layout
            main_layout.addLayout(footer_selection_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Create Cancel and Save buttons
        cancel_button = QPushButton("Cancel")
        save_button = QPushButton("Save")

        # Style buttons with colors
        cancel_button.setStyleSheet("background-color: red; color: white;")
        save_button.setStyleSheet("background-color: green; color: white;")

        # Add buttons to the buttons layout
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)

        # Add the buttons layout to the main layout
        main_layout.addLayout(buttons_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        # Connect buttons to actions
        cancel_button.clicked.connect(self.cancel_action)
        save_button.clicked.connect(self.save_action)

        if not reload:
            # Dynamic update of footer
            self.prom_input.textEdited.connect(self.update_footers)
            self.school_input.textEdited.connect(self.update_footers)
            self.subject_input.textEdited.connect(self.update_footers)
            self.author_name_input.textEdited.connect(self.update_footers)

        # Set the save button as default (triggers with Enter key)
        save_button.setDefault(True)

    def cancel_action(self):
        QApplication.quit()
        sys.exit(-1)

    def save_action(self):
        self.ui_data.fname = self.file_name_input.text()
        self.ui_data.title = self.title_input.text()
        self.ui_data.authors = self.author_name_input.text()
        self.ui_data.l_footer = self.left_footer_input.text()
        self.ui_data.c_footer = self.center_footer_input.text()
        self.ui_data.r_footer = self.right_footer_input.text()

        QApplication.quit()

    def update_footers(self):
        if self.footer_checkbox_automatic.isChecked():
            # Split the author names by commas and join them with '\\'
            authors_list = self.author_name_input.text().split(",")
            formatted_authors = "\\\\".join(
                author.strip() for author in authors_list if author.strip()
            )  # Ensure no empty spaces or namesr

            formatted_school_prom_footer = f"{self.school_input.text()} - {self.prom_input.text()}\\\\{self.subject_input.text()}"

            if self.footer_checkbox.isChecked():
                self.left_footer_input.setText(formatted_authors)
                self.right_footer_input.setText(formatted_school_prom_footer)
            else:
                self.right_footer_input.setText(formatted_authors)
                self.left_footer_input.setText(formatted_school_prom_footer)


def launch_ui(update: bool) -> TemplateData:
    """
    Launch user UI that enable template edition
    """
    global reload
    ui_data = TemplateData()
    if update:
        ui_data.fname = os.path.basename(find_main(os.getcwd()))
        reload = True

    # Create and display the main window
    app = QApplication([])
    window = MainWindow()
    window.show()
    return app.exec()
