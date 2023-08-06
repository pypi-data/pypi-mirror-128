from collections import defaultdict
from lxml import etree as ET  # noqa
from pathlib import Path
from shapely.geometry import Point  # noqa shapely comes with geopandas
from typing import Dict
from typing import Optional
from typing import Union

import geopandas as gpd
import logging
import os


logger = logging.getLogger(__name__)


def elements_equal(e1, e2):
    if e1.tag != e2.tag:
        return False
    if e1.text != e2.text:
        return False
    if e1.tail != e2.tail:
        return False
    if e1.attrib != e2.attrib:
        return False
    if len(e1) != len(e2):
        return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))


def xml_to_etree(xml_filepath: Path) -> ET._Element:
    """parses an xml-file to an etree. ETree can be used in function etree_to_dict"""
    assert isinstance(xml_filepath, Path), f"path {xml_filepath} must be a pathlib.Path"
    etree = ET.parse(source=xml_filepath.as_posix()).getroot()
    return etree


def etree_to_dict(etree: Union[ET._Element, ET._Comment], section_start: str = None, section_end: str = None,) -> Dict:
    """converts an etree to a dictionary"""
    assert isinstance(etree, ET._Comment) or isinstance(
        etree, ET._Element
    ), "etree must be either be a ET._Comment or ET._Element"
    if isinstance(etree, ET._Comment):
        return {}
    _dict = {etree.tag.rpartition("}")[-1]: {} if etree.attrib else None}
    children = list(etree)

    # get a section only
    if section_start or section_end:
        if section_start:
            start = [
                idx
                for idx, child in enumerate(children)
                if isinstance(child, ET._Comment)
                if ET.tostring(child).decode("utf-8").strip() == section_start
            ][0]
        else:
            start = 0
        if section_end:
            end = [
                idx
                for idx, child in enumerate(children)
                if isinstance(child, ET._Comment)
                if ET.tostring(child).decode("utf-8").strip() == section_end
            ][0]
            if start < end:
                children = children[start:end]
        else:
            children = children[start:]

    children = [child for child in children if not isinstance(child, ET._Comment)]

    if children:
        dd = defaultdict(list)
        # for dc in map(etree_to_dict, children):
        for dc in [etree_to_dict(etree=child) for child in children]:
            for k, v in dc.items():
                dd[k].append(v)

        _dict = {etree.tag.rpartition("}")[-1]: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if etree.attrib:
        _dict[etree.tag.rpartition("}")[-1]].update((k, v) for k, v in etree.attrib.items())
    if etree.text:
        text = etree.text.strip()
        if children or etree.attrib:
            if text:
                _dict[etree.tag.rpartition("}")[-1]]["#text"] = text
        else:
            _dict[etree.tag.rpartition("}")[-1]] = text
    return _dict


def xml_to_dict(xml_filepath: Path, section_start: str = None, section_end: str = None) -> Dict:
    """converts an xml-file to a dictionary"""
    etree = xml_to_etree(xml_filepath=xml_filepath)
    _dict = etree_to_dict(etree=etree, section_start=section_start, section_end=section_end)
    return _dict


class FewsConfig:

    geo_datum = {"Rijks Driehoekstelsel": "epsg:28992"}
    Z_NODATA_VALUE = -9999.0

    def __init__(self, path: Path):
        self.path = path
        self._location_sets = None

        # FEWS config dir-structure
        self.CoefficientSetsFiles = dict()
        self.DisplayConfigFiles = dict()
        self.FlagConversionsFiles = dict()
        self.IconFiles = dict()
        self.IdMapFiles = dict()
        self.MapLayerFiles = dict()
        self.ModuleConfigFiles = dict()
        self.ModuleDatasetFiles = dict()
        self.PiClientConfigFiles = dict()
        self.RegionConfigFiles = dict()
        self.ReportTemplateFiles = dict()
        self.RootConfigFiles = dict()
        self.SystemConfigFiles = dict()
        self.UnitConversionsFiles = dict()
        self.WorkflowFiles = dict()

        # populate config dir-structure
        self._validate_constructor()
        self._populate_files()
        self._validate_minimal_config_exists()

    def _validate_constructor(self):
        assert isinstance(self.path, Path), f"path {self.path} must be a pathlib.Path"
        assert self.path.is_dir(), f"path {self.path} must be an existing directory"

    def _populate_files(self) -> None:
        """Set all fews config filepaths (.xml, .shx, etc) on self.

        Example result:
            self.CoefficientSetsFiles = {
                'BovenkantBuis': WindowsPath('.../FEWS_SA/config/CoefficientSetsFiles/BovenkantBuis.xml'),
                'DebietParameters': WindowsPath('.../FEWS_SA/config/CoefficientSetsFiles/DebietParameters.xml')
                },
            self.DisplayConfigFiles = {
                'GridDisplay': WindowsPath('../FEWS_SA/config/DisplayConfigFiles/GridDisplay.xml'),
                'ManualForecastDisplay': WindowsPath('.../FEWS_SA/config/DisplayConfigFiles/ManualForecastDisplay.xml'),
                'SystemMonitorDisplay': WindowsPath('.../FEWS_SA/config/DisplayConfigFiles/SystemMonitorDisplay.xml'),
                etc..
                },
            etc..
        """
        for dirpath, dirnames, filenames in os.walk(self.path):
            _dirpath = Path(dirpath)
            if _dirpath == self.path:
                continue
            if _dirpath.name not in self.__dict__.keys():
                continue
            for filename in filenames:
                filename_no_suffix = Path(filename).stem
                full_path = _dirpath / filename
                logger.debug(f"populate FewsConfig with property {_dirpath.name} for file {filename_no_suffix}")
                self.__dict__[_dirpath.name].update({filename_no_suffix: full_path})
        logger.info("finished populating FEWS config files")

    def _validate_minimal_config_exists(self):
        assert self.MapLayerFiles
        assert self.IdMapFiles
        assert self.RegionConfigFiles
        required_region_config_files = ["LocationSets", "Parameters"]
        for required_file in required_region_config_files:
            if not self.RegionConfigFiles.get(required_file, None):
                raise AssertionError(f"{required_file} must be in WIS config {self.path}")

    @property
    def location_sets(self) -> Dict:
        if self._location_sets is not None:
            return self._location_sets
        location_dict = xml_to_dict(xml_filepath=self.RegionConfigFiles["LocationSets"])
        location_sets = location_dict["locationSets"]["locationSet"]
        self._location_sets = {
            location_set["id"]: {key: value for key, value in location_set.items() if key != "id"}
            for location_set in location_sets
        }
        return self._location_sets

    def get_parameters(self, dict_keys: str = "groups") -> Dict:
        """Extract a dictionary of parameter(groups) from a FEWS-config.
        Some waterboards define parameters in a csv file that is read into a parameters.xml.
        HDSR however directly defines it in a parameters.xml"""
        assert dict_keys in ("groups", "parameters")
        parameters_dict = xml_to_dict(xml_filepath=self.RegionConfigFiles["Parameters"])
        parameters = parameters_dict["parameters"]
        if dict_keys == "groups":
            return {
                group["id"]: {key: value for key, value in group.items() if key != "id"}
                for group in parameters["parameterGroups"]["parameterGroup"]
            }
        result = {}
        for group in parameters["parameterGroups"]["parameterGroup"]:
            if type(group["parameter"]) == dict:
                group["parameter"] = [group["parameter"]]
            for parameter in group["parameter"]:
                result.update({parameter["id"]: {}})
                result[parameter["id"]] = {key: value for key, value in parameter.items() if key != "id"}
                result[parameter["id"]].update({key: value for key, value in group.items() if key != "parameter"})
                result[parameter["id"]]["groupId"] = result[parameter["id"]].pop("id")
        return result

    @classmethod
    def add_geometry_column(
        cls, gdf: gpd.GeoDataFrame, filepath: Path, x_attrib: str, y_attrib: str, z_attrib: str = None,
    ) -> gpd.GeoDataFrame:
        """Add geometry column to geodataframe by merging geodataframe columns x, y, and z:
            - if column z_attrib exists, then we fill empty cells ('') with Z_NODATA_VALUE.
            - if column z_attrib does not exists? then we use Z_NODATA_VALUE -9999 for all rows.
        """

        assert (x_attrib and y_attrib) in gdf.columns, f"x={x_attrib} and y={y_attrib} must be in df"
        if z_attrib:
            assert gdf[z_attrib].dtype == "O"
            new_value = str(cls.Z_NODATA_VALUE)
            nr_empty_rows_z = len(gdf[gdf[z_attrib] == ""])
            gdf[z_attrib].replace("", new_value, inplace=True)
            logger.debug(f"replaced {nr_empty_rows_z} gdf rows column {z_attrib} from '' to {new_value}")
        try:
            if z_attrib:
                gdf["geometry"] = gdf.apply(
                    func=(lambda x: Point(float(x[x_attrib]), float(x[y_attrib]), float(x[z_attrib]),)), axis=1,
                )
            else:
                gdf["geometry"] = gdf.apply(
                    func=lambda x: Point(float(x[x_attrib]), float(x[y_attrib]), float(cls.Z_NODATA_VALUE),), axis=1,
                )
            return gdf
        except ValueError:
            # get rows where conversion error occurs (most likely because of empty cells)
            if z_attrib:
                # first make sure the problem is not in z column
                assert (
                    not gdf[z_attrib].astype(float).hasnans
                ), f"the xyz problem is within the {z_attrib} column, file={filepath}"
            # now search through x_attrib and y_attrib
            empty_xy_rows = []
            for column in [x_attrib, y_attrib]:
                empty_xy_rows.extend(list(gdf[gdf[column] == ""].index))
            assert empty_xy_rows, f"did not find expected empty_rows xy? file={filepath}"
            raise AssertionError(f"found '' in xy for dataframe rows={empty_xy_rows} from file={filepath}")
        except Exception as err:
            raise AssertionError(f"unexpected error for xyz, err={err}, file={filepath}")

    def get_locations(self, location_set_key: str) -> Optional[gpd.GeoDataFrame]:
        """Convert FEWS locationSet locations into df. Args 'location_set_key' (str) is e.g. 'OPVLWATER_HOOFDLOC'."""
        assert isinstance(location_set_key, str)
        location_set = self.location_sets.get(location_set_key, None)
        if not location_set:
            logger.warning(f"no location_set found in fews_config for location_set_key: {location_set_key}")
            return

        file = location_set.get("csvFile", {}).get("file", None)
        if not file:
            logger.warning(f"found location_set but not file in fews_config for location_set_key: {location_set_key}")
            return

        file = Path(file)
        if not file.suffix:
            file = file.parent / (file.name + ".csv")
        filepath = self.path / "MapLayerFiles" / file
        assert filepath.is_file(), f"file {filepath} does not exist"
        gdf = gpd.read_file(filename=filepath)

        x_attrib = location_set["csvFile"]["x"].replace("%", "")
        y_attrib = location_set["csvFile"]["y"].replace("%", "")
        # z column does not always exist
        z_attrib = location_set["csvFile"].get("z", "").replace("%", "")
        gdf = self.add_geometry_column(
            gdf=gdf, filepath=filepath, x_attrib=x_attrib, y_attrib=y_attrib, z_attrib=z_attrib,
        )
        geo_datum_found = location_set["csvFile"]["geoDatum"]
        crs = self.geo_datum.get(geo_datum_found, None)
        gdf.crs = crs if crs else None
        return gdf
