import json
from pathlib import Path

class TestDataManager:
    _data = None

    @classmethod
    def load_data(cls):
        if cls._data is None:
            data_path = Path("config/testdata.json")
            with open(data_path) as f:
                cls._data = json.load(f)
        return cls._data

    @classmethod
    def get(cls, *keys):
        data = cls.load_data()
        for key in keys:
            data = data.get(key)
        return data
