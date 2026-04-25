import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"HISTORY_FILE": str(tmp_path / "history.json"), "TESTING": True})
    with app.test_client() as client:
        yield client


def test_calculate_valid(client):
    res = client.post("/calculate", json={"a": 10, "b": 2, "operation": "divide"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["result"] == 5.0
    assert data["operation"] == "divide"


def test_calculate_all_operations(client):
    for op, a, b, expected in [
        ("sum", 3, 4, 7),
        ("subtract", 10, 3, 7),
        ("multiply", 3, 4, 12),
        ("divide", 10, 2, 5),
    ]:
        res = client.post("/calculate", json={"a": a, "b": b, "operation": op})
        assert res.status_code == 200
        assert res.get_json()["result"] == expected


def test_calculate_divide_by_zero(client):
    res = client.post("/calculate", json={"a": 10, "b": 0, "operation": "divide"})
    assert res.status_code == 422
    assert "Cannot divide by zero" in res.get_json()["error"]


def test_calculate_invalid_a(client):
    res = client.post("/calculate", json={"a": "hello", "b": 3, "operation": "sum"})
    assert res.status_code == 400
    assert "'a'" in res.get_json()["error"]


def test_calculate_unknown_operation(client):
    res = client.post("/calculate", json={"a": 5, "b": 3, "operation": "modulo"})
    assert res.status_code == 400


def test_calculate_missing_body(client):
    res = client.post("/calculate", content_type="application/json", data="")
    assert res.status_code == 400


def test_history_returns_list(client):
    client.post("/calculate", json={"a": 1, "b": 2, "operation": "sum"})
    res = client.get("/history")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_about_returns_200(client):
    res = client.get("/about")
    assert res.status_code == 200
    assert "operations" in res.get_json()
