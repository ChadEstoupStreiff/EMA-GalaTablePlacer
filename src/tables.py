import json
import copy
import random
import streamlit as st

import math
from stqdm import stqdm


def get_distance(A, B):
    return math.sqrt(abs(A[0] - B[0]) ** 2 + abs(A[1] - B[1]) ** 2)


def load_tables():
    with open("/app/tables.json", "r") as f_i:
        tables = json.loads(f_i.read())
    return tables


def get_score(tables, physical_table):
    score = 0
    for i, tableA in enumerate(tables):
        nbr_friend = 0
        in_distance_friend = 0
        for j, tableB in enumerate(tables):
            if i != j:
                for code in tableB["codes"]:
                    if code[0] in tableA["friends"]:
                        nbr_friend += 1
                        if get_distance(physical_table[i], physical_table[j]) < 3:
                            in_distance_friend += 1
                        break
        if nbr_friend > 0:
            score += int(in_distance_friend / nbr_friend * 1000)
        score -= 10 * physical_table[i][0]
    return score


def get_solution(tables, physical_tables, nbr_random=100):
    best_sol = None
    best_score = None

    empty = st.empty()
    for _ in stqdm(range(nbr_random)):
        loop_tables = copy.copy(tables)
        random.shuffle(loop_tables)
        score = get_score(loop_tables, physical_tables)
        if best_score is None or score > best_score:
            best_sol = loop_tables
            best_score = score

            with empty:
                st.info(f"Actual best score: {best_score}")

    for i, table in enumerate(best_sol):
        table["coord"] = physical_tables[i]
    return best_sol, best_score
