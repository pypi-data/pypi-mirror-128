from typing import Optional, Callable

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter


class ConditionalSpanProcessorConfig(object):
    def __init__(self,
                 span_condition_checker: Optional[Callable[[ReadableSpan], bool]] = False):

        self.span_condition_checker = span_condition_checker


class ConditionalSpanProcessor(SimpleSpanProcessor):
    def __init__(self, exporter: SpanExporter,
                 config: Optional[ConditionalSpanProcessorConfig] = None):
        super().__init__(exporter)
        self.span_condition_checker = config.span_condition_checker if config else None

    def on_end(self, span: ReadableSpan) -> None:
        if not self.span_condition_checker(span):
            return

        super().on_end(span)
