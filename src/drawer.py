from PIL import Image, ImageDraw, ImageFont
import os

from config import __SOURCES


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
            fnt = ImageFont.truetype(os.path.join(__SOURCES, "assets/font.ttf"), 40)
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
            image_scale * (max([table[0] for table in physical_tables]) + 3),
            image_scale * (max([table[1] for table in physical_tables]) + 3),
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
