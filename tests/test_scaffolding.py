import sys

import stress_dw


def test_package_imports_on_the_declared_python_floor() -> None:
    assert sys.version_info >= (3, 12)
    assert stress_dw.__doc__
