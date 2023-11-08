import streamlit as st
from loaders import process_excel
from calculators import solve_placement
import statistics
import json
import os
from tables import load_tables, get_solution, draw_solution


__SOURCES = "/app"

def metrics():
    cols = st.columns([1, 1, 1, 1])
    with cols[0]:
        st.metric("Number of tables", len(st.session_state.result))
    with cols[1]:
        st.metric(
            "Minimum table size",
            min([table["size"] for table in st.session_state.result]),
        )
    with cols[2]:
        st.metric(
            "Average table size",
            int(
                statistics.mean(
                    [float(table["size"]) for table in st.session_state.result]
                )
                * 1000
            )
            / 1000,
        )
    with cols[3]:
        st.metric(
            "Median table size",
            int(
                statistics.median(
                    [float(table["size"]) for table in st.session_state.result]
                )
                * 1000
            )
            / 1000,
        )

    cols = st.columns([1, 1, 1, 1])
    with cols[0]:
        st.metric(
            "Solution score",
            st.session_state.score,
        )
    with cols[1]:
        st.metric(
            "Maximum nbr of friends",
            max([len(table["friends"]) for table in st.session_state.result]),
        )
    with cols[2]:
        st.metric(
            "Average number of friends",
            int(
                statistics.mean(
                    [len(table["friends"]) for table in st.session_state.result]
                )
                * 1000
            )
            / 1000,
        )
    with cols[3]:
        st.metric(
            "Median number of friends",
            int(
                statistics.median(
                    [len(table["friends"]) for table in st.session_state.result]
                )
                * 1000
            )
            / 1000,
        )


def people_searcher():
    person = st.selectbox(
        "Person",
        [
            person
            for table in st.session_state.result
            for code in table["codes"]
            for person in code[2]
        ],
    )

    for table in st.session_state.result:
        for code in table["codes"]:
            if person in code[2]:
                show_table(table)
                return


def table_searcher():
    table_id = st.selectbox(
        "Table",
        [table["id"] for table in st.session_state.result],
    )

    for table in st.session_state.result:
        if table["id"] == table_id:
            show_table(table)
            return


def show_table(table, expanded=True):
    draw_solution(st.session_state.result, st.session_state.physical_tables, table=table, path="table.png")
    with st.expander(f"Table {table['id']}", expanded=expanded):
        st.markdown(f"## Table {table['id']} - {table['size']} seats")
        st.image(os.path.join(__SOURCES, "images/table.png"))
        st.markdown(f"#### Coordinates: {table['coord'][0]}, {table['coord'][1]}")
        st.markdown(f"#### {len(table['codes'])} code(s):")
        for code in table["codes"]:
            st.markdown(f"- {code[0]} - {code[1]} people")
            st.json(code[2])
        st.markdown(f"#### {len(table['friends'])} friend(s):")
        for friend in table["friends"]:
            st.markdown(f"- {friend}")


