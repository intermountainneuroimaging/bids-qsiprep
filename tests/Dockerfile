ARG BASE

# hadolint ignore=DL3006
FROM ${BASE}

ENV FLYWHEEL="/flywheel/v0"

# Installing pre-commit and poetry with dev dependencies:
RUN poetry run pip install pre-commit \
    &&  poetry install

ENTRYPOINT [""]
