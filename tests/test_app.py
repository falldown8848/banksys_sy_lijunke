"""Streamlit 页面冒烟测试(关键路径,AppTest 无头执行)。

E2E 层只覆盖关键路径,不替代单元测试(见 standards/03 §1)。
"""

from streamlit.testing.v1 import AppTest

MAIN_PAGE = "app/main.py"
ANALYSIS_PAGE = "app/pages/1_data_analysis.py"


def _run(path: str) -> AppTest:
    at = AppTest.from_file(path, default_timeout=120)
    at.run()
    return at


def test_main_page_runs_without_exception():
    # Arrange / Act
    at = _run(MAIN_PAGE)

    # Assert:at.exception 为 ElementList,空列表表示无异常
    assert not at.exception


def test_analysis_page_runs_without_exception():
    # Arrange / Act
    at = _run(ANALYSIS_PAGE)

    # Assert:页面无异常,且渲染了概览指标
    assert not at.exception
    assert len(at.metric) >= 4
