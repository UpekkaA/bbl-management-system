import unittest

from league.util import Util


class UtilTestCase(unittest.TestCase):

    # test util method to calculate the 90th percentile for a given data array
    def test_percentile(self):
        percentile = 0
        arr = [20, 2, 7, 1, 34, 10, 22, 10, 3, 30]
        percentile = Util.get_percentile(arr, 90)
        print(percentile)
        assert percentile != 0


if __name__ == '__main__':
    unittest.main()
