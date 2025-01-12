import json
from io import StringIO

import pytest

from src.model import Product, Category
from unittest.mock import Mock, patch


@pytest.fixture
def employee_coffe():
    return Product('coffe', 'just a coffe', 300.0, 10)

@pytest.fixture
def category_coffe():
    return Category('coffe', 'just a coffe', ["coffe"])

def test_init(employee_coffe):
    assert employee_coffe.name == 'coffe'
    assert employee_coffe.description == 'just a coffe'
    assert employee_coffe.price == 300.0
    assert employee_coffe.quantity == 10

def test_init_count(category_coffe):
    assert category_coffe.name == 'coffe'
    assert category_coffe.description == 'just a coffe'
    assert category_coffe.products == ["coffe"]
    assert category_coffe.category_count == 1
    assert category_coffe.product_count == 1

def test_parser_json_valid_data():
    json_data = [
        {"name": "Category1", "description": "Description1", "products": ["prod1", "prod2"]},
        {"name": "Category2", "description": "Description2", "products": ["prod3"]}
    ]


    with patch("builtins.open", return_value=StringIO(json.dumps(json_data))):
        category = Category("", "", [])
        result = category.parser_json("fake_path.json")
        assert category.name == "Category2"
        assert category.description == "Description2"
        assert category.products == ["prod3"]
        assert result == json_data

def test_parser_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        category = Category("", "", [])
        result = category.parser_json("non_existing_file.json")

        assert result == []
