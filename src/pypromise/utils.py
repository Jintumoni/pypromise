import time
from typing import Callable

from pypromise.promise import submit_promise


def set_timeout(fn: Callable, duration: int):
    def helper():
        time.sleep(duration)
        fn()

    submit_promise(helper)
