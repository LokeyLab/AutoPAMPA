import pytest
import sys
import doubles
from pathlib import Path
outpath = Path("./tests/outputs")
default_args = [
    "autopampa",
    "./tests/inputs/test_job.xlsx",
    "-g",
    "-u",
    "-o",
    "./tests/outputs",
]

def test_runs():
    these_args = default_args.copy()
    doubles.patch("sys.argv", these_args)
    from autopampa.cli.main import main
    # main()
    # assert outpath.exists()
    # outpath.unlink()