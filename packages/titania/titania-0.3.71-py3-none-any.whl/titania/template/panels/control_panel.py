from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QLabel, QComboBox, QPushButton, QTextEdit, QWidget, QCheckBox, QRadioButton

from titania.panels import ControlPanelInterface


class ControlPanel(ControlPanelInterface):
    def __init__(self, data=None, widget=None):
        self.control_panel = QGridLayout()
        self.data_buttons_group = QGridLayout()

        self.sensor_id_label = QLabel("Sensor ID:")
        self.sensor_id_combo_box = QComboBox()
        self.sensor_id_combo_box.addItem("1")
        self.sensor_id_combo_box.addItem("2")
        self.sensor_id_combo_box.addItem("3")

        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.prev_four_button = QPushButton("Prev Four")
        self.next_four_button = QPushButton("Next Four")

        self.data_buttons_group.addWidget(self.sensor_id_label, 1, 0, alignment=QtCore.Qt.AlignRight)
        self.data_buttons_group.addWidget(self.sensor_id_combo_box, 1, 1)
        self.data_buttons_group.addWidget(self.previous_button, 2, 0)
        self.data_buttons_group.addWidget(self.next_button, 2, 1)
        self.data_buttons_group.addWidget(self.prev_four_button, 3, 0)
        self.data_buttons_group.addWidget(self.next_four_button, 3, 1)

        self.notification_label = QLabel("Notifications:")
        self.notification_text_box = QTextEdit()
        self.notification_text_box.setMaximumSize(400, 600)
        self.notification_text_box.setText("TEST NOTIFICATION")

        self.split_line = QWidget()
        self.split_line.setStyleSheet("background-color:black;")
        self.split_line.setMinimumSize(400, 2)
        self.split_line.setMaximumSize(400, 2)

        self.display_references_button = QCheckBox("Display references")
        self.overlay_button = QRadioButton("Overlay")
        self.data_ref_button = QRadioButton("data - Ref")
        self.data_slash__button = QRadioButton("data/Ref")

        self.split_line2 = QWidget()
        self.split_line2.setStyleSheet("background-color:black;")
        self.split_line2.setMinimumSize(400, 2)
        self.split_line2.setMaximumSize(400, 2)

        self.run_number_label = QLabel("Run number:")

        self.run_number_combo_box = QComboBox()
        self.run_number_combo_box.addItem("12345")
        self.run_number_combo_box.addItem("54321")

        self.reference_number_label = QLabel("Reference number:")

        self.reference_number_combo_box = QComboBox()
        self.reference_number_combo_box.addItem("Auto")
        self.reference_number_combo_box.addItem("12345")
        self.reference_number_combo_box.addItem("54321")

        self.control_panel.addLayout(self.data_buttons_group, 0, 0)
        self.control_panel.addWidget(self.notification_label, 4, 0)
        self.control_panel.addWidget(self.notification_text_box, 5, 0)
        self.control_panel.addWidget(self.split_line, 6, 0)
        self.control_panel.addWidget(self.display_references_button, 7, 0)
        self.control_panel.addWidget(self.overlay_button, 8, 0)
        self.control_panel.addWidget(self.data_ref_button, 9, 0)
        self.control_panel.addWidget(self.data_slash__button, 10, 0)
        self.control_panel.addWidget(self.split_line2, 11, 0)
        self.control_panel.addWidget(self.run_number_label, 12, 0)
        self.control_panel.addWidget(self.run_number_combo_box, 13, 0)
        self.control_panel.addWidget(self.reference_number_label, 14, 0)
        self.control_panel.addWidget(self.reference_number_combo_box, 15, 0)

    def get_control_panel(self):
        return self.control_panel