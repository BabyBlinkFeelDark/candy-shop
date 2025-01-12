import json
from typing import List, Dict


class Product:
    """
    Класс для представления продукта.

    Атрибуты:
        name (str): Название продукта.
        description (str): Описание продукта.
        price (float): Цена продукта.
        quantity (int): Количество товара в наличии.

    Методы:
        __init__: Инициализирует объект продукта с заданными значениями.
    """
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity) -> None:
        """
        Инициализирует объект продукта с указанными параметрами.

        Args:
            name (str): Название продукта.
            description (str): Описание продукта.
            price (float): Цена продукта.
            quantity (int): Количество продукта в наличии.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Класс для представления категории товаров.

    Атрибуты:
        name (str): Название категории.
        description (str): Описание категории.
        products (list): Список товаров, относящихся к категории.
        total_categories (int): Общее количество созданных категорий.
        total_products (int): Общее количество товаров во всех категориях.

    Методы:
        __init__: Инициализирует объект категории.
        parser_json: Парсит JSON-файл и обновляет атрибуты объекта с данными.
    """
    name: str
    description: str
    products: list
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name, description, products):
        """
        Инициализирует объект категории с заданными значениями.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
            products (list): Список товаров в категории.
        """
        self.name = name
        self.description = description
        self.products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def parser_json(self, file_path: str) -> List[Dict]:
        """
        Парсит JSON-файл по указанному пути и возвращает данные в виде списка словарей.

        Args:
            file_path (str): Путь к JSON-файлу.

        Returns:
            list[dict]: Список транзакций, если данные корректны. Пустой список, если файл отсутствует
                        или данные не являются списком.
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                for item in data:
                    self.name = item["name"]
                    self.description = item['description']
                    self.products = item['products']
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []