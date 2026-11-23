"""Setup checks: prove the finsight package is installed and importable."""

from importlib.metadata import version
from pathlib import Path

import finsight


def test_package_imports():
    assert finsight.__doc__, "finsight package should have a docstring"


def test_package_is_installed():
    # Fails if pip has not installed the project into the active environment.
    assert version("finsight-ai") == "0.1.0"


def test_package_loads_from_src():
    # The src layout means the import must resolve to src/finsight/.
    package_dir = Path(finsight.__file__).resolve().parent
    assert package_dir.parent.name == "src"
