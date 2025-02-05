import json
from io import StringIO
from unittest.mock import patch

import pytest

from src.model import Category, Product


@pytest.fixture
def product_coffee():
    return Product("coffe", "just a coffe", 300.0, 10)


@pytest.fixture
def category_coffee():
    prod = Product("coffe", "just a coffe", 300.0, 10)
    return Category("coffe", "just a coffe", [prod])


def test_init(product_coffee):
    assert product_coffee.name == "coffe"
    assert product_coffee.description == "just a coffe"
    assert product_coffee.price == 300.0
    assert product_coffee.quantity == 10


def test_init_count(category_coffee):
    assert category_coffee._Category__name == "coffe"
    assert category_coffee._Category__description == "just a coffe"
    expected = "coffe, 300.0 руб. Остаток: 10 шт."
    assert category_coffee.products == expected
    assert Category.category_count >= 1
    assert Category.product_count >= 1


def test_parser_json_valid_data():
    json_data = [
        {"name": "Category1", "description": "Description1", "products": ["prod1", "prod2"]},
        {"name": "Category2", "description": "Description2", "products": ["prod3"]},
    ]
    with patch("builtins.open", return_value=StringIO(json.dumps(json_data))):
        category = Category("", "", [])
        result = category.parser_json("fake_path.json")
        assert category._Category__name == "Category2"
        assert category._Category__description == "Description2"
        assert category.products == "prod3"
        assert result == json_data


def test_parser_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        category = Category("", "", [])
        result = category.parser_json("non_existing_file.json")
        assert result == []


def test_set_negative_price(product_coffee, capsys):
    product_coffee.price = -100
    captured = capsys.readouterr().out
    assert "Цена не должна быть нулевой или отрицательной" in captured
    assert product_coffee.price == 300.0


def test_set_negative_quantity(product_coffee, capsys):
    product_coffee.quantity = -5
    captured = capsys.readouterr().out
    assert "Количество не может быть меньше 0" in captured
    assert product_coffee.quantity == 10


def test_price_decrease_confirmation_accept(product_coffee, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "y")
    product_coffee.price = 250
    assert product_coffee.price == 250


def test_price_decrease_confirmation_decline(product_coffee, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "n")
    product_coffee.price = 250
    captured = capsys.readouterr().out
    assert "Изменение цены отменено." in captured
    assert product_coffee.price == 300.0


def test_new_product_validation():
    with pytest.raises(ValueError):
        Product.new_product({"name": "test", "description": "desc", "price": 100.0})
    result = Product.new_product({"name": "test", "description": "desc", "price": -100.0, "quantity": 10})
    assert result is None


def test_new_product_duplicate():
    products_list = []
    prod_data1 = {"name": "TestProd", "description": "desc", "price": 100.0, "quantity": 5}
    prod_data2 = {"name": "TestProd", "description": "desc", "price": 120.0, "quantity": 3}
    p1 = Product.new_product(prod_data1, products_list)
    p2 = Product.new_product(prod_data2, products_list)
    assert p1 is p2
    assert p1.quantity == 8
    assert p1.price == 120.0


def test_str_method():
    p = Product("TestProd", "Test Desc", 100.0, 10)
    expected = "TestProd, 100.00 руб. Остаток: 10 шт."
    assert str(p) == expected


def test_add_method():
    p1 = Product("Prod1", "Desc", 100.0, 10)
    p2 = Product("Prod2", "Desc", 200.0, 5)
    total_value = p1 + p2
    assert total_value == 2000


def test_category_iterator():
    p1 = Product("Prod1", "Desc", 100.0, 10)
    p2 = Product("Prod2", "Desc", 200.0, 5)
    category = Category("TestCat", "Category Desc", [p1, p2])
    iterated_products = [prod for prod in category]
    assert iterated_products == [p1, p2]


def test_existing_product_update():
    products_list = []
    prod_data1 = {"name": "TestProd", "description": "Desc", "price": 100.0, "quantity": 5}
    prod_data2 = {"name": "TestProd", "description": "Desc", "price": 120.0, "quantity": 3}
    p1 = Product.new_product(prod_data1, products_list)
    p2 = Product.new_product(prod_data2, products_list)
    assert p1 is p2
    assert p1.quantity == 8
    assert p1.price == 120.0


