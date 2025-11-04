import pandas as pd
import numpy as np

class DataProvider:
    def generate_mock_data(self, num_rows: int) -> pd.DataFrame:
        # Placeholder for actual data generation logic
        data = {
            "symbol": [f"STOCK{i}" for i in range(num_rows)],
            "name": [f"Stock Name {i}" for i in range(num_rows)],
            "price": np.random.uniform(10, 1000, num_rows),
            "change": np.random.uniform(-5, 5, num_rows),
            "volume": np.random.randint(10000, 1000000, num_rows),
            "market_cap": np.random.uniform(1e9, 1e12, num_rows),
        }
        return pd.DataFrame(data)

def get_data_provider():
    return DataProvider()
