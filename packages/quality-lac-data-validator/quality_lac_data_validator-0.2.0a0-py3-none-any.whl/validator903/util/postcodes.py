import logging
import os
from pathlib import Path

import pandas as pd
from typing import Iterable
import qlacref_postcodes

logger = logging.getLogger(__name__)

_dtypes = {
    'pcd': 'str',
    'oseast1m': 'float64',
    'osnrth1m': 'float64',
    'laua': 'str',
    'pcd_abbr': 'str',
}


class Postcodes:
    _read = set()
    _data_dir = Path(qlacref_postcodes.__file__).parent
    _df = pd.DataFrame({c: pd.Series(dtype=t) for c, t in _dtypes.items()})

    @property
    def dataframe(self):
        return self._df

    def load_postcodes(self, letters: Iterable[str]):
        if os.getenv("QLAC_DISABLE_PC"):
            return
        dataframes = [self._df]
        to_load = set([l.upper() for l in letters]) - self._read
        logger.info(f"Loading {to_load}")
        for letter in to_load:
            if letter in self._read:
                continue
            try:
                logger.debug(f"Opening {letter}")
                df = pd.read_json(self._data_dir / f"postcodes_{letter}.json.bz2", dtype=_dtypes)
                logger.debug(f"Read {df.shape[0]} postcodes from {letter}")
                dataframes.append(df)
            except (ValueError, FileNotFoundError):
                logger.debug(f"File not found for {letter}")
                pass

        if len(dataframes) > 1:
            self._df = pd.concat(dataframes).drop_duplicates().reset_index(drop=True)
            self._df['pcd_abbr'] = self._df['pcd'].str.replace(' ', '')
            self._read = self._read | to_load
