import pytest
from calculator.models import HistoryEntry
from calculator.storage import FileStorage


@pytest.fixture
def storage(tmp_path):
    return FileStorage(str(tmp_path / "history.json"))


def make_entry(**kwargs):
    defaults = dict(id="test-id", a=1.0, b=2.0, operation="sum", result=3.0, duration_ms=0.1, timestamp="2026-01-01T00:00:00+00:00")
    defaults.update(kwargs)
    return HistoryEntry(**defaults)


def test_creates_file_on_init(tmp_path):
    path = tmp_path / "history.json"
    assert not path.exists()
    FileStorage(str(path))
    assert path.exists()


def test_save_and_load(storage):
    entry = make_entry(id="e1", result=3.0)
    storage.save(entry)
    entries = storage.load_all()
    assert len(entries) == 1
    assert entries[0].id == "e1"
    assert entries[0].result == 3.0


def test_multiple_saves_preserve_order(storage):
    storage.save(make_entry(id="first"))
    storage.save(make_entry(id="second"))
    storage.save(make_entry(id="third"))
    ids = [e.id for e in storage.load_all()]
    assert ids == ["first", "second", "third"]


def test_clear_empties_history(storage):
    storage.save(make_entry())
    storage.clear()
    assert storage.load_all() == []


def test_load_returns_empty_on_missing_file(tmp_path):
    storage = FileStorage(str(tmp_path / "missing.json"))
    storage.clear()
    assert storage.load_all() == []


def test_load_returns_empty_on_corrupt_file(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("not valid json")
    storage = FileStorage(str(path))
    assert storage.load_all() == []


def test_schema_mismatch_uses_defaults(tmp_path):
    import json
    path = tmp_path / "history.json"
    path.write_text(json.dumps([{"id": "x", "result": 9.0}]))
    storage = FileStorage(str(path))
    entries = storage.load_all()
    assert entries[0].id == "x"
    assert entries[0].a == 0.0
    assert entries[0].operation == ""
