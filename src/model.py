import json


class Employee:  # Название класса
    name: str  # Атрибуты (свойства) класса
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):  # Конструктор
        self.name = name  # Атрибуты (свойства) класса
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:  # Название класса
    name: str  # Атрибуты (свойства) класса
    description: str
    products: list
    total_categories: int = 0
    total_products: int = 0

    def __init__(self, name, description, products):  # Конструктор
        self.name = name  # Атрибуты (свойства) класса
        self.description = description
        self.products = products
        Category.total_categories += 1
        Category.total_products += len(products)

    def parser_json(self, file_path: str):
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