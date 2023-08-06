import bz2
from typing import Iterable

import pandas as pd
from pathlib import Path

columns = ['pcd', 'oseast1m', 'osnrth1m', 'laua']


class Postcodes:
    _data_dir =  Path(__file__).parent
    _df = pd.DataFrame(columns=columns)
    _read = set()

    @property
    def dataframe(self):
        return self._df

    def load_postcodes(self, letters: Iterable[str]):
        dataframes = [self._df]
        for letter in letters:
            letter = letter[0].upper()
            if letter in self._read:
                continue
            self._read.add(letter)
            try:
                with bz2.open(self._data_dir / f"postcodes_{letter}.json.bz2") as file:
                    dataframes.append(pd.read_json(file))
            except FileNotFoundError:
                pass

        if len(dataframes) > 1:
            self._df = pd.concat(dataframes).drop_duplicates().reset_index(drop=True)
