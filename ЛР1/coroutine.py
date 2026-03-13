from typing import Generator, Optional


def fib_coroutine() -> Generator[int, Optional[bool], None]:
    """
    Сопрограмма для бесконечной генерации чисел Фибоначчи.

    Отличие от генератора: принимает значения извне через метод send().
    Если отправить в сопрограмму значение True (coro.send(True)), 
    последовательность будет сброшена к начальному состоянию (0, 1).

    :return: Генератор, отдающий числа Фибоначчи и принимающий флаг сброса.
    """
    a: int = 0
    b: int = 1
    while True:
        reset: Optional[bool] = yield a
        
        if reset is True:
            a, b = 0, 1
        else:
            a, b = b, a + b