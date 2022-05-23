# the qsiprep image is huge (11.6 GB), so the GitLab CI tests fail to even
# download it with the error: "no space left on device".
# For now I'm going to use a vanilla Python, so that I can push commits.
#FROM pennbbl/qsiprep:0.15.1 as base
FROM python:3.8.10-slim-buster as base

LABEL maintainer="support@flywheel.io"

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Dev install. git for pip editable install.
# hadolint ignore=DL3008
RUN apt-get update && apt-get install --no-install-recommends -y git && \
    apt-get clean && \
    pip install --no-cache-dir "poetry==1.1.2" && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry install --no-dev

# Installing the current project (most likely to change, above layer can be cached)
# Note: poetry requires a README.md to install the current project
COPY run.py manifest.json README.md $FLYWHEEL/
COPY fw_gear_bids_qsiprep $FLYWHEEL/fw_gear_bids_qsiprep
COPY utils $FLYWHEEL/utils
RUN poetry install --no-dev

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["poetry","run","python","/flywheel/v0/run.py"]
