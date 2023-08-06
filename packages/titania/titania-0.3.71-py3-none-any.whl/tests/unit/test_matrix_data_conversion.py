import unittest
import sys
sys.path.append("../implementation/example/")

from data.matrix_data import MatrixData


class MatrixDataConvertionTest(unittest.TestCase):

    def test_produced_matrix(self):
        matrix_data = MatrixData()

        self.assertEqual(256, len(matrix_data.data[0]))
        self.assertEqual(256, len(matrix_data.data[0][0]))

