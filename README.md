
# :passport_control: customs

![workflow](https://github.com/NERSC/customs/actions/workflows/tests.yml/badge.svg)

Inspect and report Python packages of interest

This helps you learn about what modules and packages are imported by Python processes when your code runs.
It provides a way to specify a list of modules to watch for and mechanisms for reporting their detection.
The main way this reporting happens is through the use of `atexit` hooks, created by the `register_exit_hook` function.
When the code exits (normally) the modules are detected by inspecting `sys.modules` and then reported in a manner of your choosing.
Aggressive stoppage of your code will prevent the reporting from happening.
Read the `atexit` documentation for more detail.

## Example

Say you are interested in knowing when NumPy, SciPy are imported.
Assume you're also interested in ROOT which doesn't actually show up in `sys.modules` as ROOT but rather as ROOT.std.
This block of code lets you do that:

    import customs
    from customs.reporters import TextFileReporter as Reporter
    modules = [
        "numpy",
        "scipy",
        ("root", lambda sys_modules: "ROOT.std" in sys_modules)
    ]
    customs.register_exit_hook(modules, Reporter)

You can put that anywhere and when the code exits you'll get a file listing which of those modules were actually imported.

The list of modules can contain strings or tuples.
If a module is listed as a string, we just check for its presence in `sys.modules` at exit time.
If it's a tuple, the first argument of the tuple is used as a name, but the second argument is a check predicate.
The check predicate should take a dictionary (probably `sys.modules`) and return True or False.
In this case, we have to look for ROOT.std, but we report that "root" was imported if it is detected.

You can call the `register_exit_hook` function as many times as you like.
You can use this to vary what modules are reported to what reporter.
You can even use this have multiple reporters report on the same list of modules to different destinations.
It's up to you.

## Using with `sitecustomize.py`

When Python starts up normally it looks for a script called `sitecustomize.py` in `sys.path` and runs it.
You can exploit this feature to report on imports detected by any script using a particular Python interpreter.
With suitable configuration of your system, you can capture quite a bit of info.

# References

* [C. Maclean, *Python Usage Metrics on Blue Waters*, Cray User Group 2017, Redmond, Washington](https://cug.org/proceedings/cug2017_proceedings/includes/files/pap163s2-file1.pdf)
* R. Thomas, L. Stephey, A. Greiner, B. Cook, *Monitoring Scientific Python Usage on a Supercomputer*, SciPy 2021, Austin Texas, *accepted*
