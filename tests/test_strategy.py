import unittest
import pandas as pd
from src.strategy import simple_moving_average_strategy

class TestStrategy(unittest.TestCase):
    def test_simple_moving_average_strategy(self):
        # Create a sample DataFrame for testing
        data = {
            'time': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05'],
            'close': [10, 12, 15, 13, 11]
        }
        df = pd.DataFrame(data)
        
        # Apply the simple moving average strategy
        df = simple_moving_average_strategy(df)
        
        # Assert the expected values
        self.assertEqual(df['SMA20'].tolist(), [None, None, None, 12.5, 12.75])
        self.assertEqual(df['SMA50'].tolist(), [None, None, None, None, None])
        self.assertEqual(df['signal'].tolist(), [0, 0, 0, 1, 0])
        self.assertEqual(df['position'].tolist(), [0, 0, 0, 1, 0])

if __name__ == '__main__':
    unittest.main()