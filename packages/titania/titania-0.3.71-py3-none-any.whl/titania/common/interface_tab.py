from abc import ABC, abstractmethod

class TitaniaTabInterface(ABC):
    def __init__(self):
        """
        Interface for creating any tab in titania.
        """


    @abstractmethod
    def get_title(self) -> None:
        """
        A setter fot eh tab name

        """
        pass

    @abstractmethod
    def initiate(self) -> None:
        """
        This method initiates the tab.

        """
        pass
