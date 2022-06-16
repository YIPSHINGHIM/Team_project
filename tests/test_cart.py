from sqlalchemy import null
from website.cart import cart
from website.models import Item

test_cart = cart()

def test_create():
    assert test_cart==test_cart

def test_cart_list():
    assert test_cart.cart_items == []

def test_cart_add():
    new_cart = cart()
    new_cart.add_item(1)
    assert new_cart.cart_items == [1]

def test_cart_add_multiple():
    new_cart = cart()
    new_cart.add_item(1)
    new_cart.add_item(2)
    new_cart.add_item(3)
    assert new_cart.cart_items == [1,2,3]

def test_remove_item():
    new_cart = cart()
    new_cart.add_item(1)
    new_cart.remove_item(1)
    assert new_cart.cart_items == []

def test_clear_cart():
    new_cart = cart()
    new_cart.add_item(1)
    new_cart.clear_cart()
    assert new_cart.cart_items == []

def test_cart_total():
    new_cart = cart()
    assert new_cart.cart_total() == 0


