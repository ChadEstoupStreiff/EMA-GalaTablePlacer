import json
import copy
import random
import sys
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

import os
import math
from stqdm import stqdm


__SOURCES = "/app"

def draw_physical_tables(draw, image_scale, tables):
    for table in tables:
        draw.rectangle(
            (
                image_scale * table[0] + image_scale,
                image_scale * table[1] + image_scale,
                image_scale * (table[0] + 1) + image_scale,
                image_scale * (table[1] + 1) + image_scale,
            ),
            fill="#1F1F1F",
        )


def draw_tables(draw, image_scale, tables, show_name):
    for table in tables:
        draw.rectangle(
            (
                image_scale * table["coord"][0] + image_scale,
                image_scale * table["coord"][1] + image_scale,
                image_scale * (table["coord"][0] + 1) + image_scale,
                image_scale * (table["coord"][1] + 1) + image_scale,
            ),
            fill="#ffff33",
        )
        if show_name:
            fnt = ImageFont.truetype(os.path.join(__SOURCES, "font.ttf"), 40)
            draw.text(
                (
                    image_scale * table["coord"][0] + image_scale,
                    image_scale * table["coord"][1] + image_scale,
                ),
                table["id"],
                font=fnt,
                fill=(0, 0, 0, 128),
            )


def draw_solution(
    tables, physical_tables, table=None, path="tmp.png", show_names=False
):
    image_scale = 100
    im = Image.new(
        "RGB",
        (
            image_scale * (max([table[0] for table in physical_tables]) + 1),
            image_scale * (max([table[1] for table in physical_tables]) + 1),
        ),
        (100, 100, 100),
    )
    draw = ImageDraw.Draw(im)
    draw_physical_tables(draw, image_scale, physical_tables)
    draw_tables(draw, image_scale, tables, show_names)
    if table is not None:
        draw.rectangle(
            (
                image_scale * table["coord"][0] + image_scale,
                image_scale * table["coord"][1] + image_scale,
                image_scale * (table["coord"][0] + 1) + image_scale,
                image_scale * (table["coord"][1] + 1) + image_scale,
            ),
            fill="#FE0102",
        )
    if not os.path.exists(os.path.join(__SOURCES, "images")):
        os.makedirs(os.path.join(__SOURCES, "images"))
    im.save(os.path.join(os.path.join(__SOURCES, "images"), path))


def get_distance(A, B):
    return math.sqrt(abs(A[0] - B[0]) ** 2 + abs(A[1] - B[1]) ** 2)


def load_tables():
    with open(os.path.join(__SOURCES, "tables.json"), "r") as f_i:
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
