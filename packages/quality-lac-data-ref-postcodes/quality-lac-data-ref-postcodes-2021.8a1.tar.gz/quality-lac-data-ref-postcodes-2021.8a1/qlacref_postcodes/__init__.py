import bz2

import pandas as pd
from pathlib import Path
from typing import List

columns = ['pcd', 'oseast1m', 'osnrth1m', 'laua']


class Postcodes:
    _data_dir =  Path(__file__).parent
    _df = pd.DataFrame(columns=columns)
    _read = set()

    def load_postcodes(self, letters: str):
        dataframes = [self._df]
        for letter in letters:
            letter = letter[0].upper()
            if letter in self._read:
                continue
            self._read.add(letter)
            with bz2.open(self._data_dir / f"postcodes_{letter}.json.bz2") as file:
                dataframes.append(pd.read_json(file))

        if len(dataframes) > 1:
            self._df = pd.concat(dataframes).drop_duplicates().reset_index(drop=True)
