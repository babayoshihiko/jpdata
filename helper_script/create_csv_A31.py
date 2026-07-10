import sys
import os
import csv
import zipfile
import re


# macOS / VS Code 環境での出力文字コード対策
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass


rows = []


def decode_zip_filename(zip_info):
    """
    古い ZIP（cp437 として誤認識されるもの）と
    新しい ZIP（UTF-8 正常処理）の両方に対応
    """
    try:
        return zip_info.filename.encode("cp437").decode("cp932")
    except UnicodeEncodeError:
        return zip_info.filename
    except UnicodeDecodeError:
        return zip_info.filename


def get_name_from_code(code):
    for row in rows:
        if int(row["code"]) == int(code):
            return row["name"]
    return code


def get_name_from_shp(shp):
    match = re.search(r"[0-9]{10}", shp)
    if match:
        return get_name_from_code(match.group())
    return ""


def get_detail2(shp):
    if "計画規模" in shp:
        return "計画規模"
    elif "想定最大規模" in shp:
        return "想定最大規模"
    elif "浸水継続時間" in shp:
        return "浸水継続時間"
    elif "家屋倒壊等氾濫想定区域_氾濫流" in shp:
        return "家屋倒壊等氾濫想定区域_氾濫流"
    elif "家屋倒壊等氾濫想定区域_河岸侵食" in shp:
        return "家屋倒壊等氾濫想定区域_河岸侵食"
    else:
        return ""


def get_qml(shp):
    if "計画規模" in shp:
        return "A31-2023_Plan.qml"
    elif "想定最大規模" in shp:
        return "A31-2023_Worst.qml"
    elif "浸水継続時間" in shp:
        return "A31-2023_FloodDuration.qml"
    elif "家屋倒壊等氾濫想定区域_氾濫流" in shp:
        return "A31-2023_Overflow.qml"
    elif "家屋倒壊等氾濫想定区域_河岸侵食" in shp:
        return "A31-2023_Erosion.qml"
    else:
        return ""


def list_files_in_zip(zip_filepath, output_txt_path, url, year, name, code_filepath):

    global rows

    # CSV 読み込み
    if os.path.exists(code_filepath):
        with open(code_filepath, "r", encoding="utf-8") as f:
            csvreader = csv.DictReader(f)
            rows = list(csvreader)
    else:
        print(f"Error: The file {code_filepath} does not exist.")
        return


    if not os.path.exists(zip_filepath):
        print(f"Error: The file {zip_filepath} does not exist.")
        return


    if not zipfile.is_zipfile(zip_filepath):
        print(f"Error: The file {zip_filepath} is not a valid ZIP archive.")
        return


    zip_filename = os.path.basename(zip_filepath)


    try:
        with zipfile.ZipFile(zip_filepath, "r") as zip_file:

            with open(
                output_txt_path,
                "w",
                encoding="utf-8-sig",
                newline=""
            ) as txt_file:

                writer = csv.writer(txt_file)

                for zip_info in zip_file.infolist():

                    if zip_info.is_dir():
                        continue

                    # 以前必要だった処理を維持
                    # filename = zip_info.filename.encode("cp437").decode("cp932")
                    filename = decode_zip_filename(zip_info)
                    filename = filename.replace("\\", "/")


                    if filename.lower().endswith(".shp"):

                        detail1 = get_name_from_shp(filename)
                        detail2 = get_detail2(filename)
                        qml = get_qml(filename)

                        writer.writerow([
                            name,
                            year,
                            url,
                            zip_filename,
                            filename,
                            "",
                            qml,
                            detail1,
                            detail2
                        ])


        print(f"File list written to {output_txt_path}")


    except Exception:
        import traceback
        traceback.print_exc()



if __name__ == "__main__":

    year = sys.argv[1]
    code = sys.argv[2]
    name = sys.argv[3]

    year2digit = year[-2:]

    url = (
        f"https://nlftp.mlit.go.jp/ksj/gml/data/A31a/"
        f"A31a-{year2digit}/"
        f"A31a-{year2digit}_{code}_10_SHP.zip"
    )

    zip_path = os.path.expanduser(
        f"~/data.noindex/A31a/A31a-{year2digit}_{code}_10_SHP.zip"
    )

    output_path = os.path.expanduser(
        f"~/data.noindex/A31a/A31a-{year2digit}_{code}_10_SHP.csv"
    )

    code_filepath = os.path.expanduser(
        "~/github.noindex/jpdata/helper_script/RiverCode.csv"
    )


    list_files_in_zip(
        zip_path,
        output_path,
        url,
        year,
        name,
        code_filepath
    )