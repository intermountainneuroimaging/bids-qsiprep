"""Run this instead of running actual command"""

import logging
import os
from pathlib import Path
from typing import List, Union

log = logging.getLogger(__name__)


def make_dirs_and_files(files: List[Union[str, Path]]) -> None:
    """Create directories and touch files.

    Args:
        files: paths to files to be created
    """
    for ff in files:
        if not isinstance(ff, str):
            ff = str(ff)

        if os.path.exists(ff):
            log.debug("Exists: " + ff)
        else:
            log.debug("Creating: " + ff)
            dir_name = os.path.dirname(ff)
            os.makedirs(dir_name)
            Path(ff).touch(mode=0o777, exist_ok=True)


def pretend_it_ran(destination_id: str) -> None:
    """Make some output like the command would have done only fake.

    Args:
        destination_id (str) ID of destination container
    """

    path = Path("work")

    log.info("Creating fake output in " + str(path))

    files = [
        path / "somedir" / "d3.js",
        path
        / "reportlets"
        / "somecmd"
        / "sub-TOME3024"
        / "anat"
        / "sub-TOME3024_desc-about_T1w.html",
    ]

    make_dirs_and_files(files)

    # Output directory
    path = Path("output") / Path(destination_id)

    log.info("Creating fake output in " + str(path))

    files = [
        path / "somedir" / "logs" / "CITATION.md",
        path
        / "somedir"
        / "sub-TOME3024"
        / "anat"
        / "sub-TOME3024_acq-MPR_from-orig_to-T1w_mode-image_xfm.txt",
        path / "freesurfer" / "fsaverage" / "mri" / "subcort.prob.log",
    ]

    make_dirs_and_files(files)

    html = """<html>
    <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>sub-TOME3024</title>
    </head>
    <body>
    <h1>sub-TOME3024</h1>
    <p>This is a test html file.&nbsp; How do you love it?<br>
    </p>
    </body>
    </html>"""

    ff = path / "somedir" / "sub-TOME3024.html"
    with open(ff, "w") as fp:
        fp.write(html)
    log.debug("Creating: " + str(ff))
