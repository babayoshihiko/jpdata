# -*- coding: utf-8 -*-
import os, csv
from . import jpDataUtils

# --- Module-level cache: dict {pref_code: list_of_rows} ---
_csv_cache = {}


def _load_csv(folder, pref_code):
    """Load and cache the CSV for a given prefecture code."""
    if pref_code not in _csv_cache:
        data_file = os.path.join(
            folder,
            "Addr",
            pref_code.zfill(2) + "000-23.0a",
            pref_code.zfill(2) + "_2024.csv",
        )
        with open(data_file, "r", encoding="CP932") as f:
            reader = csv.reader(f)
            _csv_cache[pref_code] = [row for row in reader if row]
    return _csv_cache[pref_code]


def set_cb_prefs(combobox):
    """Set preferences for address data source selection combobox."""
    combobox.clear()
    for i in range(1, 48):
        combobox.addItem(jpDataUtils.getPrefNameByCode(i))
    combobox.setCurrentIndex(12)


def set_cb_cities(combobox, folder, pref_name):
    """Set city names in the combobox based on the selected prefecture code."""
    combobox.clear()
    cities = _get_cities_by_prefcode(folder, pref_name)
    for city in cities:
        combobox.addItem(city)
    if cities:
        combobox.setCurrentIndex(0)


def set_cb_towns(combobox, folder, pref_name, city_name):
    """Set town names in the combobox based on the selected prefecture code and city name."""
    combobox.clear()
    towns = _get_towns_by_municode(folder, pref_name, city_name)
    for town in towns:
        combobox.addItem(town)
    if towns:
        combobox.setCurrentIndex(0)


def set_cb_details(combobox, folder, pref_name, city_name, town_name):
    """Set town names in the combobox based on the selected prefecture code and city name."""
    combobox.clear()
    details = _get_details_by_town(folder, pref_name, city_name, town_name)
    for detail in details:
        combobox.addItem(detail)
    if details:
        combobox.setCurrentIndex(0)


def _get_cities_by_prefcode(folder, pref_name):
    pref_code = jpDataUtils.getPrefCodeByName(pref_name)
    unzip_addr_data(folder)
    rows = _load_csv(folder, pref_code)

    cities = [row[1] for row in rows if len(row) > 1]
    unique_rows = []
    for x in cities:
        if x not in unique_rows and x not in ("", "市区町村名"):
            unique_rows.append(x)
    return unique_rows


def _get_towns_by_municode(folder, pref_name, city_name):
    pref_code = jpDataUtils.getPrefCodeByName(pref_name)
    rows = _load_csv(folder, pref_code)

    towns = [row[2] for row in rows if len(row) > 2 and row[1] == city_name]
    return sorted(set(towns))


def _get_details_by_town(folder, pref_name, city_name, town_name):
    pref_code = jpDataUtils.getPrefCodeByName(pref_name)
    rows = _load_csv(folder, pref_code)

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

    for row in rows:
        if (
            len(row) > 9
            and row[1] == city_name
            and row[2] == town_name
            and row[4] == detail_code
        ):
            return (float(row[9]), float(row[8]))  # lon, lat
    return (None, None)
