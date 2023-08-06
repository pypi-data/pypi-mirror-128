"""Provides tasks."""
from invoke import Collection, task

from katapy import precommit, tox


@task
def check(c):
    """Check implementation."""
    precommit.run(c)
    tox.run(c)


ns = Collection(
    check,
    precommit,
    tox,
)
