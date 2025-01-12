# Candy-shop

Этот проект включает два класса: `Product` и `Category`, которые позволяют управлять товарами и их категориями. Также предусмотрен метод для парсинга JSON-файлов с данными о категориях и товарах.

## Описание классов

### 1. `Product`

Класс для представления продукта с такими атрибутами как название, описание, цена и количество.

**Атрибуты:**
- `name (str)` — Название продукта.
- `description (str)` — Описание продукта.
- `price (float)` — Цена продукта.
- `quantity (int)` — Количество продукта в наличии.

**Методы:**
- `__init__(name, description, price, quantity)` — Инициализирует объект продукта с заданными значениями.

### 2. `Category`

Класс для представления категории товаров, которая может включать несколько продуктов.

**Атрибуты:**
- `name (str)` — Название категории.
- `description (str)` — Описание категории.
- `products (list)` — Список товаров, относящихся к категории.
- `category_count (int)` — Общее количество созданных категорий (статическое).
- `product_count (int)` — Общее количество товаров во всех категориях (статическое).

**Методы:**
- `__init__(name, description, products)` — Инициализирует объект категории.
- `parser_json(file_path)` — Парсит JSON-файл и обновляет атрибуты объекта с данными о категории.

## Использование

### 1. Создание экземпляра класса `Product`

```python
product = Product(name="Product1", description="Description of Product1", price=19.99, quantity=100)
```

### 2. Создание экземпляра класса `Category`

```python
category = Category(name="Category1", description="Description of Category1", products=[product])
```

### 3. Парсинг JSON-файла

Для того чтобы заполнить данные о категории и продуктах из JSON-файла, используйте метод `parser_json`. Он читает файл по указанному пути и обновляет атрибуты объекта.

Пример использования:

```python
category = Category(name="", description="", products=[])
category_data = category.parser_json("path/to/categories.json")
```
JSON-файл должен содержать список объектов, каждый из которых представляет категорию с атрибутами `name`, `description` и `products`.

### Пример JSON:

```json
[
  {
    "name": "Category1",
    "description": "Description of Category1",
    "products": [
      {
        "name": "Product1",
        "description": "Description of Product1",
        "price": 19.99,
        "quantity": 100
      }
    ]
  }
]
```

### Установка
Для работы с проектом необходимо иметь установленный Python 3.x. Если требуется установить зависимости, воспользуйтесь менеджером пакетов `poetry`.

Клонируйте репозиторий:

```bash
git clone https://github.com/your_username/repository_name.git
cd repository_name
```
Установите необходимые библиотеки (если они есть):

```bash
poetry install 
```

### Лицензия
Этот проект лицензирован под MIT License. Подробнее смотрите в файле [LICENSE]().
