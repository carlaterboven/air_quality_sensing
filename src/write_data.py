import pandas as pd
import os

dirname = os.path.dirname(__file__)
DATA_FILE = os.path.join(dirname, '../data/data.csv')
ride_df = pd.read_csv(DATA_FILE)


if __name__ ==  '__main__':
    pm1 = 0
