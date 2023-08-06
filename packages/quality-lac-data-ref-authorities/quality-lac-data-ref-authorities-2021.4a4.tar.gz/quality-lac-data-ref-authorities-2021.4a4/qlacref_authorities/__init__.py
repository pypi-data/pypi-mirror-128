import sys
from pathlib import Path


class __Authorities:
    @property
    def dataframe(self):
        import pandas as pd
        return pd.read_parquet((Path(__file__).parent / "df.parquet"))

    @property
    def records(self):
        import json
        with open(Path(__file__).parent / "records.json", 'rt') as jsonfile:
            return json.load(jsonfile)

sys.modules[__name__] = __Authorities()
