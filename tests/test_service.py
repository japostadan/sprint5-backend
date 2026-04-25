import pytest
from calculator.service import CalculatorService
from calculator.storage import FileStorage
from calculator.models import Operation


@pytest.fixture
def service(tmp_path):
    storage = FileStorage(str(tmp_path / "history.json"))
    return CalculatorService(storage)


def test_sum(service):
    result = service.calculate(3, 4, "sum")
    assert result.result == 7.0
    assert result.operation == Operation.SUM


def test_subtract(service):
    result = service.calculate(10, 4, "subtract")
    assert result.result == 6.0


def test_multiply(service):
    result = service.calculate(3, 5, "multiply")
    assert result.result == 15.0


def test_divide(service):
    result = service.calculate(10, 2, "divide")
    assert result.result == 5.0


def test_divide_by_zero(service):
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        service.calculate(10, 0, "divide")


def test_divide_by_float_zero(service):
    with pytest.raises(ZeroDivisionError):
        service.calculate(10, 0.0, "divide")


def test_invalid_a(service):
    with pytest.raises(ValueError, match="'a' must be a number"):
        service.calculate("hello", 5, "sum")


def test_invalid_b(service):
    with pytest.raises(ValueError, match="'b' must be a number"):
        service.calculate(5, "world", "sum")


def test_invalid_operation(service):
    with pytest.raises(ValueError, match="Invalid operation"):
        service.calculate(5, 3, "modulo")


def test_result_stored_in_history(service):
    service.calculate(2, 3, "sum")
    history = service.get_history()
    assert len(history) == 1
    assert history[0].result == 5.0


def test_history_preserves_order(service):
    service.calculate(1, 1, "sum")
    service.calculate(2, 2, "multiply")
    history = service.get_history()
    assert history[0].operation == "sum"
    assert history[1].operation == "multiply"


def test_duration_ms_is_positive(service):
    result = service.calculate(10, 5, "divide")
    assert result.duration_ms > 0


def test_about_returns_dict(service):
    info = service.about()
    assert "name" in info
    assert "operations" in info
    assert "sum" in info["operations"]
