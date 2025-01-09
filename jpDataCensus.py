# -*- coding: utf-8 -*-


def getUrl(year, code_pref, code_muni, type_muni="小地域"):
    url = None
    if len(code_pref) == 1:
        code_pref = "0" + code_pref

    if type_muni == "小地域":
        if year == "2020" or year == "2015":
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A00200521"
                + year
                + "&code="
                + code_pref
                + code_muni
                + "&coordSys=2&format=shape&downloadType=5&datum=2011"
            )
        else:
            url = (
                "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=A00200521"
                + year
                + "&code="
                + code_pref
                + code_muni
                + "&coordSys=2&format=shape&downloadType=5&datum=2000"
            )
    elif type_muni == "3次メッシュ（1kmメッシュ）":
        url = (
            "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=S&code="
            + code_muni
            + "&coordSys=1&format=shape&downloadType=5"
        )
    elif type_muni == "4次メッシュ（500mメッシュ）":
        url = (
            "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=H&code="
            + code_muni
            + "&coordSys=1&format=shape&downloadType=5"
        )
    elif type_muni == "5次メッシュ（250mメッシュ）":
        url = (
            "https://www.e-stat.go.jp/gis/statmap-search/data?dlserveyId=Q&code="
            + code_muni
            + "&coordSys=1&format=shape&downloadType=5"
        )
    return url


def getZipFileName(year, code_pref, code_muni, type_muni="小地域"):
    zipFileName = None
    if type_muni == "小地域":
        if len(code_pref) == 1:
            code_pref = "0" + code_pref
        if year == "2020" or year == "2015":
            zipFileName = (
                "A00200521" + year + "XYSWC" + code_pref + code_muni + "-JGD2011.zip"
            )
        else:
            zipFileName = "A00200521" + year + "XYSWC" + code_pref + code_muni + ".zip"
    elif type_muni == "3次メッシュ（1kmメッシュ）":
        zipFileName = "SDDSWS" + code_muni + ".zip"
    elif type_muni == "4次メッシュ（500mメッシュ）":
        zipFileName = "HDDSWH" + code_muni + ".zip"
    elif type_muni == "5次メッシュ（250mメッシュ）":
        zipFileName = "QDDSWQ" + code_muni + ".zip"
    return zipFileName


def getShpFileName(year, code_pref, code_muni, type_muni="小地域"):
    shpFileName = None
    if len(code_pref) == 1:
        code_pref = "0" + code_pref
    if type_muni == "小地域":
        if year == "2020":
            shpFileName = "r2ka" + code_pref + code_muni + ".shp"
        elif year == "2015":
            shpFileName = "h27ka" + code_pref + code_muni + ".shp"
        elif year == "2010":
            shpFileName = "h22ka" + code_pref + code_muni + ".shp"
        elif year == "2005":
            shpFileName = "h17ka" + code_pref + code_muni + ".shp"
        elif year == "2000":
            shpFileName = "h12ka" + code_pref + code_muni + ".shp"
    elif type_muni == "3次メッシュ（1kmメッシュ）":
        shpFileName = "MESH0" + code_muni + ".shp"
    elif type_muni == "4次メッシュ（500mメッシュ）":
        shpFileName = "MESH0" + code_muni + ".shp"
    elif type_muni == "5次メッシュ（250mメッシュ）":
        shpFileName = "MESH0" + code_muni + ".shp"
    return shpFileName
