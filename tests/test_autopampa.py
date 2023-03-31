import pytest
import sys
import shutil
import doubles
from pathlib import Path
outstr = "./tests/outputs/test"
outpath = Path(outstr)
default_args = [
    "autopampa",
    "./tests/inputs/test_job.xlsx",
    "-g",
    "-u",
    "-o",
    outstr,
]

def test_runs():
    these_args = default_args.copy()
    doubles.patch("sys.argv", these_args)
    from autopampa.cli.main import main
    main()
    assert (outpath.parent / "test_Out.xlsx").exists()
    assert (outpath.parent / "test_Results.xlsx").exists()
    assert (outpath.parent / "test_I1").exists()
    assert (outpath.parent / "test_R1").exists()
    assert (outpath.parent / "test_P1").exists()
    (outpath.parent / "test_Out.xlsx").unlink()
    (outpath.parent / "test_Results.xlsx").unlink()
    shutil.rmtree((outpath.parent / "test_I1"))
    shutil.rmtree((outpath.parent / "test_P1"))
    shutil.rmtree((outpath.parent / "test_R1"))