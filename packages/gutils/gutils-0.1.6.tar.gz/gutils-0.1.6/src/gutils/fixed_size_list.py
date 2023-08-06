from typing import Any


class FixedSizeList(list):
    def __init__(self, capacity: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self._capacity = capacity

    def append(self, item: Any) -> None:
        if len(self) == self._capacity:
            self.pop(0)
        super().append(item)
