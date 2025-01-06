def align_row_elements():
    return """
        div.stButton > button {
            border: none;
            background: transparent;
            padding: 0;
            margin: 0;
        }
        div.stSelectbox {
            margin-top: -10px;
        }
        div.stSelectbox > div[role="button"] {
            background: transparent;
            border: none;
            padding: 0;
        }
        div.stSelectbox > div {
            min-width: 150px;
            max-width: 150px;
        }
    """
