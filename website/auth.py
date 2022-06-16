import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import false, true, update
from werkzeug.security import check_password_hash, generate_password_hash

from website.cart import cart

from . import Mail, db
from .models import Item, Kitchen, Order, Type, User

auth = Blueprint('auth', __name__)
current_id = int
current_priority = int
cart = cart()

food_img = []
for file in os.listdir('website/static/images/food_img'):
    food_img.append(file)
food_img.sort()

def has_number(inputString):
    """
    Checks if string has an integer in it
    
    Returns
    -------
    Return any(char.isdigit() for char in inputString) to give a boolena on whether there is any numbers
    
    @author : Harry Webster
    """
    return any(char.isdigit() for char in inputString)

def has_specialC(inputString):
    """
    Checks if a String has any no alphanumeric values e.g. ?,/,<
    
    Returns
    -------
    Return any(not char.isalnum() for char in inputString) to give a boolean on whether there is any special characters
    
    @author : Harry Webster
    """
    return any(not char.isalnum() for char in inputString)


@auth.route('/customer_login', methods=['GET', 'POST'])
def login():
    """
    rendering the login page 

    Returns
    -------
    Return render_template function to render login.html template
    Return boolean to see the user logged in or not
    
    @author : Harry Webster
    
    """
    # global current_id
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        global current_id, current_priority
        if user:
            if (user.password == password):
                if (user.priority == 0):
                    flash('Logged in succesfully', category='success')
                    login_user(user, remember=True)
                    current_id = user.id
                    current_priority = user.priority
                    return redirect(url_for('views.home'))
                else:
                    flash('This is a customer login, find a staff terminal',category='error')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('email does not exist.', category='error')

    return render_template("customer_login.html", boolean=True)


@auth.route('/logout')
@login_required
def logout():
    """
    letting user to log out the account

    Returns
    -------
    Return redirect function to render the home page
    
    @author : Harry Webster
    
    """
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/customer_signup', methods=['GET', 'POST'])
def sign_up():
    """
    rendering the sign page 

    Returns
    -------
    Return redirect function to render the home page if the user already existing or error
    Return render_template function to render sign.html template if user sign up successful
    
    @author : Harry Webster
    @author : Harveen Chada
    @author : Mashhood Manzoor
    @author : Hyunwoo Kim
    
    """
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        ### CODE TO CHECK FOR EXISTING EMAILS
        user = User.query.filter_by(email=email).first()
        if(user):
            if user.email == email:
                flash('Email already exists', category='error')
                return render_template("customer_signup.html")
        if len(email) < 10:
            flash('Email must be great than 10 characters.', category='error')
            return render_template("customer_signup.html")
        if len(firstName) < 2:
            flash('Firstname must be great than 1 characters.', category='error')
            return render_template("customer_signup.html")
        if password1 != password2:
            flash('Password must be equal to each other.', category='error')
            return render_template("customer_signup.html")
        if len(password1) < 7:
            flash('Password must be longer than 7 characters.', category='error')
            return render_template("customer_signup.html")
        if(has_number(firstName)):
            flash('Name can not have a number.', category='error')
            return render_template("customer_signup.html")
        if(has_specialC(firstName)):
            flash('Name can not have any special characters.', category='error')
            return render_template("customer_signup.html")
        else:
            new_user = User(email=email, firstName=firstName,
                            password=password1, priority=0)
            db.session.add(new_user)
            db.session.commit()
            with open('website/resources/user.txt','a') as f:
                f.write('\n'+email+","+firstName+","+password1+",0")
            login_user(new_user, remember=True)
            global current_id
            current_id = new_user.id
            flash('Account created!', category='success')
        return redirect(url_for('views.home'))
    return render_template("customer_signup.html")


