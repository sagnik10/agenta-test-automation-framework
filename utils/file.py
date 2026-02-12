import json
import pandas as pd

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def read_excel(path, sheet_name=0):
    df = pd.read_excel(path, sheet_name=sheet_name)
    return df.to_dict(orient='records')
