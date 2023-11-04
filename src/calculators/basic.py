import streamlit as st


def transform_to_tables(entries):
    def find_friends(key, entries):
        friends = []
        for i in range(len(entries)):
            if entries["Code table"][i] == key:
                if entries["Code table ami"][i] not in friends:
                    friends.append(entries["Code table ami"][i])
        return friends

    values = entries["Code table"].value_counts()
    return [
        {
            "id": f"T{i}",
            "size": values[key],
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
                        "codes": [(table["codes"][0][0], int(table_size))],
                        "friends": table["friends"],
                    }
                )
            if int(table["size"] % table_size) > 0:
                tables_new.append(
                    {
                        "id": f"T{len(tables_new) + 1}",
                        "size": int(table["size"] % table_size),
                        "codes": [
                            (table["codes"][0][0], int(table["size"] % table_size))
                        ],
                        "friends": table["friends"],
                    }
                )
        else:
            tables_new.append(
                {
                    "id": f"T{len(tables_new) + 1}",
                    "size": table["size"],
                    "codes": [(table["codes"][0][0], int(table["codes"][0][1]))],
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
                    "friends": [
                        friend for table_all in all for friend in table_all["friends"]
                    ],
                }
            )

    return sorted(tables_new, key=lambda x: x["size"], reverse=True)


def solve_placement(entries, table_size: int = 10):
    with st.spinner("Casting to tables"):
        tables = transform_to_tables(entries)
    st.info("Tables casted")
    with st.spinner("Spliting tables"):
        tables = split_tables(tables, table_size)
    st.info("Tables splited")
    with st.spinner("Merging tables"):
        tables = merge_tables(tables, table_size)
    st.info("Tables merged")
    with st.spinner("Placing peoples"):
        pass
    st.info("People placed")
    return tables
