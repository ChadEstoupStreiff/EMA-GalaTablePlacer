
import pandas as pd

def process_excel(file):
    return pd.read_excel(file, index_col=0) 