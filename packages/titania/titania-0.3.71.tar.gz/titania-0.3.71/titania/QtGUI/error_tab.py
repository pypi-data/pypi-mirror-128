
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel
from titania.QtGUI.base_tab import QtTabInterface

class ErrorQtTab(QtTabInterface):

    def __init__(self,  message: str, title: str, parent=None):
        """
        A tab that is used to display error in place of any tab that fails to be created.

        """
        QtTabInterface.__init__(self, parent)
        self.title = title
        print(self.title)
        self.parent = parent
        self.line_layout = QVBoxLayout()
        label = QLabel(message)
        self.line_layout.addWidget(label)

    def initiate(self):
        self.setLayout(self.line_layout)

    def get_title(self):
        return self.title
