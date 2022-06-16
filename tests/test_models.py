from website.models import User, Type, Order

def test_new_user():
    user = User(email='test@test.com', password='testPassword', firstName='Test')
    assert user.email=='test@test.com'
    assert user.password=='testPassword'
    assert user.firstName=='Test'

def test_new_type():
    type = Type(name='testType')
    assert type.name=='testType'

def orders():
    order = Order(user_id='1', items='2')
    assert order.user_id=='1'
    assert order.items=='2'

