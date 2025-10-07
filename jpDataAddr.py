# -*- coding: utf-8 -*-
import os, csv
from . import jpDataUtils

# --- Module-level cache: dict {pref_code: list_of_rows} ---
from collections import OrderedDict

# global cache: keep up to 5 items
_csv_cache = OrderedDict()
_CACHE_SIZE = 5


def get_url(pref_code):
    return (
        "https://nlftp.mlit.go.jp/isj/dls/data/23.0a/"
        + str(pref_code).zfill(2)
        + "000-23.0a.zip"
    )


def get_zip(pref_code):
    return str(pref_code).zfill(2) + "000-23.0a.zip"


def _load_csv(folder, pref_code, encoding="cp932"):
    """Load and cache the CSV for a given prefecture code (max 5 cached).

    Args:
        folder (str): Base folder containing Addr subfolder.
        pref_code (str|int): Prefecture code.
        encoding (str): Encoding of the CSV (default: cp932).

    Returns:
        list[list[str]]: Rows from the CSV.
        None: If file does not exist.
    """
    pref_code = str(pref_code).zfill(2)

    # if cached, move it to the end (mark as most recently used)
    if pref_code in _csv_cache:
        _csv_cache.move_to_end(pref_code)
        return _csv_cache[pref_code]

    # construct path
    data_file = os.path.join(
        folder, "Addr", f"{pref_code}000-23.0a", f"{pref_code}_2024.csv"
    )

    try:
        with open(data_file, "r", encoding=encoding) as f:
            reader = csv.reader(f)
            rows = [row for row in reader if any(row)]
    except FileNotFoundError:
        return None

    # insert into cache
    _csv_cache[pref_code] = rows
    _csv_cache.move_to_end(pref_code)

    # evict oldest if over capacity
    if len(_csv_cache) > _CACHE_SIZE:
        _csv_cache.popitem(last=False)

    return rows


def set_cb_prefs(combobox):
    """Set preferences for address data source selection combobox."""
    combobox.clear()
    for i in range(1, 48):
        combobox.addItem(jpDataUtils.getPrefNameByCode(i))


def set_cb_cities(combobox, folder, pref_name):
    """Set city names in the combobox based on the selected prefecture code."""
    combobox.clear()
    cities = _get_cities_by_prefcode(folder, pref_name)
    if cities:
        for city in cities:
            combobox.addItem(city)
        combobox.setCurrentIndex(0)
        return True
    else:
        return False


def set_cb_towns(combobox, folder, pref_name, city_name):
    """Set town names in the combobox based on the selected prefecture code and city name."""
    combobox.clear()
    towns = _get_towns_by_municode(folder, pref_name, city_name)
    if towns:
        for town in towns:
            combobox.addItem(town)
        combobox.setCurrentIndex(0)


def set_cb_details(combobox, folder, pref_name, city_name, town_name):
    """Set town names in the combobox based on the selected prefecture code and city name."""
    combobox.clear()
    details = _get_details_by_town(folder, pref_name, city_name, town_name)
    if details:
        for detail in details:
            combobox.addItem(detail)
        combobox.setCurrentIndex(0)


def _get_cities_by_prefcode(folder, pref_name):
    pref_code = jpDataUtils.getPrefCodeByName(pref_name)
    unzip_addr_data(folder)
    rows = _load_csv(folder, pref_code)
    if rows is None:
        return False

    cities = [row[1] for row in rows if len(row) > 1]
    unique_rows = []
    for x in cities:
        if x not in unique_rows and x not in ("", "市区町村名"):
            unique_rows.append(x)
    return unique_rows


def _get_towns_by_municode(folder, pref_name, city_name):
    pref_code = jpDataUtils.getPrefCodeByName(pref_name)
    rows = _load_csv(folder, pref_code)
    if rows is None:
        return False

    towns = [row[2] for row in rows if len(row) > 2 and row[1] == city_name]
    return sorted(set(towns))


def _get_details_by_town(folder, pref_name, city_name, town_name):
    pref_code = jpDataUtils.getPrefCodeByName(pref_name)
    rows = _load_csv(folder, pref_code)
    if rows is None:
        return False

    details = [
        row[4]
        for row in rows
        if len(row) > 5 and row[1] == city_name and row[2] == town_name
    ]
    return sorted(set(details))


def unzip_addr_data(folder):
    """Unzip address data files if not already unzipped."""
    for i in range(1, 48):
        pref_code = str(i).zfill(2)
        if os.path.exists(
            os.path.join(folder, "Addr", pref_code + "000-23.0a.zip")
        ) and not os.path.exists(
            os.path.join(
                folder, "Addr", pref_code + "000-23.0a", pref_code + "_2024.csv"
            )
        ):
            jpDataUtils.unzip(os.path.join(folder, "Addr"), pref_code + "000-23.0a.zip")


def get_lonlat_by_addr(folder, pref_name, city_name, town_name, detail_code):
    pref_code = jpDataUtils.getPrefCodeByName(pref_name)
    rows = _load_csv(folder, pref_code)
    if rows is None:
        return (None, None)

    for row in rows:
        if (
            len(row) > 9
            and row[1] == city_name
            and row[2] == town_name
            and row[4] == detail_code
        ):
            return (float(row[9]), float(row[8]))  # lon, lat
    return (None, None)
