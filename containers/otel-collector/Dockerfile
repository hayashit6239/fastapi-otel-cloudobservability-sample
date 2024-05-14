FROM otel/opentelemetry-collector-contrib:0.90.1

COPY ./containers/otel-collector/otel-collector.yml /etc/otel-collector.yml
COPY ./containers/otel-collector/application_default_credentials.json /etc/application_default_credentials.json

CMD ["--config=/etc/otel-collector.yml"]