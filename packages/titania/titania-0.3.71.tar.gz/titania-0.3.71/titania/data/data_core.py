from abc import ABC, abstractmethod


class TitaniaDataInterface(ABC):
    """
    This is an abstract class that interfaces all data classes.
    It requires only the difinition of  :func:`~TitaniaDataInterface.fetch`,
    which can return any kind of data.
    """

    @abstractmethod
    def fetch(self) -> object:
        """
        Returns data of any kind
        """
        pass


class EmptyTitaniaData(TitaniaDataInterface):

    def fetch(self):
        """

        Returns: empty list

        """
        return []