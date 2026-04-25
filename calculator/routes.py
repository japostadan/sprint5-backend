from flask import Blueprint, request, jsonify

from .service import CalculatorService
from .storage import FileStorage

bp = Blueprint("calculator", __name__)


def get_service() -> CalculatorService:
    return CalculatorService(FileStorage("history.json"))


@bp.post("/calculate")
def calculate():
    data = request.get_json(silent=True) or {}
    try:
        result = get_service().calculate(
            data.get("a"),
            data.get("b"),
            data.get("operation"),
        )
        return jsonify({
            "a": result.a,
            "b": result.b,
            "operation": result.operation.value,
            "result": result.result,
            "duration_ms": result.duration_ms,
        }), 200
    except ZeroDivisionError as e:
        return jsonify({"error": str(e)}), 422
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.get("/history")
def history():
    entries = get_service().get_history()
    return jsonify([
        {
            "id": e.id,
            "a": e.a,
            "b": e.b,
            "operation": e.operation,
            "result": e.result,
            "duration_ms": e.duration_ms,
            "timestamp": e.timestamp,
        }
        for e in entries
    ]), 200


@bp.get("/about")
def about():
    return jsonify(get_service().about()), 200
