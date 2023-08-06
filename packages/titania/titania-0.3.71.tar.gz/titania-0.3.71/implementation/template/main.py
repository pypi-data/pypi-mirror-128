import sys
from PyQt5.QtWidgets import QApplication

from titania.QtGUI.main_window import MainWindow
from config import config

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex = MainWindow(height=height, width=width, tab_config=config)
    ex.show()
    sys.exit(app.exec_())