def setup():
    st.set_page_config(
        page_title="EMA - GalaTablePlace",
        page_icon="random",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    if len(st.session_state) == 0:
        st.session_state.file_changed = False
        st.session_state.result_file_changed = False
        st.session_state.file_processed = None
        st.session_state.result = None
        st.session_state.physical_tables = load_tables()

    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    style = f"""
    <style>
    footer:after {{
        content: "@ 2023, developped by Chad Estoup--Streiff, made with Streamlit";
        visibility: visible;
        display: block;
        text-align: center;
        position: relative;
        padding: 5px;
        top: 2px;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)


def file_changed():
    st.session_state.file_changed = True


def result_file_changed():
    st.session_state.result_file_changed = True


def main():
    with st.sidebar:
        sidebar_top = st.container()
        st.divider()
        sidebar_bottom = st.container()

    with sidebar_top.expander("Load result save", expanded=False):
        result_file = st.file_uploader(
            "Upload result file", type=["json"], on_change=result_file_changed
        )

    file = sidebar_top.file_uploader(
        "Upload EXCEL file", type=["xlsx"], on_change=file_changed
    )

    if st.session_state.file_changed:
        st.session_state.file_changed = False
        st.session_state.file_processed = None
        if file:
            st.session_state.result = None
            with sidebar_bottom:
                with st.spinner("loading file"):
                    st.session_state.file_processed = process_excel(file)
            sidebar_bottom.success("File loaded")

    if st.session_state.result_file_changed and result_file:
        st.session_state.result_file_changed = False
        save = json.loads(result_file.getvalue().decode("utf-8"))
        st.session_state.score = save[0]
        st.session_state.physical_tables = save[1]
        st.session_state.result = save[2]
        draw_solution(st.session_state.result, st.session_state.physical_tables, path="solution.png", show_names=True)
        sidebar_bottom.success("Save Loaded")

    top = st.container()
    if st.session_state.file_processed is not None:
        with st.expander("Excel Entries", expanded=True):
            cols = st.columns([1, 1, 1, 1])

            file_edited = st.data_editor(
                st.session_state.file_processed,
                column_config={
                    "Identifier": "Identifier",
                    "Selected": st.column_config.CheckboxColumn(label="Selected"),
                },
                disabled=["Identifier"],
                use_container_width=True,
                height=700,
            )

            value_count = file_edited["Code table"].value_counts()

            with cols[0]:
                st.metric("Numbrr of entries", len(file_edited))
            with cols[1]:
                st.metric("Number of tables", file_edited["Code table"].nunique())
            with cols[2]:
                st.metric(
                    "Number of friend tables", file_edited["Code table ami"].nunique()
                )
            with cols[3]:
                st.metric(
                    f"Bigest table: {value_count.keys()[0]}",
                    str(file_edited["Code table"].value_counts()[0]) + " people",
                )

        with sidebar_top:
            with st.form("generate"):
                table_size = st.number_input("Size of a table", min_value=1, value=10)
                nbr_of_sol = st.number_input(
                    "number of solution to try", min_value=1, value=100000
                )

                calculate_button = st.form_submit_button(
                    "Calculate table placement", use_container_width=True
                )
        if calculate_button:
            with sidebar_bottom:
                st.session_state.result = solve_placement(
                    file_edited, table_size=table_size
                )
                st.session_state.result, st.session_state.score = get_solution(
                    st.session_state.result, st.session_state.physical_tables, nbr_of_sol
                )
                draw_solution(st.session_state.result, st.session_state.physical_tables, path="solution.png", show_names=True)
            sidebar_bottom.success("Table placement solved")
    else:
        if st.session_state.result is None:
            st.error("Please load a file")

    if st.session_state.result is not None:
        with top:
            st.image(os.path.join(__SOURCES, "images/solution.png"))

            if sidebar_top.checkbox("Show metrics", value=True):
                st.divider()
                metrics()

            if sidebar_top.checkbox("Show people and table search", value=True):
                st.divider()
                c1, c2 = st.columns([1, 1])
                with c1:
                    people_searcher()
                with c2:
                    table_searcher()

            if sidebar_top.checkbox("Show all Tables", value=False):
                st.divider()
                for i in range(int(len(st.session_state.result) / 3) + 1):
                    c1, c2, c3 = st.columns(3)
                    if i * 3 < len(st.session_state.result):
                        with c1:
                            show_table(st.session_state.result[i * 3], expanded=False)
                    if i * 3 + 1 < len(st.session_state.result):
                        with c2:
                            show_table(
                                st.session_state.result[i * 3 + 1], expanded=False
                            )
                    if i * 3 + 2 < len(st.session_state.result):
                        with c3:
                            show_table(
                                st.session_state.result[i * 3 + 2], expanded=False
                            )

            if sidebar_top.checkbox("Show raw JSONs"):
                st.divider()
                st.subheader("Tables JSON")
                st.json(
                    st.session_state.result,
                    expanded=True,
                )

            sidebar_top.download_button(
                "Download results",
                json.dumps([
                    st.session_state.score,
                    st.session_state.physical_tables,
                    st.session_state.result
                ]),
                file_name="tables.json",
                use_container_width=True,
            )


if __name__ == "__main__":
    setup()
    main()
