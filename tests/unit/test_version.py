import subprocess
import sys

import pytest

from abusor.version import VERSION


@pytest.mark.skipif(
    sys.version_info < (3, 7), reason="capture_output is not supported in python 3.6"
)
def test_recorded_version_matches_git_tag():
    """Verify that we have the same version  in the package as in our git repository.

    This test tries to detect releases with an outdated version.
    """
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == VERSION