@auth.route('/customer_contact', methods=['GET', 'POST'])
def contact():
    """
    rendering the contact page 

    Returns
    -------
    Return render_template function to render contact.html
    
    @author : Harveen Chada
    
    """
    if request.method == "POST":
        name = request.form.get('firstname')
        email = request.form.get('email')
        message = request.form.get('message')
        # msg = Message(subject=f"Mail from {name}", body=f"Name = {name}; Email = {email}\n Message = {message} ",
                    #   sender="", recipients=['harveen.chada@gmail.com'])
        # mail.send(msg)

    return render_template("customer_contact.html", success=True)


@auth.route('/submenu', methods=["GET", "POST"])
def submenu():
    """
    Displays menu page for customers.
    
    It loads item from database using sqlAlchemy to show the menu items
    with different conditions.
    
    
    Attributes
    ----------
    starters_data : Item
        menus for starters (type id = 1)
    main_data : Item
        menus for main dishes (typ id = 2)
    desserts_data : Item
        menus for desserts (typ id = 3)
    drinks_data : Item
        menus for drinks (typ id = 4)
    alcohol_data : Item
        menus for alcohol (typ id = 5)

    Returns
    -------
    Render_template
        submenu.html for menu page,
        starters_data for starters,
        main_data for main dishes,
        desserts_data for desserts,
        drinks_data for drinks,
        alcohol_data for alcohols,
        food_img for images of selected menus
    
    @author : Hyunwoo Kim
    @author : Shing him Yip
    @author : Alex Woodcock
    @author : Harveen Chada

    """
    #Filters inital menu by availability.
    starters_data, main_data, desserts_data, drinks_data, alcohol_data = [], [], [], [], []
    del starters_data, main_data, desserts_data, drinks_data, alcohol_data
    starters_data = Item.query.filter_by(type_id=1, is_available=True)
    main_data = Item.query.filter_by(type_id=2, is_available=True)
    desserts_data = Item.query.filter_by(type_id=3, is_available=True)
    drinks_data = Item.query.filter_by(type_id=4, is_available=True)
    alcohol_data = Item.query.filter_by(type_id=5, is_available=True)

    if request.method == 'POST':

        for x in range(50):
            if str(x) in request.form:
                cart.add_item(x)
                flash('Added', category='success')

        if ('call_waiter') in request.form:
            flash('Waiter called over!', category='success')
            if (current_user.is_authenticated and current_user.email.endswith("@OAXACA.com")):
                flash('Table 1 has called you over', category='error')

        max_calories = request.form.get('max_calories')

        #Calories are not obtained when POST request is done for Call Waiter/Add to Cart functions.
        #Set calories to 1500 (default) in this case.
        if (max_calories == None):
            max_calories = 1500
        
        starters_data = starters_data.filter(Item.calories <= max_calories)
        main_data = main_data.filter(Item.calories <= max_calories)
        desserts_data = desserts_data.filter(Item.calories <= max_calories)
        drinks_data = drinks_data.filter(Item.calories <= max_calories)
        alcohol_data = alcohol_data.filter(Item.calories <= max_calories)

        if ('non_alcoholic') in request.form:
            starters_data = starters_data.filter(Item.is_alcoholic!=1)
            main_data = main_data.filter(Item.is_alcoholic!=1)
            desserts_data = desserts_data.filter(Item.is_alcoholic!=1)
            drinks_data = drinks_data.filter(Item.is_alcoholic!=1)
            alcohol_data = alcohol_data.filter(Item.is_alcoholic!=1)
            
        
        if ('is_vegetarian') in request.form:
            starters_data = starters_data.filter(Item.is_vegetarian==1)
            main_data = main_data.filter(Item.is_vegetarian==1)
            desserts_data = desserts_data.filter(Item.is_vegetarian==1)
            drinks_data = drinks_data.filter(Item.is_vegetarian==1)
            alcohol_data = alcohol_data.filter(Item.is_vegetarian==1)
        

        if ('submit_search') in request.form:
            max_calories = request.form.get('max_calories')
            is_vegetarian = request.form.get('is_vegetarian')
            is_alcoholic = request.form.get('is_alcoholic')

            return render_template('submenu.html',
                                   starters_data=starters_data,
                                   main_data=main_data,
                                   desserts_data=desserts_data,
                                   drinks_data=drinks_data,
                                   alcohol_data=alcohol_data,
                                   food_img=food_img,
                                   max_calories=int(max_calories),
                                   is_vegetarian=is_vegetarian,
                                   is_alcoholic=is_alcoholic
                                   )

    return render_template('submenu.html',
                           starters_data=starters_data,
                           main_data=main_data,
                           desserts_data=desserts_data,
                           drinks_data=drinks_data,
                           alcohol_data=alcohol_data,
                           food_img=food_img,
                           # Calories = Calories
                           max_calories=3000,
                           is_vegetarian=false,
                           is_alcoholic=false
                           )


