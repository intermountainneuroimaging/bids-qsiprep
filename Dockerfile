FROM python:3.8-slim as base

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
COPY fw_gear_skeleton $FLYWHEEL/fw_gear_skeleton
RUN poetry install --no-dev

# Configure entrypoint
RUN chmod a+x $FLYWHEEL/run.py
ENTRYPOINT ["poetry","run","python","/flywheel/v0/run.py"]
