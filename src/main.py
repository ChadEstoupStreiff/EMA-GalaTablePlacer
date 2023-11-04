import streamlit as st
from loaders.excels import process_excel
from calculators.basic import solve_placement
import statistics
import json


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
                st.subheader(f"Table {table['id']}")
                st.json(table, expanded=False)
                return


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
        st.session_state.result = json.loads(result_file.getvalue().decode("utf-8"))
        sidebar_bottom.success("Result Loaded")

    top = st.container()
    if st.session_state.file_processed is not None:
        with st.expander("Excel Entries"):
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

                calculate_button = st.form_submit_button(
                    "Calculate table placement", use_container_width=True
                )
        if calculate_button:
            with sidebar_bottom:
                st.session_state.result = solve_placement(
                    file_edited, table_size=table_size
                )
            sidebar_bottom.success("Table placement solved")
    else:
        st.error("Please load a file")

    if st.session_state.result is not None:
        with top:
            cols = st.columns([1, 1, 1, 1])
            with cols[0]:
                st.metric("Number of tables", len(st.session_state.result))
            with cols[1]:
                st.metric(
                    "Minimum size",
                    min([table["size"] for table in st.session_state.result]),
                )
            with cols[2]:
                st.metric(
                    "Average size",
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
                    "Median size",
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
                    "Numner of seats",
                    sum([table["size"] for table in st.session_state.result]),
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

            st.divider()
            people_searcher()

            if sidebar_top.checkbox("Show JSONs"):
                st.divider()
                st.subheader("Tables JSON")
                st.json(
                    st.session_state.result,
                    expanded=True,
                )

            sidebar_top.download_button(
                "Download results",
                json.dumps(st.session_state.result),
                file_name="tables.json",
                use_container_width=True,
            )

            st.divider()


if __name__ == "__main__":
    setup()
    main()
