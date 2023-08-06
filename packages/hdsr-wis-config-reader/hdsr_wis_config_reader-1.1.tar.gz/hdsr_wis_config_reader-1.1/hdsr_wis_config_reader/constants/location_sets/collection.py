from hdsr_wis_config_reader.constants import location_sets
from hdsr_wis_config_reader.fews_utilities import FewsConfig
from typing import List

import pandas as pd  # noqa pandas comes with geopandas


class LocationSetCollection:
    def __init__(self, fews_config: FewsConfig):
        self.fews_config = fews_config
        self._hoofdloc_new = None
        self._hoofdloc = None
        self._subloc = None
        self._waterstandloc = None
        self._mswloc = None
        self._psloc = None

    def all(self) -> List[location_sets.base.LocationSetBase]:
        return [self.hoofdloc, self.subloc, self.waterstandloc, self.mswloc, self.psloc]

    @property
    def hoofdloc(self) -> location_sets.hoofd.HoofdLocationSet:
        """Get HoofdLocationSet. The property .geo_df has eventually been updated."""
        if self._hoofdloc_new is not None:
            assert self._hoofdloc and isinstance(self._hoofdloc, location_sets.hoofd.HoofdLocationSet)
            assert isinstance(self._hoofdloc_new, pd.DataFrame)
            self._hoofdloc._geo_df = self._hoofdloc_new
        if self._hoofdloc is not None:
            return self._hoofdloc
        self._hoofdloc = location_sets.hoofd.HoofdLocationSet(fews_config=self.fews_config)
        return self._hoofdloc

    @property
    def subloc(self) -> location_sets.sub.SubLocationSet:
        if self._subloc is not None:
            return self._subloc
        self._subloc = location_sets.sub.SubLocationSet(fews_config=self.fews_config)
        return self._subloc

    @property
    def waterstandloc(self) -> location_sets.ow.WaterstandLocationSet:
        if self._waterstandloc is not None:
            return self._waterstandloc
        self._waterstandloc = location_sets.ow.WaterstandLocationSet(fews_config=self.fews_config)
        return self._waterstandloc

    @property
    def mswloc(self) -> location_sets.msw.MswLocationSet:
        if self._mswloc is not None:
            return self._mswloc
        self._mswloc = location_sets.msw.MswLocationSet(fews_config=self.fews_config)
        return self._mswloc

    @property
    def psloc(self) -> location_sets.ps.PeilschaalLocationSet:
        if self._psloc is not None:
            return self._psloc
        self._psloc = location_sets.ps.PeilschaalLocationSet(fews_config=self.fews_config)
        return self._psloc
