import json
from typing import Any, Dict, List, Optional, Iterator, cast


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

    def __str__(self) -> str:
        """
        Возвращает строковое представление продукта.

        Выводится в формате:
            "Название продукта, цена руб. Остаток: количество шт."
        (без двоеточия после названия)
        """
        return f"{self.name}, {self._price:.2f} руб. Остаток: {self._quantity} шт."

    def __add__(self, other: "Product") -> float:
        """
        Реализует оператор сложения для продуктов.

        Возвращает суммарную стоимость товаров (цена * количество) для обоих продуктов.
        Если other не является объектом Product или объекты относятся к разным классам,
        выбрасывается TypeError.
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")
        if type(self) != type(other):
            raise TypeError("Можно складывать только объекты одного класса")
        return (self._price * self._quantity) + (other._price * other._quantity)

    @property
    def price(self) -> float:
        """Возвращает цену продукта."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Устанавливает цену продукта, если значение положительное.

        Если новая цена ниже текущей, запрашивает подтверждение у пользователя.
        При попытке установить нулевую или отрицательную цену выводится предупреждение.

        Args:
            value (float): Новая цена.
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

        Args:
            value (int): Новое количество.
        """
        if value < 0:
            print(f"Количество не может быть меньше 0. Попытка установить {value}).")
            return
        self._quantity = value

    @classmethod
    def new_product(
        cls, prod: Dict[str, Any], existing_products: Optional[List["Product"]] = None
    ) -> Optional["Product"]:
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


class Smartphone(Product):
    """
    Класс для представления смартфона.

    Помимо свойств Product, имеет:
        efficiency (float): Производительность.
        model (str): Модель смартфона.
        memory (int): Объем встроенной памяти.
        color (str): Цвет смартфона.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency: float = efficiency
        self.model: str = model
        self.memory: int = memory
        self.color: str = color


class LawnGrass(Product):
    """
    Класс для представления газонной травы.

    Помимо свойств Product, имеет:
        country (str): Страна-производитель.
        germination_period (str): Срок прорастания.
        color (str): Цвет травы.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.country: str = country
        self.germination_period: str = germination_period
        self.color: str = color


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
            List[Dict[str, Any]]: Список транзакций, если данные корректны.
                                  Пустой список, если файл отсутствует или данные не являются списком.
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
            TypeError: Если переданный аргумент не является экземпляром Product или его наследником.
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
        Иначе выводится строковое представление элемента.

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

    def __iter__(self) -> "CategoryIterator":
        """Возвращает итератор для перебора товаров категории."""
        return CategoryIterator(self)


class CategoryIterator:
    """
    Вспомогательный класс для итерации по товарам категории.

    Принимает объект класса Category и позволяет перебирать товары в цикле for.
    """

    def __init__(self, category: Category) -> None:
        self._products: List[Any] = cast(List[Any], getattr(category, "_Category__products"))
        self._index: int = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Any:
        if self._index >= len(self._products):
            raise StopIteration
        result = self._products[self._index]
        self._index += 1
        return result
