import time
import uuid
from datetime import datetime, timezone

from .models import Operation, OperationRequest, OperationResult, HistoryEntry
from .storage import FileStorage


class CalculatorService:
    def __init__(self, storage: FileStorage):
        self.storage = storage

    def calculate(self, raw_a, raw_b, raw_operation) -> OperationResult:
        try:
            a = float(raw_a)
        except (TypeError, ValueError):
            raise ValueError("'a' must be a number")

        try:
            b = float(raw_b)
        except (TypeError, ValueError):
            raise ValueError("'b' must be a number")

        try:
            operation = Operation(raw_operation)
        except ValueError:
            valid = ", ".join(op.value for op in Operation)
            raise ValueError(f"Invalid operation '{raw_operation}'. Valid: {valid}")

        if operation == Operation.DIVIDE and b == 0:
            raise ZeroDivisionError("Cannot divide by zero")

        start = time.perf_counter()
        match operation:
            case Operation.SUM:
                result = a + b
            case Operation.SUBTRACT:
                result = a - b
            case Operation.MULTIPLY:
                result = a * b
            case Operation.DIVIDE:
                result = a / b
        duration_ms = (time.perf_counter() - start) * 1000

        entry = HistoryEntry(
            id=str(uuid.uuid4()),
            a=a,
            b=b,
            operation=operation.value,
            result=result,
            duration_ms=round(duration_ms, 4),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.storage.save(entry)

        return OperationResult(
            a=a,
            b=b,
            operation=operation,
            result=result,
            duration_ms=entry.duration_ms,
        )

    def get_history(self) -> list[HistoryEntry]:
        return self.storage.load_all()

    def about(self) -> dict:
        return {
            "name": "Calculator API",
            "version": "1.0.0",
            "description": "A simple calculator backend with history tracking.",
            "operations": [op.value for op in Operation],
            "endpoints": {
                "POST /calculate": "Perform a calculation",
                "GET /history": "Retrieve all past calculations",
                "GET /about": "Info about this API",
            },
        }
