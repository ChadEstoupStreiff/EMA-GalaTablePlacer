import streamlit as st


def setup():
    st.set_page_config(
        page_title="EMA - GalaTablePlace",
        page_icon="random",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    if len(st.session_state == 0):
        st.session_state.file_changed = False

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

    file = st.file_uploader("Upload EXCEL file", on_change=file_changed)

    if st.session_state.file_changed:
        st.session_state.file_changed = False
        if file:
            pass

if __name__ == "__main__":
    setup()
    main()