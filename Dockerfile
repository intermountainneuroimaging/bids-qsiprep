FROM pennbbl/qsiprep:0.15.4 as base
# the qsiprep image is huge (11.6 GB). To create the main functionality of the gear,
# just comment out the previous "FROM" line and uncomment this line (to use a vanilla
# Python):
#FROM python:3.8.10-slim-buster as base

LABEL maintainer="support@flywheel.io"

ENV HOME=/root/

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Install git to run pre-commit hooks inside container:
# (We need to rm cuda & nvidia sources because their keys are broken, and we don't
#  need to update them anyway)
RUN rm /etc/apt/sources.list.d/cuda.list \
       /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get update && \
    apt-get install --no-install-recommends -y git=1:2.17.1-1ubuntu0.12 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# install vendored poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VERSION=1.1.13
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -fLSs https://raw.githubusercontent.com/python-poetry/poetry/$POETRY_VERSION/get-poetry.py | python; \
    ln -sf ${POETRY_HOME}/lib/poetry/_vendor/py3.9 ${POETRY_HOME}/lib/poetry/_vendor/py3.8; \
    chmod +x "$POETRY_HOME/bin/poetry"

# Installing main dependencies
COPY pyproject.toml poetry.lock $FLYWHEEL/
RUN poetry export -f requirements.txt --without-hashes -o $FLYWHEEL/requirements.txt \
    && pip install --no-cache-dir --upgrade scipy==1.8.1 \
    && pip install --no-cache-dir -r $FLYWHEEL/requirements.txt

# Installing the current project (most likely to change, above layer can be cached)
COPY ./ $FLYWHEEL/
RUN pip install --no-cache-dir .

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["python","/flywheel/v0/run.py"]
