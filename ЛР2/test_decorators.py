import json
import unittest

import yaml  # Требует установки: pip install pyyaml

# Импортируем классы из нашего основного файла
from data_providers import (
    CSVDecorator,
    JSONDecorator,
    SimpleDataProvider,
    YAMLDecorator,
)


class TestDataDecorators(unittest.TestCase):
    """Набор тестов для проверки паттерна Декоратор и форматов данных."""

    def setUp(self) -> None:
        """Подготовить тестовые данные перед каждым тестом."""
        self.raw_data = [
            {"id": 1, "name": "Иван", "role": "developer"},
            {"id": 2, "name": "Анна", "role": "manager"}
        ]
        self.provider = SimpleDataProvider(self.raw_data)

    def test_base_provider(self) -> None:
        """Проверить, что базовый компонент возвращает исходные данные."""
        self.assertEqual(self.provider.get_data(), self.raw_data)

    def test_json_decorator(self) -> None:
        """Проверить корректность форматирования в JSON."""
        json_provider = JSONDecorator(self.provider)
        result = json_provider.get_data()
        
        # Проверяем, что строка парсится обратно в исходные данные
        parsed_data = json.loads(result)
        self.assertEqual(parsed_data, self.raw_data)

    def test_yaml_decorator(self) -> None:
        """Проверить корректность форматирования в YAML."""
        yaml_provider = YAMLDecorator(self.provider)
        result = yaml_provider.get_data()
        
        # Проверяем, что строка парсится обратно в исходные данные
        parsed_data = yaml.safe_load(result)
        self.assertEqual(parsed_data, self.raw_data)

    def test_csv_decorator(self) -> None:
        """Проверить корректность форматирования в CSV."""
        csv_provider = CSVDecorator(self.provider)
        result = csv_provider.get_data()
        
        # Проверяем наличие заголовков и данных в результирующей строке
        self.assertIn("id,name,role", result)
        self.assertIn("1,Иван,developer", result)
        self.assertIn("2,Анна,manager", result)

    def test_empty_csv(self) -> None:
        """Проверить обработку пустого списка для CSV."""
        empty_provider = SimpleDataProvider([])
        csv_provider = CSVDecorator(empty_provider)
        self.assertEqual(csv_provider.get_data(), "")


if __name__ == '__main__':
    unittest.main()