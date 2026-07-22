import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://bustime.jp/GtfsAgency/gtfs_list/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers)
r.raise_for_status()

# UTF-8指定
r.encoding = "utf-8"

soup = BeautifulSoup(r.text, "html.parser")

table = soup.find("table")

rows = []

for tr in table.find_all("tr")[1:]:   # ヘッダを飛ばす
    tds = tr.find_all("td")

    # 途中に「期限まで○日」などの行があるので除外
    if len(tds) < 10:
        continue

    # 列
    name = tds[0].get_text(" ", strip=True)
    prefecture = tds[1].get_text(strip=True)

    # DL列（5列目）
    dl_link = ""
    a = tds[4].find("a")
    if a and a.get("href"):
        dl_link = urljoin(URL, a["href"])

    # 有効期限(feed_end_date)
    feed_end = tds[9].get_text(" ", strip=True)

    rows.append({
        "name": name,
        "prefecture": prefecture,
        "download": dl_link,
        "feed_end_date": feed_end,
    })

# 表示と出力    
with open("gtfs_list.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)

    # ヘッダ
    writer.writerow(["データ名", "都道府県", "DL", "有効期限"])

    # データ
    for row in rows:
        print(row)
        writer.writerow([
            row["name"],
            row["prefecture"],
            row["download"],
            row["feed_end_date"],
        ])


print(f"\nTotal: {len(rows)}")