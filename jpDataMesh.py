# -*- coding: utf-8 -*-

import os, posixpath, csv
from . import jpDataUtils


def unique_sorted_values(rows, key):
    return sorted({row[key] for row in rows})


def getMesh1ByPrefName(name_pref):
    str_code_pref = jpDataUtils.getPrefCodeByName(name_pref)
    return getMesh1ByPrefCode(str_code_pref)


def getMesh1ByPrefMuniName(name_pref, name_munis, lang="j"):
    str_code_pref = jpDataUtils.getPrefCodeByName(name_pref)
    int_code_pref = int(str_code_pref)

    cvsfile = posixpath.join(os.path.dirname(__file__), "csv", "muni_mesh1.csv")
    rows = jpDataUtils.get_records_from_csv(cvsfile)

    mesh1s = [
        row["code_mesh1"]
        for row in rows
        if int(row["code_pref"]) == int_code_pref
        and (row["name_muni_e"] in name_munis or row["name_muni_j"] in name_munis)
    ]

    return sorted(set(mesh1s))


def getMesh1ByPrefCode(code_pref):
    if code_pref == "":
        return []

    int_code_pref = int(code_pref)

    cvsfile = posixpath.join(os.path.dirname(__file__), "csv", "muni_mesh1.csv")
    rows = jpDataUtils.get_records_from_csv(cvsfile)

    rows = [r for r in rows if int(r["code_pref"]) == int_code_pref]

    return unique_sorted_values(rows, "code_mesh1")


def getMesh1ByPrefMuniCode(code_pref, code_muni):
    int_code_pref = int(code_pref)
    int_code_muni = int(code_muni)

    cvsfile = posixpath.join(os.path.dirname(__file__), "csv", "muni_mesh1.csv")
    rows = jpDataUtils.get_records_from_csv(cvsfile)

    rows = [
        r for r in rows
        if int(r["code_pref"]) == int_code_pref
        and int(r["code_muni"]) == int_code_muni
    ]

    return unique_sorted_values(rows, "code_mesh1")


def getMeshExpression(code_map):
    str_expression = ""
    if code_map == "L03-a":
        str_expression = "CASE "
        str_expression += 'WHEN "田" > "他農用地" AND "田" > "森林" AND "田" > "荒地" AND "田" > "建物用地" AND "田" > "道路" AND "田" > "鉄道" AND "田" > "他用地" AND "田" > "河川湖沼" AND "田" > "海水域" AND "田" > "ゴルフ場" AND "田" > "範囲外" THEN \'田\' '
        str_expression += 'WHEN "他農用地" > "森林" AND "他農用地" > "荒地" AND "他農用地" > "建物用地" AND "他農用地" > "道路" AND "他農用地" > "鉄道" AND "他農用地" > "他用地" AND "他農用地" > "河川湖沼" AND "他農用地" > "海水域" AND "他農用地" > "ゴルフ場" AND "他農用地" > "範囲外" THEN \'他農用地\' '
        str_expression += 'WHEN "森林" > "荒地" AND "森林" > "建物用地" AND "森林" > "道路" AND "森林" > "鉄道" AND "森林" > "他用地" AND "森林" > "河川湖沼" AND "森林" > "海水域" AND "森林" > "ゴルフ場" AND "森林" > "範囲外" THEN \'森林\' '
        str_expression += 'WHEN "荒地" > "建物用地" AND "荒地" > "道路" AND "荒地" > "鉄道" AND "荒地" > "他用地" AND "荒地" > "河川湖沼" AND "荒地" > "海水域" AND "荒地" > "ゴルフ場" AND "荒地" > "範囲外" THEN \'荒地\' '
        str_expression += 'WHEN "建物用地" > "道路" AND "建物用地" > "鉄道" AND "建物用地" > "他用地" AND "建物用地" > "河川湖沼" AND "建物用地" > "海水域" AND "建物用地" > "ゴルフ場" AND "建物用地" > "範囲外" THEN \'建物用地\' '
        str_expression += 'WHEN "道路" > "鉄道" AND "道路" > "他用地" AND "道路" > "河川湖沼" AND "道路" > "海水域" AND "道路" > "ゴルフ場" AND "道路" > "範囲外" THEN \'道路\' '
        str_expression += 'WHEN "鉄道" > "他用地" AND "鉄道" > "河川湖沼" AND "鉄道" > "海水域" AND "鉄道" > "ゴルフ場" AND "鉄道" > "範囲外" THEN \'鉄道\' '
        str_expression += 'WHEN "他用地" > "河川湖沼" AND "他用地" > "海水域" AND "他用地" > "ゴルフ場" AND "他用地" > "範囲外" THEN \'他用地\' '
        str_expression += 'WHEN "河川湖沼" > "海水域" AND "河川湖沼" > "ゴルフ場" AND "河川湖沼" > "範囲外" THEN \'河川湖沼\' '
        str_expression += (
            'WHEN "海水域" > "ゴルフ場" AND "海水域" > "範囲外" THEN \'海水域\' '
        )
        str_expression += 'WHEN "ゴルフ場" > "範囲外" THEN \'ゴルフ場\' '
        str_expression += "ELSE '範囲外' END"
    return str_expression
