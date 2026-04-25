import pytest
from calculator.models import Operation, OperationRequest, OperationResult, HistoryEntry


def test_operation_enum_values():
    assert Operation.SUM.value == "sum"
    assert Operation.SUBTRACT.value == "subtract"
    assert Operation.MULTIPLY.value == "multiply"
    assert Operation.DIVIDE.value == "divide"


def test_operation_lookup_by_value():
    assert Operation("sum") == Operation.SUM
    assert Operation("divide") == Operation.DIVIDE


def test_operation_invalid_value():
    with pytest.raises(ValueError):
        Operation("modulo")


def test_operation_all_members():
    values = [op.value for op in Operation]
    assert values == ["sum", "subtract", "multiply", "divide"]


def test_history_entry_fields():
    entry = HistoryEntry(
        id="abc",
        a=10.0,
        b=2.0,
        operation="divide",
        result=5.0,
        duration_ms=0.1,
        timestamp="2026-01-01T00:00:00+00:00",
    )
    assert entry.id == "abc"
    assert entry.result == 5.0
    assert entry.operation == "divide"


def test_operation_result_fields():
    result = OperationResult(a=3.0, b=4.0, operation=Operation.SUM, result=7.0, duration_ms=0.05)
    assert result.result == 7.0
    assert result.operation == Operation.SUM
