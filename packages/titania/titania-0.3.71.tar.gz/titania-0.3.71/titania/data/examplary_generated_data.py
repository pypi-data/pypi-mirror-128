import random
from typing import List
from titania.data.data_core import TitaniaDataInterface


class RandomNList(TitaniaDataInterface):
    def __init__(self, n: int = 10):
        """
        This creates random list
        Args:
            n: length of generated list
        """
        self.n = n

    def fetch(self) -> List[float]:
        """

        Returns: a random list of length n

        """
        return [random.random() for _ in range(self.n)]
