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