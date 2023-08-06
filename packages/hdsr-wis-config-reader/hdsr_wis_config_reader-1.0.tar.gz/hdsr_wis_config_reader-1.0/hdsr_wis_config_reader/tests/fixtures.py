from hdsr_wis_config_reader.constants import location_sets
from hdsr_wis_config_reader.constants import paths
from hdsr_wis_config_reader.fews_utilities import FewsConfig

import pytest


@pytest.fixture()
def fews_config():
    # we use config saved in this repo (=static), instead of downloading from repo 'wis_config'
    fews_config = FewsConfig(path=paths.WIS_CONFIG_TEST_DIR)
    return fews_config


@pytest.fixture
def locsets(fews_config):
    hoofdloc = location_sets.hoofd.HoofdLocationSet(fews_config=fews_config)
    subloc = location_sets.sub.SubLocationSet(fews_config=fews_config)
    wsloc = location_sets.ow.WaterstandLocationSet(fews_config=fews_config)
    mswloc = location_sets.msw.MswLocationSet(fews_config=fews_config)
    psloc = location_sets.ps.PeilschaalLocationSet(fews_config=fews_config)
    return hoofdloc, subloc, wsloc, mswloc, psloc
