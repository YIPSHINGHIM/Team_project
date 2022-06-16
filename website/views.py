import os

from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    """
    renders the home page 

    Returns
    -------
    Return render_template function and render home.html template 
    Return the home page image list
    
    @author : Mashhood Manzoor
    @author : Shing Him Yip
    
    """
    home_page_img = []
    for file in os.listdir('website/static/images/home_page_img'):
        home_page_img.append(file)
    home_page_img.sort()

    return render_template("home.html",
                           home_page_img=home_page_img)


@views.route('/waiter_dashboard')
def waiter_dashboard():
    """
    render the waiter dashboard page 

    Returns
    -------
    Return render_template function to render waiter_dash.html template 
    
    @author : Harry Webster
    
    """
    return render_template("waiter_dash.html")

@views.route('/kitchen_dashboard')
def kitchen_dashboard():
    """
    render the kitchen dashboard page 

    Returns
    -------
    Return render_template function to render Kitchen_dash.html template 
    
    @author : Harry Webster
    
    """
    return render_template("kitchen_dash.html")

@views.route('/customer_about')
def about():
    """
    render the about page 

    Returns
    -------
    Return render_template function to render about.html template 
    
    @author : Harveen Chada 
    
    """
    return render_template("customer_about.html")



@views.route('/customer_thankyou')
def thankyou():
    """
    render the thank you page after contact

    Returns
    -------
    Return render_template function to render checkout.html template 
    
    @author : Harveen Chada
    
    """
    return render_template("customer_thankyou.html")
