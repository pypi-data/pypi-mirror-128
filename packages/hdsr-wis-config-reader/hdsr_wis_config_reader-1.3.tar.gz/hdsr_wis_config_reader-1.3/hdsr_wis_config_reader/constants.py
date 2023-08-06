from pathlib import Path


# Handy constant for building relative paths
BASE_DIR = Path(__file__).parent.parent
assert (
    BASE_DIR.name == "hdsr_wis_config_reader"
), f"BASE_DIR must be project name 'hdsr_wis_config_reader' but is {BASE_DIR.name}"

WIS_CONFIG_TEST_DIR = BASE_DIR / "hdsr_wis_config_reader" / "tests" / "data" / "input" / "config_wis60prd_202002"
