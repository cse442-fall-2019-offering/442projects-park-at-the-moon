import unittest
import count_spots as cs
import math

class TestStringMethods(unittest.TestCase):

    df = cs.countSpots()
    lotNames = list(df["Parking Lots"])

    def test_noNaN(self):
        for i in range(0, len(self.lotNames)):
            self.assertFalse(math.isnan(self.df.at[i, "Total Max Spots"]))

    def test_positiveInteger(self):
        for i in range(0, len(self.lotNames)):
            self.assertTrue(self.df.at[i, "Total Max Spots"] > 0)

if __name__ == '__main__':
    unittest.main()