"""Tasks related with the source code."""
import invoke


@invoke.task
def run(c):
    """Run pre-commit on all files."""
    c.run("pre-commit run --all-files", pty=True)
