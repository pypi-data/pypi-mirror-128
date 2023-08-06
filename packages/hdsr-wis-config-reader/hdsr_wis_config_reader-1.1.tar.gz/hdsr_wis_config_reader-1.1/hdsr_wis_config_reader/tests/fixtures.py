from hdsr_wis_config_reader.constants import paths
from hdsr_wis_config_reader.constants.location_sets import LocationSetCollection
from hdsr_wis_config_reader.fews_utilities import FewsConfig

import pytest


@pytest.fixture()
def fews_config() -> FewsConfig:
    # we use config saved in this repo (=static), instead of downloading from repo 'wis_config'
    fews_config = FewsConfig(path=paths.WIS_CONFIG_TEST_DIR)
    return fews_config


@pytest.fixture
def loc_sets() -> LocationSetCollection:
    fews_config = FewsConfig(path=paths.WIS_CONFIG_TEST_DIR)
    loc_sets = LocationSetCollection(fews_config=fews_config)
    return loc_sets
