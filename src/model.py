import json
from typing import Any, Dict, List, Optional


class Product:
    """
    Класс для представления продукта.

    Атрибуты:
        name (str): Название продукта.
        description (str): Описание продукта.
        _price (float): Цена продукта (хранится во внутреннем атрибуте).
        _quantity (int): Количество товара в наличии (хранится во внутреннем атрибуте).
    """

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Инициализирует объект продукта с указанными параметрами.

        Args:
            name (str): Название продукта.
            description (str): Описание продукта.
            price (float): Цена продукта.
            quantity (int): Количество продукта в наличии.
        """
        self.name: str = name
        self.description: str = description
        self._price: float = price
        self._quantity: int = quantity

    def __str__(self):
        return f'{self.name}, {self._price} руб. Остаток: {self._quantity} шт.'

    @property
    def price(self) -> float:
        """Возвращает цену продукта."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Устанавливает цену продукта, если значение положительное.

        """
        if value <= 0:
            print(f"Цена не должна быть нулевой или отрицательной (попытка установить {value}).")
            return

        if value < self._price:
            answer = input(f"Вы уверены, что хотите понизить цену с {self._price} до {value}? (y/n): ")
            if answer.lower() != "y":
                print("Изменение цены отменено.")
                return

        self._price = value

    @property
    def quantity(self) -> int:
        """Возвращает количество продукта."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """
        Устанавливает количество продукта, если значение не меньше 0.
        При попытке установить отрицательное значение выводится предупреждение.
        """
        if value < 0:
            print(f"Количество не может быть меньше 0. Попытка установить {value}).")
            return
        self._quantity = value

    @classmethod
    def new_product(cls, prod: Dict[str, Any], existing_products: Optional[List["Product"]] = None)\
            -> Optional["Product"]:
        """
        Создает новый продукт из словаря параметров.

        Args:
        prod (Dict[str, Any]): Словарь с параметрами продукта.
        Обязательные ключи: "name", "description", "price", "quantity".
        existing_products (Optional[List[Product]]): Список существующих продуктов для проверки дубликатов.

        Returns:
        Optional[Product]: Созданный или обновленный объект продукта, или None, если валидация не прошла.

        Raises:
        ValueError: Если отсутствуют обязательные ключи в словаре.
        """
        required_keys = {"name", "description", "price", "quantity"}
        if not required_keys.issubset(prod.keys()):
            raise ValueError("Отсутствуют обязательные ключи")

        if prod["price"] < 0 or prod["quantity"] < 0:
            return None

        if existing_products is not None:
            for p in existing_products:
                if p.name == prod["name"]:
                    p.quantity += prod["quantity"]
                    p.price = max(p.price, prod["price"])
                    return p
        new_prod = cls(**prod)
        if existing_products is not None:
            existing_products.append(new_prod)
        return new_prod


class Category:
    """
    Класс для представления категории товаров.

    Атрибуты:
        __name (str): Название категории.
        __description (str): Описание категории.
        __products (List[Any]): Приватный список товаров.
        category_count (int): Общее количество созданных категорий.
        product_count (int): Общее количество товаров во всех категориях.
    """
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Any]) -> None:
        """
        Инициализирует объект категории с заданными значениями.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
            products (List[Any]): Список товаров в категории.
        """
        self.__name: str = name
        self.__description: str = description
        self.__products: List[Any] = products
        Category.category_count += 1
        Category.product_count += len(products)

    def parser_json(self, file_path: str) -> List[Dict[str, Any]]:
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
                    self.__name = item["name"]
                    self.__description = item["description"]
                    self.__products = item["products"]
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_product(self, prod: Product) -> None:
        """
        Добавляет продукт в категорию.

        Args:
            prod (Product): Объект продукта для добавления.

        Raises:
            TypeError: Если переданный аргумент не является экземпляром Product.
        """
        if not isinstance(prod, Product):
            raise TypeError("Можно добавлять только объекты класса Product")
        self.__products.append(prod)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """
        Геттер для получения списка товаров в читаемом формате.

        Если элемент списка является экземпляром Product, используется формат:
            "Название продукта, цена руб. Остаток: количество шт."
        Иначе просто выводится строковое представление элемента.

        Returns:
            str: Строка с описанием каждого продукта или сообщение об отсутствии товаров.
        """
        if not self.__products:
            return "В категории нет товаров."
        formatted = []
        for p in self.__products:
            if hasattr(p, "name") and hasattr(p, "price") and hasattr(p, "quantity"):
                formatted.append(f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт.")
            else:
                formatted.append(str(p))
        return "\n".join(formatted)