@auth.route('/customer_order', methods=['GET', 'POST'])
def order():
    """
    Displays cart(basket) page for customers
    
    It loads data from cart.py that is added from '/submenu'  
    by customer to be ordered.
    
    Attributes
    ----------
    item_list : list
        list of all menus in class Item
    data : dict
        dictionary of all items that is added in Order class.

    Returns
    -------
    Render_template
        order_page_1.html for order page,
        cart_price for total price,
        data for ordered items in cart
        food_img for images of selected menus
        item_list for list of all menus
        
    
    @author : Mashhood Manzoor
    @author : Hyunwoo Kim
    @author : Harveen Chada
    @author : Shing him Yip
    
    """
    item_list = []

    for x in range(1, len(food_img)):

        food_item = Item.query.filter_by(id=x).first()
        item_list.append(food_item)

    data = cart.in_cart()

    if request.method == 'POST':     
   
        if ('help') in request.form:
            queryperson = current_user

            queryperson.needHelp = 1
            db.session.commit()
            return render_template('customer_order.html',
                                   cart_price=cart.cart_total(),
                                   data=data,
                                   food_img=food_img,
                                   item_list=item_list
                                   )
            
        if ('ordering') in request.form:
            
            tableNumber = request.form['table_number']
            
            for x in item_list:
                if x.id in data:
                    new_order = Order(user_id=current_id, item_id=x.id, item_quantity=data[x.id], table_number=tableNumber)

                    db.session.add(new_order)
                    db.session.commit()
            cart.clear_cart()
            
            flash('order sent', category='success')
            return render_template('customer_order.html',
                                   cart_price=cart.cart_total(),
                                   data=data,
                                   food_img=food_img,
                                   item_list=item_list
                                   )

        for x in range(1, len(food_img)):
            if (str(x) + ' del') in request.form:
                flash('item deleted !', category='success')
                cart.remove_item(x)

                return render_template('customer_order.html',
                                       cart_price=cart.cart_total(),
                                       data=data,
                                       food_img=food_img,
                                       item_list=item_list
                                       )

            if (str(x) + ' update') in request.form:
                flash('price update !', category='success')
                quantity = request.form

                if x in data:
                    quantity_change = request.form[str(x) + ' quantity']
                    cart.change_cart_value(x, int(quantity_change))
                    print(data)
                    print(data.get(x))

                return render_template('customer_order.html',
                                       cart_price=cart.cart_total(),
                                       data=data,
                                       food_img=food_img,
                                       quantity=quantity,
                                       item_list=item_list
                                       )

    return render_template('customer_order.html',
                           cart_price=cart.cart_total(),
                           data=data,
                           food_img=food_img,
                           quantity=0,
                           item_list=item_list
                           )





@auth.route('/waiter_notific', methods = ['GET', 'POST'])
def waiter_notific():
    if current_priority !=1:
        flash('Wrong place!', category='error')
        return render_template("home.html")
    query = User.query.filter_by(needHelp=1).all()
    queryList = []
    for x in query:
        queryList.append(x)

    return render_template('waiter_notific.html',
                            queryList = queryList)

