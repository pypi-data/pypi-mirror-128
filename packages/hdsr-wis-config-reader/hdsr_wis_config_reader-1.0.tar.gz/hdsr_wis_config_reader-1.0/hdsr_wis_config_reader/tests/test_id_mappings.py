from hdsr_wis_config_reader.constants.idmappings.collection import IdMappingCollection
from hdsr_wis_config_reader.tests.fixtures import fews_config
from hdsr_wis_config_reader.utils import is_equal_dataframes

import pandas as pd  # noqa pandas comes with geopandas


# silence flake8
fews_config = fews_config


expected_df_a = pd.DataFrame(
    data={
        "externalLocation": {2880: "610", 5929: "7610"},
        "externalParameter": {2880: "Q1", 5929: "Q1"},
        "internalLocation": {2880: "KW761001", 5929: "KW761001"},
        "internalParameter": {2880: "Q.G.0", 5929: "Q.G.0"},
        "source": {2880: "IdOPVLWATER", 5929: "IdOPVLWATER"},
        "histtag": {2880: "610_Q1", 5929: "7610_Q1"},
    }
)

expected_df_b = pd.DataFrame(
    data={
        "externalLocation": {2880: "610", 5929: "7610", 2252: "610"},
        "externalParameter": {2880: "Q1", 5929: "Q1", 2252: "Q1"},
        "internalLocation": {2880: "KW761001", 5929: "KW761001", 2252: "KW761001"},
        "internalParameter": {2880: "Q.G.0", 5929: "Q.G.0", 2252: "Q.G.0"},
        "source": {2880: "IdOPVLWATER", 5929: "IdOPVLWATER", 2252: "IdOPVLWATER_HYMOS"},
        "histtag": {2880: "610_Q1", 5929: "7610_Q1", 2252: "610_Q1"},
    }
)


def test_idmapping_opvl_water(fews_config):
    id_mappings = IdMappingCollection(fews_config=fews_config)
    assert id_mappings.idmap_opvl_water.shape == (6050, 6)

    df_idmap_opvl_water = id_mappings.idmap_opvl_water.get_filtered_df(int_loc="KW761001")
    assert isinstance(df_idmap_opvl_water, pd.DataFrame)
    assert len(df_idmap_opvl_water) == 2
    assert is_equal_dataframes(expected_df=expected_df_a, test_df=df_idmap_opvl_water)

    df_all = id_mappings.idmap_all.get_filtered_df(int_loc="KW761001")
    assert isinstance(df_all, pd.DataFrame)
    assert len(df_all) == 3
    assert is_equal_dataframes(expected_df=expected_df_b, test_df=df_all)
