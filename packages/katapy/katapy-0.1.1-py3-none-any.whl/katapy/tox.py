"""Tox tasks."""
import shutil
from pathlib import Path

import invoke

TOX_FILE = Path(__file__).parent / "tox.ini"


@invoke.task
def init(c):
    """Generate tox.ini file."""
    shutil.copy(TOX_FILE, Path.cwd() / "tox.ini")


@invoke.task
def run(c):
    """Run tox."""
    init(c)
    c.run("tox", pty=True)
