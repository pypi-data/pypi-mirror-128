from collections import OrderedDict
from typing import Any, Callable, Dict, Generator, Sequence


def chunks(l: Sequence, n: int = 5) -> Generator[Sequence, None, None]:
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

class LRUCache:
    # initialising capacity
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def has(self, key) -> bool:
        return key in self.cache


    def get(self, key):
        if key not in self.cache:
            return None
        else:
            self.cache.move_to_end(key)
            return self.cache[key]


    def put(self, key, value) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def pop(self, key, value):
        self.cache.pop(key, None)
