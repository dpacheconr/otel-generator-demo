import logging
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import \
    OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import Resource
import time
import os
#global resource information
attributes ={
"otelcol.test": "loggen",
}
resource = Resource(attributes=attributes)

#Check which datacentre we exporting our data to
if "OTEL_EXPORTER_OTLP_ENDPOINT" in os.environ:
    OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')
    print("OTEL_EXPORTER_OTLP_ENDPOINT in use is "+OTEL_EXPORTER_OTLP_ENDPOINT)
else:
    print("OTEL_EXPORTER_OTLP_ENDPOINT not configured")
    exit
    
#Set variables to use for OTEL metrics and logs exporters
endpoint="{}".format(OTEL_EXPORTER_OTLP_ENDPOINT)

def get_logger(endpoint,resource, name):
    exporter = OTLPLogExporter(endpoint=endpoint)
    logger = logging.getLogger(str(name))
    logger.handlers.clear()
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logger.addHandler(handler)
    return logger

LoggingInstrumentor().instrument(set_logging_format=True,log_level=logging.DEBUG)

logger = get_logger(endpoint,resource,"project_logger")

while True:
    time.sleep(5)
    logger.info("""PASTE_JSON_HERE""")