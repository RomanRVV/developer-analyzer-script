import pytest
from reports import PerformanceReport, BaseReport

CORRECT_ROW = {
    "name": "David Chen",
    "position": "QA",
    "completed_tasks": "36",
    "performance": "4.6",
    "skills": "Swift, Kotlin, React Native, iOS",
    "team": "Mobile Team",
    "experience_years": "3"
}


def test_process_correct_row() -> None:
    report = PerformanceReport()
    report.process_row(CORRECT_ROW)

    assert "QA" in report.performance_by_position
    assert report.performance_by_position["QA"] == [4.6]


@pytest.mark.parametrize("missing_key", [
    "position",
    "performance",
])
def test_process_row_missing_required_key(missing_key: str) -> None:
    report = PerformanceReport()
    incomplete_row = CORRECT_ROW.copy()
    del incomplete_row[missing_key]

    with pytest.raises(KeyError):
        report.process_row(incomplete_row)


@pytest.mark.parametrize("invalid_performance", [
    "not_a_number",
    "abc",
    "12.34.56",
    "",
])
def test_process_row_invalid_performance(invalid_performance: str) -> None:
    report = PerformanceReport()
    row = CORRECT_ROW.copy()
    row["performance"] = invalid_performance

    with pytest.raises(ValueError):
        report.process_row(row)


def test_render_correct_row() -> None:
    report = PerformanceReport()
    new_row = CORRECT_ROW.copy()
    new_row["performance"] = "5.6"

    report.process_row(CORRECT_ROW)
    report.process_row(new_row)
    avg_perf = "5.1"

    result = report.render()

    assert "QA" in result
    assert avg_perf in result


def test_cannot_instantiate_base_report() -> None:
    with pytest.raises(TypeError):
        BaseReport()    # type: ignore[abstract]
