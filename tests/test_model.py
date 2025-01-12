import pytest

from src.model import Employee, Category


@pytest.fixture
def employee_coffe():
    return Employee('coffe', 'just a coffe', 300.0,10)

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
    assert category_coffe.total_categories == 1
    assert category_coffe.total_products == 1