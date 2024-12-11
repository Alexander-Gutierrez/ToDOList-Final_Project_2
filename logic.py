from PyQt6.QtWidgets import *
from gui import *
from PyQt6.QtCore import Qt


class Logic(QMainWindow, Ui_Widget):
    def __init__(self):
        super().__init__()
        self.reminder_checkbox = None
        self.todo_button = None
        self.setupUi(self)
        self.group_boxes = {}  # Dictionary to store unique group boxes for each button

        self.button_newlist.clicked.connect(self.create_list)

    def create_list(self):
        text, ok = QInputDialog.getText(self, "Input List Name", "Enter the Name of the New List Category:")

        text = text.strip()
        if ok and text:
            self.add_new_widget(text)

    def add_new_widget(self, widget_name):
        new_button = QPushButton(widget_name, self)
        new_button.setObjectName(widget_name)
        new_button.setStyleSheet("""QPushButton { 
                                    background-color:#D35400;
                                    color: white;
                                    font-size: 15px;
                                    border-style: outset;
                                    border-width:2px;
                                    border-radius: 10px;
                                    border-color: rgb(37, 37, 37);
                                  }""")
        new_button.setFixedWidth(200)

        # Connect the button to the method that creates and toggles the group box
        new_button.clicked.connect(lambda: self.toggle_group_box(widget_name))

        # Add the new button to the List_Layout
        self.List_Layout.addWidget(new_button)
        self.List_Layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.List_Layout.setSpacing(25)
        self.List_Layout.setContentsMargins(10, 20, 10, 10)

    def toggle_group_box(self, button_name):
        # Check if the group box already exists
        if button_name not in self.group_boxes:
            # Create a new group box for the button
            group_box = QGroupBox(f"{button_name} List", self)

            group_box.setStyleSheet("""QGroupBox{ color: white; 
                                              font-size: 25px;
                                            }""")

            # Create a layout for the group box
            group_box_layout = QVBoxLayout()
            group_box.setLayout(group_box_layout)

            # Add the group box to the Box_layout
            self.Box_layout.addWidget(group_box)

            # Create a new label for the group box
            box_layout_label = QLabel('+ Double Click to Enter Reminder', self)
            box_layout_label.setStyleSheet("""QLabel{
                                                color: #707070;
                                                font-size: 15px;
                                             }""")
            box_layout_label.setAlignment(Qt.AlignmentFlag.AlignTop)
            group_box_layout.addWidget(box_layout_label)

            # Store the group box in the dictionary
            self.group_boxes[button_name] = {
                "group_box": group_box,
                "label": box_layout_label,
                "checkboxes": []  # Store checkboxes added to the group box
            }

            # Enable double-click event for adding reminders
            group_box.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
            group_box.mouseDoubleClickEvent = lambda event, button_name=button_name: self.add_reminder_on_double_click(
                event, button_name)
        else:
            # If the group box already exists, toggle it
            group_box = self.group_boxes[button_name]["group_box"]
            if group_box.isVisible():
                group_box.setVisible(False)  # Hide the group box
            else:
                group_box.setVisible(True)  # Show the group box

    def add_reminder_on_double_click(self, event, group_name):
        # Show the input dialog when double-clicking on the group box
        reminder_text, ok = QInputDialog.getText(self, "Input Reminder", "Enter the Reminder")

        if ok and reminder_text:
            self.add_checkbox_to_group(group_name, reminder_text)

    def add_checkbox_to_group(self, group_name, reminder_text):
        # Add a checkbox to the specified group (if the group exists)
        if group_name not in self.group_boxes:
            return  # Group box doesn't exist

        group_box = self.group_boxes[group_name]["group_box"]
        group_box_layout = group_box.layout()

        # Create a new checkbox for the reminder
        check_box = QCheckBox(f"{reminder_text}", self)
        check_box.setStyleSheet("""QCheckBox { 
                                    color: white; 
                                    font-size: 15px; 
                                  }""")

        # Add the checkbox to the layout of the group box
        group_box_layout.addWidget(check_box)
        group_box_layout.setSpacing(10)  # Set the space between checkboxes
        group_box_layout.setAlignment(check_box, Qt.AlignmentFlag.AlignTop)

        # Save the checkbox to avoid adding it again
        self.group_boxes[group_name]["checkboxes"].append(check_box)


