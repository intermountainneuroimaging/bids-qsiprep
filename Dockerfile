FROM pennbbl/qsiprep:0.15.4 as base
# the qsiprep image is huge (11.6 GB), so the GitLab CI tests fail to even
# download it with the error: "no space left on device".
# To create the main functionality of the gear, just comment out the previous "FROM" line
# and uncomment this line (to use a vanilla Python):
#FROM python:3.8.10-slim-buster as base

LABEL maintainer="support@flywheel.io"

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Dev install. git for pip editable install.
RUN pip install --no-cache-dir "poetry==1.1.13" && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry install --no-dev

# Installing the current project (most likely to change, above layer can be cached)
# Note: poetry requires a README.md to install the current project
COPY ./ $FLYWHEEL/
RUN poetry install --no-dev

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["poetry","run","python","/flywheel/v0/run.py"]
