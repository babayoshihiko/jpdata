import sys, os, csv, posixpath
import zipfile
import re

this = sys.modules[__name__]
this.rows = None


def get_name_from_code(code):
    for row in this.rows:
        if int(row["code_pref"]) * 1000 * int(row["code_muni"]) == int(code):
            return row["name_muni"]
    return code


def get_name_from_shp(shp):
    code = re.findall("[0-9]{5}", shp)[0]
    if code is None:
        return ""
    else:
        return get_name_from_code(code)


def get_detail2(shp):
    if len(re.findall("bouka", shp)) == 1:
        return "防火・準防火地域"
    elif len(re.findall("chikukei", shp)) == 1:
        return "地区計画"
    elif len(re.findall("douro", shp)) == 1:
        return "都市計画道路"
    elif len(re.findall("koudori", shp)) == 1:
        return "高度利用地区"
    elif len(re.findall("koudoti", shp)) == 1:
        return "高度地区"
    elif len(re.findall("kouen", shp)) == 1:
        return "都市公園"
    elif len(re.findall("senbiki", shp)) == 1:
        return "区域区分"
    elif len(re.findall("tkbt", shp)) == 1:
        return "特別用途地域"
    elif len(re.findall("tochiku", shp)) == 1:
        return "土地区画整理事業"
    elif len(re.findall("tokei", shp)) == 1:
        return "都市計画区域"
    elif len(re.findall("youto", shp)) == 1:
        return "用途地域"
    else:
        return ""


def get_qml(shp):
    if len(re.findall("bouka", shp)) == 1:
        return "A55-2023_bouka.qml"
    elif len(re.findall("chikukei", shp)) == 1:
        return "A55-2023_chikukei.qml"
    elif len(re.findall("douro", shp)) == 1:
        return "A55-2023_douro.qml"
    elif len(re.findall("koudori", shp)) == 1:
        return "A55-2023_koudori.qml"
    elif len(re.findall("koudoti", shp)) == 1:
        return "A55-2023_koudoti.qml"
    elif len(re.findall("kouen", shp)) == 1:
        return "A55-2023_kouen.qml"
    elif len(re.findall("senbiki", shp)) == 1:
        return "A55-2023_senbiki.qml"
    elif len(re.findall("tkbt", shp)) == 1:
        return "A55-2023_tkbt.qml"
    elif len(re.findall("tochiku", shp)) == 1:
        return "A55-2023_tochiku.qml"
    elif len(re.findall("tokei", shp)) == 1:
        return "A55-2023_tokei.qml"
    elif len(re.findall("youto", shp)) == 1:
        return "A55-2023_youto.qml"
    else:
        return ""


def list_files_in_zip(zip_filepath, output_txt_path, url, year, name, code_filepath):
    """
    Lists all files in the given ZIP file and writes the list to a text file.

    :param zip_filepath: Path to the ZIP file
    :param output_txt_path: Path to the output text file
    """

    if os.path.exists(code_filepath):
        with open(code_filepath, "r") as f:
            csvreader = csv.DictReader(f)
            this.rows = list(csvreader)
    else:
        print(f"Error: The file {code_filepath} does not exist.")
        return

    if not os.path.exists(zip_filepath):
        print(f"Error: The file {zip_filepath} does not exist.")
        return

    if not zipfile.is_zipfile(zip_filepath):
        print(f"Error: The file {zip_filepath} is not a valid ZIP archive.")
        return

    try:
        with zipfile.ZipFile(zip_filepath, "r") as zip_file:
            with open(output_txt_path, "w") as txt_file:

                # txt_file.write(
                #    "availability,year,url,zip,shp,altdir,qml,detail1,detail2\n"
                # )
                for zip_info in zip_file.infolist():
                    # Extract the filename using the correct encoding
                    # (e.g. 'cp932' for Japanese Windows)
                    filename = zip_info.filename.encode("cp437").decode("cp932")

                    if not zip_info.is_dir():
                        if filename[-4:] == ".shp":

                            detail1 = get_name_from_shp(filename)
                            detail2 = get_detail2(filename)
                            qml = get_qml(filename)
                            txt_file.write(
                                name
                                + ","
                                + year
                                + ","
                                + url
                                + ","
                                + zip_filepath
                                + ","
                                + filename
                                + ",,"
                                + qml
                                + ","
                                + detail1
                                + ","
                                + detail2
                                + "\n"
                            )

            print(f"File list written to {output_txt_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # name = input("Enter the name: ").strip()
    # year = input("Enter the year: ").strip()
    # url = input("Enter the URL: ").strip()
    # zip_path = input("Enter the path to the ZIP file: ").strip()
    # output_path = input("Enter the path for the output text file: ").strip()
    # code_filepath = input("Enter the path for the code csv: ").strip()
    name = sys.argv[1]
    year = sys.argv[2]
    code = sys.argv[3]
    url = (
        "https://nlftp.mlit.go.jp/ksj/gml/data/A55a/A55a-23/A55a-23_"
        + code
        + "_10_SHP.zip"
    )
    zip_path = os.path.expanduser("~/Downloads/A55-22_" + code + "000_SHP.zip")
    output_path = os.path.expanduser("~/Downloads/A55-22_" + code + "000_SHP.csv")
    code_filepath = os.path.expanduser("~/github/jpdata/csv/code_pref_muni.csv")

    list_files_in_zip(zip_path, output_path, url, year, name, code_filepath)
