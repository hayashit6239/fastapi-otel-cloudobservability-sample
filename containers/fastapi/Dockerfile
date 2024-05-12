from fnndsc/python-poetry:latest

COPY ./containers/otel-collector/application_default_credentials.json /etc/application_default_credentials.json

ENTRYPOINT cd /app && \
           poetry install && \
           poetry run python create_table.py && \
           poetry run uvicorn src.main:app --host 0.0.0.0 --reload