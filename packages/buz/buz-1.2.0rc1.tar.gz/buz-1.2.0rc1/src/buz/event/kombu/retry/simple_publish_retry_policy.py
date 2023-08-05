from typing import Callable, Optional

from buz.event import Event
from buz.event.kombu.retry import PublishRetryPolicy

ErrorCallback = Callable[[Event, Exception, range, int], None]


class SimplePublishRetryPolicy(PublishRetryPolicy):
    def __init__(
        self,
        max_retries: int = 10,
        interval_start: float = 0,
        interval_step: float = 0.1,
        interval_max: float = 1,
        error_callback: Optional[ErrorCallback] = None,
    ):
        self.__max_retries = max_retries
        self.__interval_start = interval_start
        self.__interval_step = interval_step
        self.__interval_max = interval_max
        self.__error_callback = error_callback

    def max_retries(self, event: Event) -> int:
        return self.__max_retries

    def interval_start(self, event: Event) -> float:
        return self.__interval_start

    def interval_step(self, event: Event) -> float:
        return self.__interval_step

    def interval_max(self, event: Event) -> float:
        return self.__interval_max

    def error_callback(self, event: Event, exc: Exception, interval_range: range, retries: int) -> None:
        if self.__error_callback is not None:
            self.__error_callback(event, exc, interval_range, retries)