@auth.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        global current_id, current_priority

        if user:
            if (user.password == password):
                if (user.priority == 1):
                    flash('Logged in succesfully', category='success')
                    login_user(user, remember=True)
                    current_id = user.id
                    current_priority = user.priority
                    return redirect(url_for('views.waiter_dashboard'))
                elif(user.priority == 2):
                    flash('Logged in succesfully', category='success')
                    login_user(user, remember=True)
                    current_id = user.id
                    current_priority = user.priority
                    return redirect(url_for('views.kitchen_dashboard'))
                else:
                    flash('Not allowed to login here, Try logging in here', category='error')
                    return redirect(url_for('auth.login'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('waiter_login.html', boolean=True)

@auth.route('/waiter_orders', methods=['GET', 'POST'])
def orders():
    """
    Displays orders for waiters in a table
    
    It loads data from class Order that is added from '/order'
    and list them in a table with different attributes.
    
    Attributes
    ----------
    item_list : list
        list of all menus in class Item
    order_list : list
        list of all Orders in class Order

    Returns
    -------
    Render_template
        order_page_1.html for order page,
        cart_price for total price,
        data for ordered items in cart
        food_img for images of selected menus
        item_list for list of all menus
        
    
    @author : Mashhood Manzoor
    @author : Hyunwoo Kim
    @author : Shing him Yip
    
    """
    
    item_list = []
    for x in range(1, len(food_img)):
        food_item = Item.query.filter_by(id=x).first()
        item_list.append(food_item)

    order_list = []
    root = Order.query.all()
    for x in root:
        order_list.append(x)

    for x in range(1, len(food_img)):
        if (str(x) + ' del') in request.form:
            flash('item deleted !', category='success')

            print(x)
            print(order_list)

            del_order = Order.query.filter_by(id=x).first()
            del_kitchen = Kitchen.query.filter_by(order_id=x).first()
            order_list.remove(del_order)
            db.session.delete(del_order)
            db.session.delete(del_kitchen)
            db.session.commit()


            return render_template('waiter_orders.html',
                                   order_list=order_list,
                                   item_list=item_list
                                   )

        if (str(x) + ' toKitchen') in request.form:
            sending = Order.query.filter_by(id=x).first()
            sending_name = Item.query.filter_by(id=sending.item_id).first().name

            sending.prepared = 1
            to_kitchen = Kitchen(waiter_id=current_id, item_name=sending_name, item_id=sending.item_id, 
                                 item_quantity=sending.item_quantity, order_id=sending.id)

            db.session.add(to_kitchen)
            db.session.commit()

            flash('order sent', category='success')
            return render_template('waiter_orders.html',
                                   order_list=order_list,
                                   item_list=item_list
                                   )

        if (str(x) + ' order-finished') in request.form:
            flash('Order finished!!!!!!!', category='success')
            sending = Order.query.filter_by(id=x).first()
            sending.prepared = 5
            db.session.commit()

            return render_template('waiter_orders.html',
                                   order_list=order_list,
                                   item_list=item_list
                                   )
    

    return render_template('waiter_orders.html',
                           order_list=order_list,
                           item_list=item_list
                           )
                        

@auth.route('/change_menu', methods=['GET', 'POST'])
def change_menu():
    """
    Allows waiters to make items available and unavailable

    It loads all of the items from the Item table
    and if a button is pressed to change it, it edits the status
    field of the item in the table called Item
    
    Attributes
    ----------
    data : list
        list of all items in the table Item
    item : field
        row of the item that needs to be changed


    Returns
    -------
    Render_template
        data which holds the menu
        
    @author : Mashhood Manzoor
    @author : Harveen Chada
    """
    data = Item.query.all()
    if request.method == 'POST':
        for x in range(50):
            if (str(x) + " hide") in request.form:
                item = Item.query.filter_by(id=x).first()
                db.session.add(item)
                item.is_available = False
                db.session.commit()
                flash("Changed", category='success')
            if (str(x) + " show") in request.form:
                item = Item.query.filter_by(id=x).first()
                db.session.add(item)
                item.is_available = True
                db.session.commit()
                flash("Changed", category='success')

    return render_template('change_menu.html', data=data)


@auth.route('/kitchen_dash', methods=['GET', 'POST'])
def kitchen():
    """
    Displays orders for kitchen staffs in a table
    
    It loads data from class Kitchen that is sent from '/orders'
    and list them in a table with different attributes.
    
    Attributes
    ----------
    item_list : list
        list of all menus in class Item
    kitchen_list : list
        list of all Orders in class Kitchen

    Returns
    -------
    Render_template
        kitchen_site.html for order page,
        food_img for images of selected menus,
        item_list for list of all menus,
        kitchen_list for list of all orders in kitchen
        
    
    @author : Hyunwoo Kim
    @author : Shing him Yip
    
    """
    item_list = []
    for x in range(1, len(food_img)):
        food_item = Item.query.filter_by(id=x).first()
        item_list.append(food_item)

    kitchen_list = []
    kitchen_order = Kitchen.query.all()
    for x in kitchen_order:
        kitchen_list.append(x)
    

    if request.method == 'POST':
        for x in range(50):
            if (str(x) + ' confirm_button_box') in request.form:
                flash('Order confirmed', category='success')
                selected_kitchen_order = Kitchen.query.filter_by(id=x).first()
                order_cooked = Order.query.filter_by(id=selected_kitchen_order.order_id).first()
                order_cooked.prepared = 2
                db.session.commit()

            if (str(x) + ' finished_button_box') in request.form:
                flash('Order Finished', category='success')
                selected_kitchen_order = Kitchen.query.filter_by(id=x).first()
                order_cooked = Order.query.filter_by(id=selected_kitchen_order.order_id).first()
                order_cooked.prepared = 3
                kitchen_list.remove(selected_kitchen_order)
                db.session.delete(selected_kitchen_order)
                db.session.commit()

            if (str(x) + ' call_waiter_to_delete') in request.form:
                flash('messages sending', category='success')
                selected_kitchen_order = Kitchen.query.filter_by(id=x).first()
                order_cooked = Order.query.filter_by(id=selected_kitchen_order.order_id).first()
                order_cooked.prepared = 4
                db.session.commit()


    return render_template('kitchen_dash.html',
                           item_list=item_list,
                           kitchen_list=kitchen_list,
                           food_img=food_img
                           )


@auth.route('/customer_checkout')
def checkout():

    
    """
    render the checkout dashboard page 

    Returns
    -------
    Return render_template function to render checkout.html template 
    
    @author : Harveen Chada
    
    """

    if request.method == 'POST':
        for x in range(50):
            if (str(x)) in request.form:
                order = Order.query.filter_by(id=x).first()
    
                order.paid = True
                db.session.add(order)
                db.session.commit()
                flash('thank you for payment', category='success')
                return render_template("customer_history.html")


    return render_template("customer_checkout.html")



@auth.route('/customer_history', methods=['GET', 'POST'])
def history():
    """
    Displays current users order history
    
    It loads all of the users orders and puts them in a table
    
    Attributes
    ----------
    order_list : list
        list to store orders
    root : list
        list of all of the users orders
 

    Returns
    -------
    Render_template
        order_list which is a list of the users orders
        
    
    @author : Mashhood Manzoor
    """
    if request.method == 'POST':
        for x in range(50):
            if (str(x)) in request.form:
                return render_template('customer_checkout.html', order = x)



    order_list = []
    global current_id
    root = Order.query.filter_by(user_id=current_id).all()
    for x in root:
        order_list.append(x)
    return render_template('customer_history.html', order_list=order_list)



