import numpy as np


class Util:

    # Util method to calculate the 90th percentile for a given data array
    # input: data: array, percentile: Eg:90, 50
    @staticmethod
    def get_percentile(data, percentile):
        return np.percentile(data, percentile)
