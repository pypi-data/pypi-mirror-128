from PyQt5.QtWidgets import QWidget
from abc import ABC, abstractmethod


class ControlPanelInterface(ABC):
    """
    A base class interface for creating control panel
    """

    @abstractmethod
    def get_control_panel(self) -> QWidget:
        """
        Returns QWidget control panel
        Returns: a control panel as a QWidget class

        """
        pass


class EmptyControlPanel(ControlPanelInterface):
    """
    Examplary empty control panel
    """
    def __init__(self, data=None, widget=None):
        self.control_panel = None

    def get_control_panel(self):
        return self.control_panel


