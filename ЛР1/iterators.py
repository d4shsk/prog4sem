from typing import Iterator, List


class FibGetItem:
    """
    Упрощенный итератор ряда Фибоначчи на основе __getitem__.

    Позволяет итерироваться по объекту за счет обращения по индексу.
    Итерация прекращается, когда выбрасывается исключение IndexError.
    """

    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self._cache: List[int] = [0, 1]

    def __getitem__(self, index: int) -> int:
        if index < 0 or index >= self.limit:
            raise IndexError("Индекс вне диапазона")
        
        # Динамически достраиваем кэш до нужного индекса
        while len(self._cache) <= index:
            self._cache.append(self._cache[-1] + self._cache[-2])
            
        return self._cache[index]


class FibIterator:
    """
    Обычный итератор ряда Фибоначчи.

    Использует классический протокол итератора с методами __iter__ и __next__.
    """

    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.current_step: int = 0
        self.a: int = 0
        self.b: int = 1

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        if self.current_step >= self.limit:
            raise StopIteration
        
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.current_step += 1
        
        return result