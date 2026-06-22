import re
import io
import os
import zipfile
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# --------------------------------------------------
# columns
# --------------------------------------------------

COLUMNS = [
    "name_j",
    # "availability",
    "code_map",
    # "type_muni",
    "name_e",
    "year",
    "url",
    "zip",
    "shp",
    # "geojson",
    "altdir",
    # "source",
    # "col",
    # "levels",
    # "labels",
    # "palette",
    # "muni_column",
    # "muni_type",
    # "encoding",
    "qml",
    # "epsg",
    # "filesize",
]


# --------------------------------------------------
# utils
# --------------------------------------------------

def log(msg):
    print(f"[INFO] {msg}")


def fetch_soup(url):
    log(f"FETCH {url}")
    r = requests.get(url, timeout=60)
    r.encoding = r.apparent_encoding
    return BeautifulSoup(r.text, "html.parser")


def create_row():
    return {c: None for c in COLUMNS}


def is_target(href):
    href = href.lower()
    return href.endswith(".zip") or href.endswith(".csv")


def get_filename(url):
    return os.path.basename(urlparse(url).path)


def extract_csv_from_zip(url):
    log(f"ZIP DOWNLOAD {url}")

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    z = zipfile.ZipFile(io.BytesIO(r.content))

    csvs = [n for n in z.namelist() if n.lower().endswith(".csv")]

    return csvs[0] if csvs else None


def resolve_file(url):
    """
    return:
        zip (filename)
        shp (csv filename)
    """

    fname = get_filename(url)

    if fname.lower().endswith(".zip"):
        shp = extract_csv_from_zip(url)
        return fname, shp

    # csv direct
    return fname, fname


# --------------------------------------------------
# MHLW
# --------------------------------------------------

def parse_name_and_size(text):

    text = re.sub(r"\s+", " ", text.strip())

    filesize = None

    # ファイルサイズ抽出
    m = re.search(r"\[([0-9.]+\s*[KMGT]?B)\]\s*$", text)
    if m:
        filesize = m.group(1)
        text = text[:m.start()].strip()

    # code_map抽出
    m2 = re.match(r"^(\d+)\s*[_\s\-－]?\s*(.+)$", text)
    code_map = None
    name_j = text

    if m2:
        code_map = f"Disability_{m2.group(1)}"
        name_j = m2.group(2)

    return name_j, code_map, filesize


def scrape_mhlw():

    url = "https://www.mhlw.go.jp/stf/kaigo-kouhyou_opendata.html"
    log("START MHLW")

    soup = fetch_soup(url)

    rows = []
    current_year = None

    for tag in soup.find_all(["h3", "a"]):

        # YEAR
        if tag.name == "h3":
            t = tag.get_text(" ", strip=True)
            if re.search(r"\d{4}", t):
                current_year = t
                log(f"MHLW YEAR = {current_year}")
            continue

        # link
        href = tag.get("href")
        if not href or not is_target(href):
            continue

        text = tag.get_text(" ", strip=True)

        name_j, code_map, filesize = parse_name_and_size(text)

        row["name_j"] = name_j
        row["code_map"] = code_map
        row["filesize"] = filesize

        fname, shp = resolve_file(urljoin(url, href))

        row = create_row()

        # row["source"] = "MHLW"
        row["year"] = current_year
        row["code_map"] = "LtCI_" + code_map
        row["name_j"] = name_j
        row["url"] = urljoin(url, href)
        row["zip"] = fname
        row["shp"] = shp
        # row["filesize"] = None

        rows.append(row)

    log(f"END MHLW ({len(rows)})")
    return rows


# --------------------------------------------------
# WAM
# --------------------------------------------------

def scrape_wam():

    url = "https://www.wam.go.jp/content/wamnet/pcpub/top/sfkopendata/"
    log("START WAM")

    soup = fetch_soup(url)

    rows = []
    current_year = None

    for tag in soup.descendants:

        if not hasattr(tag, "name"):
            continue

        # YEAR
        if tag.name == "div":
            text = tag.get_text(" ", strip=True)

            if re.search(r"\d{4}年.*時点", text):
                current_year = text
                log(f"WAM YEAR = {current_year}")

        # data
        if tag.name == "a":

            href = tag.get("href")
            if not href or not is_target(href):
                continue

            fname, shp = resolve_file(urljoin(url, href))

            row = create_row()

            # row["source"] = "WAM"
            row["year"] = current_year
            row["code_map"] = tag.get_text(" ", strip=True)
            row["name_j"] = tag.get_text(" ", strip=True)
            row["url"] = urljoin(url, href)
            row["zip"] = fname
            row["shp"] = shp

            rows.append(row)

    log(f"END WAM ({len(rows)})")
    return rows


# --------------------------------------------------
# build
# --------------------------------------------------

def build():

    log("BUILD START")

    rows = []
    rows += scrape_mhlw()
    rows += scrape_wam()

    df = pd.DataFrame(rows, columns=COLUMNS)

    df.to_csv("kaigo_catalog.csv", index=False, encoding="utf-8-sig")

    log("CSV WRITTEN: kaigo_catalog.csv")

    return df


# --------------------------------------------------
# main
# --------------------------------------------------

if __name__ == "__main__":
    build()