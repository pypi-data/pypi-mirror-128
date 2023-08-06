from hdsr_wis_config_reader.constants import location_sets
from hdsr_wis_config_reader.constants import paths
from hdsr_wis_config_reader.tests.fixtures import fews_config


# silence flake8
fews_config = fews_config


expected_idmap_section_name = ""
expected_name = "mswlocaties"
expected_csvfile = "msw_stations"
expected_fews_name = "MSW_STATIONS"

expected_validation_attributes = []

expected_validation_rules = []
expected_attrib_files = []

expected_csvfile_meta = {
    "file": "msw_stations",
    "geoDatum": "Rijks Driehoekstelsel",
    "id": "%LOC_ID%",
    "name": "%LOC_NAME%",
    "description": "MSW-station",
    "x": "%X%",
    "y": "%Y%",
    "relation": [
        {"relatedLocationId": "%GAFCODE%", "id": "AFVOERGEBIED"},
        {"relatedLocationId": "%GPGIDENT%", "id": "PEILGEBIED"},
        {"relatedLocationId": "%RBGID%", "id": "RBGID"},
    ],
    "attribute": {"text": "%PARS%", "id": "PARS"},
}


def test_mswlocationset(fews_config):
    mswloc = location_sets.msw.MswLocationSet(fews_config=fews_config)
    assert mswloc.fews_config.path == paths.WIS_CONFIG_TEST_DIR
    assert mswloc.idmap_section_name == expected_idmap_section_name
    assert mswloc.name == expected_name
    assert mswloc.csv_filename == expected_csvfile
    assert mswloc.fews_name == expected_fews_name
    assert mswloc.get_validation_attributes(int_pars=None) == expected_validation_attributes
    assert mswloc.validation_rules == expected_validation_rules
    assert mswloc.csv_file_meta == expected_csvfile_meta
    assert mswloc.attrib_files == expected_attrib_files
