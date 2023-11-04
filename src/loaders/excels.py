import pandas as pd
import re


def analyse_code(code: str) -> str:
    code = re.sub("[^0-9A-Z]+", "", str(code).upper())
    if len(code) <= 0 or code in ["NAN", "JESAISPAS", "AUCUNEIDEE", "JENESAISPAS"]:
        return "NOTABLE"
    return code


def process_excel(file):
    data = pd.read_excel(file, index_col=0)
    data["Code table"] = [analyse_code(code) for code in data["Code table"]]
    data["Code table ami"] = [analyse_code(code) for code in data["Code table ami"]]
    return data
