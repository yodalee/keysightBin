import unittest
import numpy as np
import importAgilentBin

class TestImportFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_10point(self):
        """test example 1 of agilent doc
        """
        time, data = importAgilentBin.readfile("testcase/points10.bin")
        timeAns = 1.0e-9 * np.array([
            -0.0828,
            -0.0578,
            -0.0328,
            -0.0078,
            0.0172,
            0.0422,
            0.0672,
            0.0922,
            0.1172,
            0.1422])

        dataAns = np.array([
            -0.0525,
            -0.0511,
            -0.0490,
            -0.0370,
            -0.0103,
            0.0179,
            0.0332,
            0.0374,
            0.0380,
            0.0368])

        self.assertIsNotNone(time, "time should not be None")
        self.assertIsNotNone(data, "data should not be None")
        self.assertAlmostEqual(time, timeAns)
        self.assertAlmostEqual(data, dataAns)

if __name__ == '__main__':
    unittest.main()
