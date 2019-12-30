import subprocess

from abusor.version import VERSION


def test_recorded_version_matches_git_tag():
    """Verify that we have the same version  in the package as in our git repository.

    This test tries to detect releases with an outdated version.
    """
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert result.stdout.strip() == VERSION
