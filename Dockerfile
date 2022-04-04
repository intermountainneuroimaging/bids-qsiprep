# the qsiprep image is huge (11.6 GB), so the GitLab CI tests fail to even
# download it with the error: "no space left on device".
# For now I'm going to use a vanila Python, so that I can push commits.
#FROM pennbbl/qsiprep:0.15.1 as base
FROM python:3.8.10-slim-buster as base

LABEL maintainer="support@flywheel.io"

# Save docker environ here to keep it separate from the Flywheel gear environment
RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)'

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Dev install. git for pip editable install.
RUN apt-get update && apt-get install -y git && \
    pip install "poetry==1.1.2"

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry install --no-dev

# Installing the current project (most likely to change, above layer can be cached)
# Note: poetry requires a README.md to install the current project
COPY run.py manifest.json README.md $FLYWHEEL/
COPY fw_gear_bids_qsiprep $FLYWHEEL/fw_gear_bids_qsiprep
RUN poetry install --no-dev

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["poetry","run","python","/flywheel/v0/run.py"]
