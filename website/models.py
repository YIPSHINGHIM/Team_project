import datetime

from flask_login import UserMixin
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base

from website import db

# * Models for the database
class User(db.Model, UserMixin):
    """
    The User class define the User table in database by using sqlalchemy.

    Attributes
    ----------

    id : sqlalchemy.sql.schema.Column
        the primary key for user table and User id
    email : sqlalchemy.sql.schema.Column
        user email (string)
    password : sqlalchemy.sql.schema.Column
        the password for the user (string)
    firstName : sqlalchemy.sql.schema.Column
        user first name (string)
    priority : sqlalchemy.sql.schema.Column
        define the user is a customer or a waiter or kitchen staff (int)
    orders : sqlalchemy.sql.schema.relationship
        what the user order in the restaurant 
    needHelp : sqlalchemy.sql.schema.Column
        boolean flag for the customer to call the waiters 

    @author : Mashhood Manzoor 

    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    priority = db.Column(db.Integer,primary_key = False)
    orders= db.relationship("Order", uselist = False, backref = "user")
    needHelp = db.Column(db.Integer, default = 0)


class Trait(db.Model):
    # ! missing the name and description
    """
    

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column 
        the primary key (int)
    name : sqlalchemy.sql.schema.Column
        

    @author : Harveen Chada
    
    """
    id = id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    

class Type(db.Model):
    """
    The Type class define the Type table in database by using sqlalchemy ,it assign the type for the item .

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        the primary key  (int)
    name : sqlalchemy.sql.schema.Column
        for the food's name (string)
    type : sqlalchemy.sql.schema.relationship
        the type of the food 
    
    @author : Mashhood Manzoor
    @author : Alex Woodcock
    
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    types = db.relationship('Item')


Base = declarative_base()
class Order(db.Model):
    """
    The Order class define the Order table in database by using sqlalchemy , It store the order details .

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        the primary key (int)
    user_id : sqlalchemy.sql.schema.Column
        a foreign key from User table  
    item_id : sqlalchemy.sql.schema.Column
        Items id (int)
    item_quantity : sqlalchemy.sql.schema.Column
        the quantity for the dish customer order (int)
    served : sqlalchemy.sql.schema.Column
        see the food served or not  (boolean)
    prepared : sqlalchemy.sql.schema.Column
        a stage for the dish (int)
    paid : sqlalchemy.sql.schema.Column
        check do the customer paid or not (boolean)
    created_date : sqlalchemy.sql.schema.Column
        the datatime for this order (datatime)
    table_number : :sqlalchemy.sql.schema.Column
        the customer's table number (int) 
    
    @author : Mashhood Manzoor
    @author : Hyunwoo Kim
    @author : Harveen Chada
    @author : Shing him Yip
    
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    item_id = db.Column(db.Integer)
    item_quantity = db.Column(db.Integer)

    items = db.relationship('Item', backref = 'order')
    served = db.Column(db.Boolean(), default = False)
    prepared = db.Column(db.Integer(), default = 0)
    paid = db.Column(db.Boolean(), default = False)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    
    table_number = db.Column(db.Integer, default = 0)


class Kitchen(db.Model):
    """
    A class used to represent tables for Kitchen database. 
    
    Saves data from Order table in class Order.

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        the primary key (int)
    waiter_id : sqlalchemy.sql.schema.Column
        a foreign key from User(waiter) table (int)
    order_id :  sqlalchemy.sql.schema.Column
        an id of order from Order table (int)
    item_id :  sqlalchemy.sql.schema.Column
        id of item for the menu (int)
    item_name : sqlalchemy.sql.schema.Column
        name of the item for the menu (string)
    item_quantity : sqlalchemy.sql.schema.Column
        the quantity of the item (int)
    created_date : sqlalchemy.sql.schema.Column
        the time when the order was made (datetime)
    ready : :sqlalchemy.sql.schema.Column
        state whether the menu is ready or not (boolean) 
    
    @author : Hyunwoo Kim
    
    """
    id = db.Column(db.Integer, primary_key=True)
    waiter_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    item_name = db.Column(db.String(150))
    item_quantity = db.Column(db.Integer)

    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    ready = db.Column(db.Boolean(), default=False)

class Item(db.Model):
    """
    The Order class define the Order table in database by using sqlalchemy , It store the order details .

    Attributes
    ----------
    id : sqlalchemy.sql.schema.Column
        the primary key (int)
    name : sqlalchemy.sql.schema.Column
        the dish name (string)
    price : sqlalchemy.sql.schema.Column
        dish price (float)
    calories : sqlalchemy.sql.schema.Column
        calories of the dish(int)
    is_vegetarian : sqlalchemy.sql.schema.Column
        check vegetarian or not (int)
    is_alcoholic : sqlalchemy.sql.schema.Column
        check alcoholic or not (int)
    type_id : sqlalchemy.sql.schema.Column
        ForeignKey form type table
    order_id : sqlalchemy.sql.schema.Column
        ForeignKey form order table
    trait_id : :sqlalchemy.sql.schema.Column
        ForeignKey form trait table
    traits : sqlalchemy.sql.schema.Column
        
    is_available : sqlalchemy.sql.schema.Column
        check the dish is available or not (boolean)
    time_taken : sqlalchemy.sql.schema.Column
        the cooking time (int)
    
    @author : Mashhood Manzoor
    @author : Harveen Chada
    @author : Alex Woodcock

    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    price = db.Column(db.Float)

    calories = db.Column(db.Integer)
    is_vegetarian = db.Column(db.Integer())
    is_alcoholic = db.Column(db.Integer())

    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    trait_id = db.Column(db.Integer, db.ForeignKey('trait.id'))
    traits = db.relationship('Trait', uselist = False, backref = 'item')

    is_available = db.Column(db.Boolean(), default=True)
    
    time_taken = db.Column(db.Integer())
