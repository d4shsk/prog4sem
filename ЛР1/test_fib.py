import unittest

from iterators import FibGetItem, FibIterator
from coroutine import fib_coroutine


class TestFibonacci(unittest.TestCase):
    """Набор тестов для проверки реализаций чисел Фибоначчи."""

    def test_fib_getitem(self) -> None:
        """Проверить работу упрощенного итератора через __getitem__."""
        fib = FibGetItem(7)
        result = list(fib)
        self.assertEqual(result, [0, 1, 1, 2, 3, 5, 8])
        
        # Проверка прямого доступа по индексу
        self.assertEqual(fib[5], 5)
        with self.assertRaises(IndexError):
            _ = fib[7]

    def test_fib_iterator(self) -> None:
        """Проверить работу обычного итератора через __iter__ и __next__."""
        fib = FibIterator(7)
        result = list(fib)
        self.assertEqual(result, [0, 1, 1, 2, 3, 5, 8])

    def test_fib_coroutine(self) -> None:
        """Проверить работу сопрограммы и ее реакцию на send()."""
        coro = fib_coroutine()
        
        # Стандартная генерация (для старта сопрограммы нужно вызвать next)
        self.assertEqual(next(coro), 0)
        self.assertEqual(next(coro), 1)
        self.assertEqual(next(coro), 1)
        self.assertEqual(next(coro), 2)
        self.assertEqual(next(coro), 3)
        
        # Сбрасываем сопрограмму, передав True.
        self.assertEqual(coro.send(True), 0)
        
        # Проверяем, что последовательность началась заново
        self.assertEqual(next(coro), 1)
        self.assertEqual(next(coro), 1)


if __name__ == '__main__':
    unittest.main()