import streamlit as st
from loaders.excels import process_excel
from calculators.basic import solve_placement


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
        st.session_state.file_processed = None
        st.session_state.result = None

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


def main():

    with st.sidebar:
        sidebar_top = st.container()
        st.divider()
        sidebar_bottom = st.container()

    file = sidebar_top.file_uploader("Upload EXCEL file", type=["xlsx"], on_change=file_changed)

    if st.session_state.file_changed:
        st.session_state.file_changed = False
        st.session_state.file_processed = None
        st.session_state.result = None
        if file:
            with sidebar_bottom:
                with st.spinner("loading file"):
                    st.session_state.file_processed = process_excel(file)
            sidebar_bottom.success("File loaded")



    if st.session_state.result is not None:
        sidebar_bottom.success("Table placement solved")
        with st.expander("Result", expanded=True):
            st.write(st.session_state.result)
            sidebar_top.download_button("Download results", str(st.session_state.result), file_name="tables.xlsx", use_container_width=True)

    if st.session_state.file_processed is not None:
        with st.expander("Excel Entries", expanded=(st.session_state.result is None)):
            file_edited = st.data_editor(
                st.session_state.file_processed,
                column_config={
                    "Identifier": "Identifier",
                    "Selected": st.column_config.CheckboxColumn(label="Selected"),
                },
                disabled=["Identifier"],
                hide_index=True,
                use_container_width=True,
            )

        if sidebar_top.button("Generate table placement", use_container_width=True):
            with sidebar_bottom:
                with st.spinner("Solving placement"):
                    st.session_state.result = solve_placement(file_edited)
            st.experimental_rerun()
    else:
        st.error("Please load a file")

if __name__ == "__main__":
    setup()
    main()