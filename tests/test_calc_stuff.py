import unittest

import numpy as np
import pandas as pd

from calc_stuff import calc_accel


class TestCalcStuff(unittest.TestCase):
    def test_calc_accel(self):
        df = pd.DataFrame(
            [[1, 1], [5, 9], [7, 15]], columns=["seconds_since_startup", "velocity"]
        )
        expected = pd.Series([np.nan, 2.0, 3.0])
        result = calc_accel(df["velocity"], df["seconds_since_startup"])
        pd.testing.assert_series_equal(result, expected)
