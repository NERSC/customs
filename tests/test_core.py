
import subprocess
from textwrap import dedent

import pytest

from customs.core import Check, Inspector, Reporter, create_checks, create_check

def test_check_init():
    name = "a"
    pred = lambda d: name in d
    check = Check(name, pred)
    assert(check.name == name)
    assert(check.pred == pred)

def test_check_true():
    name = "a"
    pred = lambda d: name in d
    check = Check(name, pred)
    d = {name: 1}
    assert(check(d) == True)

def test_check_false():
    name = "b"
    pred = lambda d: name in d
    check = Check(name, pred)
    d = {"a": 1}
    assert(check(d) == False)

def test_inspector_init():
    names = "a b c d".split()
    checks = list()
    for name in names:
        checks.append(Check(name, lambda d: name in d))
    inspector = Inspector(checks)
    assert(inspector.checks == checks)

def test_inspector_call_hit():
    names = "a b".split()
    make_pred = lambda name: lambda d: name in d
    checks = list()
    for name in names:
        checks.append(Check(name, make_pred(name)))
    inspector = Inspector(checks)
    d = {names[0]: 1}
    imports = inspector(d)
    assert(imports[0] == names[0])

def test_inspector_call_miss():
    names = "a b".split()
    make_pred = lambda name: lambda d: name in d
    checks = list()
    for name in names:
        checks.append(Check(name, make_pred(name)))
    inspector = Inspector(checks)
    d = {"c": 1}
    imports = inspector(d)
    assert(not imports)

def test_reporter_call_fail():
    r = Reporter()
    with pytest.raises(NotImplementedError):
        r([])

def test_exit_hook_hit():
    script = dedent("""
    import customs
    from customs.reporters import PrintReporter as Reporter
    customs.register_exit_hook(["pip"], Reporter)
    import pip""")
    p = subprocess.run(["python"], input=script, capture_output=True, text=True)
    assert(p.stdout == "['pip']\n")

def test_exit_hook_miss():
    script = dedent("""
    import customs
    from customs.reporters import PrintReporter as Reporter
    customs.register_exit_hook(["pip"], Reporter)""")
    p = subprocess.run(["python"], input=script, capture_output=True, text=True)
    assert(p.stdout == "[]\n")

def test_create_checks():
    modules = ["a", ("b", lambda d: "b" in d), 32]
    checks = create_checks(modules)
    assert(checks[0].name == "a")
    assert(checks[1].name == "b")
    assert(len(checks) == 2)
    assert(checks[0]({"a":1}) == True)
    assert(checks[0]({"b":1}) == False)
    assert(checks[1]({"a":1}) == False)
    assert(checks[1]({"b":1}) == True)

def test_duplicate_modules():
    modules = ["a", "a", "b"]
    checks = create_checks(modules)
    assert(len(checks) == 2)

def test_create_check_str():
    check = create_check("a")
    assert(check({"a":1}) == True)
    assert(check({"b":1}) == False)

def test_create_check_tuple():
    check = create_check(("a", lambda d: "a" in d))
    assert(check({"a":1}) == True)
    assert(check({"b":1}) == False)

def test_create_check_wrong():
    assert(create_check(32) is None)
