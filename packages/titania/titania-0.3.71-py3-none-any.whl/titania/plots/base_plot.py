from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QWidget
from titania.common.interface_tab import TitaniaTabInterface


class PlotInterface(ABC):
    """
    Basic plotting interface for titania
    """

    @abstractmethod
    def get_as_plot_widget(self) -> QWidget :
        """
        If the plot is a more complex QWidget, it should return that widget

        """
        pass

    def pre_draw(self):
        """
        Actions to be done before drawing the plot

        """
        pass

    @abstractmethod
    def draw_plot(self) :
        """
        Draws the plot

        """
        pass


class FinalMetaPlot(type(PlotInterface), type(FigureCanvas)):
    pass


class BaseCanvasPlot(PlotInterface, FigureCanvas, metaclass=FinalMetaPlot):
    def __init__(self, parent : QWidget = None, view : TitaniaTabInterface =None):
        """
        Implements qt canvas with matplotlib
        """
        plt.rcParams.update({'figure.max_open_warning': 0})
        self.parent = parent
        self.plot_number = 111
        self.figure = plt.figure()
        self.view = view
        FigureCanvas.__init__(self, self.figure)

    def get_as_plot_widget(self):
        return self


class MplPlot(BaseCanvasPlot):
    """
    A parent class for making matplotlib plots
    """
    def get_as_plot_widget(self, row=0):
        return self

    def pre_draw(self):
        self.figure.clear()


class NavToolbarPlot(MplPlot):
    """
    A class with a toolbar plot. The toolbar implements matplotlib toolbar with zoom,
     save file and others.
    """

    def get_as_plot_widget(self, row=10):
        self.toolbar = NavigationToolbar(self, self.view)
        self.view.plot_panel_grid.addWidget(self.toolbar, row, 1)
        return self

    def draw_plot(self):
        ax = self.figure.add_subplot(self.plot_number)
        ax.plot(self.view.data.fetch(), '*-')
        self.draw()
