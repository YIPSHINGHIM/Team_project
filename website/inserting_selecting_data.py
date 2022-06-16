def initialise_data(app, filename):
    """
    It initialise the database data while user run the programme.

    Parameters
    ----------
    app : (flask.app.Flask)
        specific the flask app programme need to use 

    filename : (str)
        passing the txt file name to the programme 

    Returns
    -------
    Nothing will be returned

    """
    import logging

    from website import db

    from .models import Item, Trait, Type, User
    with app.app_context():
        with open(filename, 'r') as file:
            for line in file:
                data = line.strip().split(',')

                if filename == "website/resources/Type.txt":
                    # print("inserting Type data")
                    # print(data)
                    new_Type = Type(name=data[0])
                    db.session.add(new_Type)
                    db.session.commit()

                if filename == "website/resources/Item.txt":
                    # print("inserting Item data")
                    # print(data)
                    new_Item = Item(name=data[0],
                                    price=data[1],
                                    calories=data[2],
                                    type_id=data[3],
                                    is_vegetarian=data[4],
                                    is_alcoholic=data[5])

                    db.session.add(new_Item)
                    db.session.commit()

                if filename == "website/resources/user.txt":
                    # print("inserting Type data")
                    # print(data)
                    new_User = User(email=data[0], password=data[2], firstName=data[1],priority = data[3])
                    db.session.add(new_User)
                    db.session.commit()
                
                if filename == "website/resources/Trait.txt":
                    new_Trait = Trait(name=data[0])
                    db.session.add(new_Trait)
                    db.session.commit()
