
import json
import pickle
import uuid

import pytest

import customs.reporters as cr

def test_print_reporter(capsys):
    r = cr.PrintReporter()
    imports = ["a", "b", "c"]
    r(imports)
    captured = capsys.readouterr()
    assert captured.out == f"{imports}\n"

def test_file_reporter_init_fail():
    with pytest.raises(NotImplementedError):
        r = cr.FileReporter()

def test_pickle_reporter_default_path_name():
    r = cr.PickleReporter()
    name = r.path.name
    assert(name.startswith("customs-"))
    assert(name.endswith(".pkl"))
    assert(uuid.UUID(name[8:-4], version=4).hex == name[8:-4])

def test_pickle_reporter(tmp_path_factory):
    path = tmp_path_factory.mktemp("pickle") / "tmp.pkl"
    r = cr.PickleReporter(path)
    imports = ["a", "b", "c"]
    r(imports)
    with open(path, "rb") as stream:
        results = pickle.load(stream)
    for l, r in zip(imports, results):
        assert(l == r)

def test_text_file_reporter_default_path_name():
    r = cr.TextFileReporter()
    name = r.path.name
    assert(name.startswith("customs-"))
    assert(name.endswith(".txt"))
    assert(uuid.UUID(name[8:-4], version=4).hex == name[8:-4])

def test_text_file_reporter(tmp_path_factory):
    path = tmp_path_factory.mktemp("text_file") / "tmp.txt"
    r = cr.TextFileReporter(path)
    imports = ["a", "b", "c"]
    r(imports)
    with open(path, "r") as stream:
        for i, line in enumerate(stream):
            assert(line.strip() == imports[i])

def test_json_file_reporter_default_path_name():
    r = cr.JSONFileReporter()
    name = r.path.name
    assert(name.startswith("customs-"))
    assert(name.endswith(".json"))
    assert(uuid.UUID(name[8:-5], version=4).hex == name[8:-5])

def test_json_file_reporter(tmp_path_factory):
    path = tmp_path_factory.mktemp("json_file") / "tmp.json"
    r = cr.JSONFileReporter(path)
    imports = ["a", "b", "c"]
    r(imports)
    with open(path, "r") as stream:
        results = json.load(stream)
    for l, r in zip(imports, results):
        assert(l == r)
