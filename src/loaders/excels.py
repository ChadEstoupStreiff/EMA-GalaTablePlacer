import pandas as pd
import re
from unidecode import unidecode


def analyse_code(code: str) -> str:
    code = re.sub("[^0-9A-Z]+", "", unidecode(str(code)).upper())
    if len(code) <= 0 or code in ["NAN", "JESAISPAS", "AUCUNEIDEE", "JENESAISPAS"]:
        return None
    return code


def process_excel(file):
    data = pd.read_excel(file, index_col=0)
    data["Prénom"] = [str(value).capitalize() for value in data["Prénom"]]
    data["Nom"] = [str(value).upper() for value in data["Nom"]]
    data["Code table"] = [
        analyse_code(code) if analyse_code(code) is not None else "NOTABLE"
        for code in data["Code table"]
    ]
    data["Code table ami"] = [analyse_code(code) for code in data["Code table ami"]]
    return data
