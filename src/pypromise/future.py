import threading
from threading import Condition
from typing import Callable


class Future:
    def __init__(self):
        self.value = None
        self.cond = Condition()
        self.completed = False
        self.exception = None

    def get(self):
        with self.cond:
            while not self.completed:
                self.cond.wait()

        return self.value


def submit_future(fn: Callable, *args) -> Future:
    fut = Future()

    def mfn():
        with fut.cond:
            try:
                fut.value = fn(*args)
            except Exception as e:
                fut.exception = e
                raise
            finally:
                fut.completed = True
                fut.cond.notify_all()

    t = threading.Thread(target=mfn)
    t.start()

    return fut
