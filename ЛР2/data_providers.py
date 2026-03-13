import abc
import csv
import io
import json
from typing import Any, Dict, List

import yaml


class DataProvider(abc.ABC):
    """
    Абстрактный базовый класс (интерфейс) для поставщиков данных.
    
    Определяет общий контракт для базовых компонентов и их декораторов.
    """

    @abc.abstractmethod
    def get_data(self) -> Any:
        pass


class SimpleDataProvider(DataProvider):
    """
    Базовый компонент, предоставляющий сырые данные.
    """

    def __init__(self, data: List[Dict[str, Any]]) -> None:
        self._data = data

    def get_data(self) -> List[Dict[str, Any]]:
        return self._data


class DataDecorator(DataProvider):
    """
    Базовый класс декоратора.
    
    Содержит ссылку на обернутый объект (компонент) и делегирует ему
    выполнение операций по умолчанию.
    """

    def __init__(self, component: DataProvider) -> None:
        self._component = component

    def get_data(self) -> Any:
        return self._component.get_data()


class JSONDecorator(DataDecorator):
    """Декоратор для форматирования данных в строку JSON."""

    def get_data(self) -> str:
        data = super().get_data()
        return json.dumps(data, ensure_ascii=False, indent=4)


class YAMLDecorator(DataDecorator):
    """Декоратор для форматирования данных в строку YAML."""

    def get_data(self) -> str:
        data = super().get_data()
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)


class CSVDecorator(DataDecorator):
    """Декоратор для форматирования данных в строку CSV."""

    def get_data(self) -> str:
        data = super().get_data()
        
        if not data:
            return ""
        
        output = io.StringIO()
        fieldnames = list(data[0].keys())
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
        return output.getvalue()