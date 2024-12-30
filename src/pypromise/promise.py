from enum import IntEnum, auto
from typing import Callable

from pypromise.future import submit_future


class PromiseStatus(IntEnum):
    PENDING = auto()
    FULFILLED = auto()
    REJECTED = auto()


class Promise:
    def __init__(self, callback: Callable[[Callable, Callable], None]):
        self.callback = callback
        self.status = PromiseStatus.PENDING
        self.future = submit_future(callback, self.resolve, self.reject)

    def resolve(self, value):
        if self.status != PromiseStatus.PENDING:
            return None

        self.status = PromiseStatus.FULFILLED
        return value

    def reject(self, value):
        if self.status != PromiseStatus.PENDING:
            return None

        self.status = PromiseStatus.REJECTED
        return value

    def then(self, fn: Callable) -> "Promise":
        def callback(resolve: Callable, reject: Callable):
            try:
                return resolve(fn(self.future.get()))
            except Exception as e:
                return reject(e)

        return Promise(callback)


def submit_promise(fn: Callable, *args) -> Promise:
    def callback(resolve: Callable, reject: Callable):
        try:
            return resolve(fn(*args))
        except Exception as e:
            return reject(e)

    return Promise(callback)
