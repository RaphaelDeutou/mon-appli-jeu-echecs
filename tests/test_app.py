from streamlit.testing.v1 import AppTest


def test_streamlit_demarre():
    at = AppTest.from_file("../fil_rouge/app_streamlit.py", default_timeout=30).run()
    assert not at.exception
