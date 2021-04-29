
import atexit
import sys
from typing import Any, Callable, Dict, List, Tuple, Type, Union

class Check:
    """Represents a module and a way to check that it was imported
    
    A check has a `name` and associated callable predicate `pred`.  The name
    doesn't have to be the actual name of the module you want to check for,
    though that's the most obvious thing to do.  The predicate should accept a
    `dict` and somehow inspect it for a sign that the module was imported.

    It is intended the that `dict` being passed is `sys.modules` but for testing
    purposes something else could be used.
    """

    def __init__(self, name: str, pred: Callable) -> None:
        self.name = name
        self.pred = pred

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __call__(self, sys_modules: Dict) -> bool:
        return self.pred(sys_modules)


class Inspector:
    """Contains and executes a series of import checks"""

    def __init__(self, checks: List[Check]) -> None:
        self.checks = checks

    def __call__(self, sys_modules: Dict) -> List[str]:
        return [check.name for check in self.checks if check(sys_modules)]


class Reporter:
    """Takes some action given a list of imported module names
    
    As the name implies, `Reporter` objects should probably report that modules
    have been imported.  Exactly how the reporting is done depends on what the
    user wants.  Text?  JSON?  Pickle?  POST to some endpoint?  Do nothing?

    Some reference `Reporter` implementations are included in the
    `customs.reporters` module.
    """

    def __call__(self, imports: List[str]) -> None:
        raise NotImplementedError


def register_exit_hook(modules: List[Union[str, Tuple[str, Callable]]],
        reporter_cls: Type[Reporter],
        *args: Any,
        **kwargs: Any) -> None:
    """Construct and register an import inspection and report exit hook

    This is really the only function most people should need to call from this
    module.  It takes a list of module specifications, the type of `Reporter`
    desired, and any positional or keyword arguments needed to instantiate the
    `Reporter` object.

    The module specification should be a `list` consisting of string or tuple
    objects.  String elements will be used to construct `Check` objects that
    simply verify that the string is found in `sys.modules`.  Tuple elements
    will be used to construct `Check` objects using the first element as the
    check name and the second as the check predicate.  Here's an example:

        modules = [
            "numpy",
            ("root", lambda sys_modules: "ROOT.std" in sys_modules),
            "tqdm"
        ]

    the first and laste elements signify that we want to use the default
    predicate for NumPy and TQDM (e.g. return `"numpy" in sys_modules`).  The
    second element looks for a different name (a side effect of how ROOT is
    imported).  In this case, if it's true then the `Inspector` will emit that
    "root" (and not "ROOT.std") was imported.

    Note!  If a module specification is neither a string or tuple it will be
    discarded silently.
    """
    def exit_hook():
        inspector = Inspector(create_checks(modules))
        reporter = reporter_cls(*args, **kwargs)
        reporter(inspector(sys.modules))
    atexit.register(exit_hook)


def create_checks(modules: List[Union[str, Tuple[str, Callable]]]) -> List[Check]:
    """Convert module list to a list of checks

    Note!  If the module specification is of the wrong type it is discarded
    silently and `None` is returned.
    """

    checks = set([create_check(module) for module in modules]) 

    checks.discard(None)
    return sorted(list(checks), key=lambda c: c.name)


def create_check(module: Union[str, Tuple[str, Callable]]) -> Union[Check, None]:
    """Convert a module specification into a `Check` object

    Note!  If the module specification is of the wrong type it is discarded
    silently and `None` is returned.
    """
    if isinstance(module, tuple):
        return Check(*module)
    elif isinstance(module, str):
        return Check(module, lambda sys_modules: module in sys_modules)
    else:
        return None
