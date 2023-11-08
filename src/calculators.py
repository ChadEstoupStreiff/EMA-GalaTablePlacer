import streamlit as st


def transform_to_tables(entries):
    def find_friends(key, entries):
        friends = []
        for i in range(len(entries)):
            if (
                entries["Code table"][i] == key
                and entries["Code table ami"][i] != "NOTABLE"
                and entries["Code table ami"][i] not in friends
                and entries["Code table ami"][i] in list(entries["Code table"])
            ):
                friends.append(entries["Code table ami"][i])
        return friends

    values = entries["Code table"].value_counts()
    return [
        {
            "id": f"T{i}",
            "size": int(values[key]),
            "codes": [(key, values[key])],
            "friends": find_friends(key, entries),
        }
        for i, key in enumerate(values.keys())
    ]


def split_tables(tables, table_size: int):
    tables_new = []
    for table in tables:
        if table["size"] > table_size:
            n = int(table["size"] / table_size)
            for _ in range(n):
                tables_new.append(
                    {
                        "id": f"T{len(tables_new) + 1}",
                        "size": table_size,
                        "codes": [[table["codes"][0][0], int(table_size)]],
                        "friends": table["friends"],
                    }
                )
            if int(table["size"] % table_size) > 0:
                tables_new.append(
                    {
                        "id": f"T{len(tables_new) + 1}",
                        "size": int(table["size"] % table_size),
                        "codes": [
                            [table["codes"][0][0], int(table["size"] % table_size)]
                        ],
                        "friends": table["friends"],
                    }
                )
        else:
            tables_new.append(
                {
                    "id": f"T{len(tables_new) + 1}",
                    "size": table["size"],
                    "codes": [[table["codes"][0][0], int(table["codes"][0][1])]],
                    "friends": table["friends"],
                }
            )
    return sorted(tables_new, key=lambda x: x["size"], reverse=True)


def merge_tables(tables, table_size: int):
    tables_new = []

    while len(tables) > 0:
        biggest = tables[0]
        del tables[0]
        if biggest["size"] >= table_size:
            tables_new.append(
                {
                    "id": f"T{len(tables_new) + 1}",
                    "size": biggest["size"],
                    "codes": biggest["codes"],
                    "friends": biggest["friends"],
                }
            )

        else:
            all = [biggest]

            has_found = True
            while has_found:
                has_found = False
                for i, table in enumerate(tables):
                    if (
                        sum([table_all["size"] for table_all in all]) + table["size"]
                        <= table_size
                    ):
                        all.append(table)
                        del tables[i]
                        has_found = True
                        break

            tables_new.append(
                {
                    "id": f"T{len(tables_new) + 1}",
                    "size": sum([table_all["size"] for table_all in all]),
                    "codes": [table_all["codes"][0] for table_all in all],
                    "friends": list(
                        set(
                            [
                                friend
                                for table_all in all
                                for friend in table_all["friends"]
                            ]
                        )
                    ),
                }
            )

    return sorted(tables_new, key=lambda x: x["size"], reverse=True)


def place_people(tables, entries):
    for table in tables:
        for code in table["codes"]:
            code.append([None] * code[1])
    for i in range(len(entries)):
        has_been_placed = False
        for table in tables:
            for code in table["codes"]:
                if code[0] == entries["Code table"][i]:
                    for y in range(code[1]):
                        if code[2][y] is None:
                            code[2][y] = f"{entries['Prénom'][i]} {entries['Nom'][i]}"
                            has_been_placed = True
                            break
                if has_been_placed:
                    break
            if has_been_placed:
                break
    return tables


def solve_placement(entries, table_size: int = 10):
    with st.spinner("Setup algorithme"):
        tables = transform_to_tables(entries)
        tables = split_tables(tables, table_size)
        tables = merge_tables(tables, table_size)
        tables = place_people(tables, entries)
    return tables