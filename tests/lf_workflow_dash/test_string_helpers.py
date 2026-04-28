from lf_workflow_dash.string_helpers import get_conclusion_time


def test_get_conclusion_time():
    time, stale = get_conclusion_time({"updated_at": "2024-09-23T06:52:27Z"})
    assert stale
    assert time == "02:52<br>09/23/24"
