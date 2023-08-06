import os
import sys
from os import path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QTabWidget, QGridLayout, QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5 import QtCore
import PyQt5
import traceback
from titania.QtGUI.error_tab import ErrorQtTab

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MainWindow(QWidget):
    def __init__(self, height=None, width=None, tab_config=None):
        super().__init__()
        self.height = height
        self.width = width
        self.init_ui()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../resources/main_window.css')
        file = open(filename)
        self.setStyleSheet(file.read())
        file.close()
        self.top_tab = QTabWidget(self)
        self.widgets = tab_config
        self.set_widgets()
        grid_layout.addWidget(self.top_tab, 0, 1, 1, 3)

    def set_widgets(self):
        for widget in self.widgets:
            self.top_tab.addTab(WidgetCreator(widget, parent=self, config=self.widgets),
                                widget)

    def init_ui(self):
        if self.width is not None and self.height is not None:
            self.resize(self.width - 100, self.height - 100)

        self.center()
        self.setWindowTitle('Titania')
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../resources/cern.gif')

        self.setWindowIcon(QIcon(filename))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return path.join(sys._MEIPASS, relative_path)
        return path.join(path.abspath(""), relative_path)

class TitaniaErrorDialog(QDialog):
    def __init__(self, tab_name, exception):
        super().__init__()

        self.setWindowTitle("Error!")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message_txt = """
        During the creation of the =={}== tab the following error occured:
        \n
        {}
        """.format(tab_name, exception)
        message = QLabel(message_txt)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class WidgetCreator(QWidget):
    def __init__(self, parent_tab=None, parent=None, config=None):
        super().__init__()
        self.parent = parent
        self.parent_tab = parent_tab
        self.config = config
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.child_tab = QTabWidget(self)
        self.set_tab()
        self.grid_layout.addWidget(self.child_tab, 0, 1)
        self.setLayout(self.grid_layout)

    def set_tab(self):
        for widget in self.config[self.parent_tab]:
            try:
                widget_object = widget(self)
                self.child_tab.addTab(widget_object, widget_object.title)
                widget_object.initiate()
            except Exception as e:
                print()
                print(type(widget))
                print("Creation of tab of type {} has failed:.\n".format(widget))
                print("===========Exception:===========")
                error_message = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
                print(error_message)
                if os.environ.get("QT_QPA_PLATFORM") != "offscreen":
                    dlg = TitaniaErrorDialog(widget, error_message)
                    dlg.exec()
                error_widget_object = ErrorQtTab(error_message, widget.__name__)
                self.child_tab.addTab(error_widget_object, error_widget_object.get_title())
                error_widget_object.initiate()
