from .models import Item


class cart():
    """
    A class used to represent a cart 

    Methods
    -------
    add_item(id)
        add the item to the cart list by using item id

    change_cart_value(id ,value)
        change the quantity in the cart

    remove_item(id)
        remove the item from the cart 

    in_cart()
        return the item is the cart

    cart_total()
        calculating the total price for all the item in the cart 
    """
    def __init__(self):
        """
        creates the cart(basket) as a dictionary structure
        @author : Mashhood Manzoor
        @author : Hyunwoo Kim

        """
        self.cart_items = {}

    def add_item(self, id):
        """
        adding item in to the cart

        Parameters
        ----------
        id : int
            the item id

        @author : Mashhood Manzoor
        @author : Hyunwoo Kim
        @author : Shing Him Yip

        """
        if id in self.cart_items:
            self.cart_items[id] += 1
        else:
            self.cart_items[id] = 1
        self.cart_total

    def change_cart_value(self,id,value):
        """
        changes the quantity in the cart

        Parameters
        ----------
        id : int
            the item id
        value : int
            the new quantity for the dish

        @author : Mashhood Manzoor
        @author : Hyunwoo Kim

        """
        self.cart_items[id]=value

    def remove_item(self, id):
        """
        remove the item by using item id 

        Parameters
        ----------
        id : int
            the item id
        
        @author : Mashhood Manzoor
       
        """
        del self.cart_items[id]

    def in_cart(self):
        """
        return the item in the cart 

        Returns
        -------
        Return the dictionary for the cart 
        
        @author : Mashhood Manzoor
       
        """
        return self.cart_items
    
    def clear_cart(self):
        """
        remove all the item in the cart 
        
        @author : Mashhood Manzoor
       
        """
        self.cart_items.clear()

    def cart_total(self):
        """
        calculating the total price for all the item in the cart

        Returns
        -------
        Return total price in the cart (float)
        
        @author : Hyunwoo Kim
        @author : Shing Him Yip
       
        """
        self.total = 0
        for x in self.cart_items:
            item = Item.query.filter_by(id=x).first()
            self.total = self.total + (item.price * self.cart_items[x])
        return round(self.total, 2)



