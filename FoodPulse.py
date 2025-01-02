###################################
#
#           Food Pulse
#
#  A CMSC 127 Project by:
#
#   Abejay, Rhys Allen V.
#   Atayde, Patrick Josh P.
#   Cedillo, Kevin Lester M.
#
#
###################################


##### Importing required libraries
import mysql.connector
import pwinput
from tabulate import tabulate
from textwrap import dedent
from datetime import date

##### Connecting to the database
db = mysql.connector.connect(
    host = "localhost",
    user = "rhys",
    password = "127rhys",

    ### initialize database before running
    ### works without this
    # database = "foodsystem",
)

##### Create cursor object to execute SQL queries
dbcursor = db.cursor()

############################################### FUNCTIONS ##########################################################

##### FUNCTION: Creates the database and tables, if not created already
def create_db():
    # Create database
    dbcursor.execute('''
        CREATE DATABASE IF NOT EXISTS foodsystem;
    ''')

    # Use created database
    dbcursor.execute('''
        USE foodsystem;
    ''')

    # Create tables

    # user table
    dbcursor.execute('''
        CREATE TABLE IF NOT EXISTS user(
        username VARCHAR(20) PRIMARY KEY NOT NULL,
        email_address VARCHAR(50) NOT NULL,
        first_name VARCHAR(30) NOT NULL,
        middle_initial VARCHAR(1),
        last_name VARCHAR(30) NOT NULL,
        password VARCHAR(20) NOT NULL,
        CONSTRAINT user_email_address UNIQUE(email_address)
        );
    ''')

    # admin table
    dbcursor.execute('''
        CREATE TABLE IF NOT EXISTS admin(
        username VARCHAR(20), 
        admin_code INT(5) AUTO_INCREMENT, 
        CONSTRAINT admin_admin_code_uk UNIQUE(admin_code),
        CONSTRAINT admin_username_fk FOREIGN KEY(username) REFERENCES user(username)
        );
    ''')

    # food_establishment table
    dbcursor.execute('''
        CREATE TABLE IF NOT EXISTS food_establishment(
        business_id INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT,
        business_name VARCHAR(30) NOT NULL,
        address VARCHAR(50) NOT NULL,
        website VARCHAR(50),
        contact_number VARCHAR(15)
        );
    ''')

    # food_item table
    dbcursor.execute('''
        CREATE TABLE IF NOT EXISTS food_item(
        food_id INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT,
        food_name VARCHAR(50) NOT NULL,
        food_type ENUM("Meat", "Vegetables", "Appetizer", "Pasta", "Dessert", "Beverage", "Bread", "Others") NOT NULL,
        price DECIMAL(5,2) NOT NULL,
        description VARCHAR(200),
        business_id INT(5),
        CONSTRAINT food_item_business_id_fk FOREIGN KEY(business_id) REFERENCES food_establishment(business_id)
        );
    ''')

    # food_review table
    dbcursor.execute('''
        CREATE TABLE IF NOT EXISTS food_review(
        review_id INT(5) PRIMARY KEY NOT NULL AUTO_INCREMENT,
        review_text VARCHAR(200) NOT NULL,
        rating INT(1),
        date_of_review DATE NOT NULL DEFAULT CURDATE(),
        username VARCHAR(20),
        business_id INT(5),
        food_id INT(5),
        CONSTRAINT food_review_username_fk FOREIGN KEY(username) REFERENCES user(username),
        CONSTRAINT food_review_business_id_fk FOREIGN KEY(business_id) REFERENCES food_establishment(business_id),
        CONSTRAINT food_review_food_id_fk FOREIGN KEY(food_id) REFERENCES food_item(food_id)
        );
    ''')

##### Call the function create_db()
create_db()


##### FUNCTION: Outputs the user profile
##### ADD: Update profile option
def profile():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                 User Profile                  |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT * FROM user WHERE username = %s", (current_user, ))
        user = dbcursor.fetchall()

        print(f"|\tUsername: {user[0][0]}")
        print(f"|\tEmail Address: {user[0][1]}")
        print(f"|\tFirst Name: {user[0][2]}")
        print(f"|\tMiddle Initial: {user[0][3]}")
        print(f"|\tLast Name: {user[0][4]}")
        print(f"|\tPassword: {user[0][5]}")
        print("|                                               |")
        print("|          [1] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
        ''')

        profile = int(input("\nEnter number corresponding to your choice: "))

        if(profile == 1):
            break
        else:
            print("Input invalid. Please enter a valid number.")

############### Functions for Food Review ###############

##### FUNCTION: Adds food review to a food establishment directly to the database, including for user inputs.
def add_establishment_review(username,establishment):

    try:
        dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (establishment, ))
        business_id = dbcursor.fetchone()[0]

        review = input("\nEnter your review: ")
        while True:
            try:
                rating = int(input("\nEnter your rating from 1-5: "))
                if 1 <= rating <= 5:
                    break
                else:
                    print("Rating must be between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter an integer between 1 and 5.")
        
        current_date = date.today()

        query = "INSERT INTO food_review (review_text, rating, date_of_review, username, business_id) VALUES(%s,%s,%s,%s,%s)"
        values = (review, rating, current_date, username, business_id)
        
        dbcursor.execute(query, values)
        db.commit()

        print("Review added successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

##### FUNCTION: Adds food review to a food item directly to the database, including asking for user inputs
def add_item_review(username,establishment, food):

    try:
        dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (establishment, ))
        business_id = dbcursor.fetchone()[0]

        dbcursor.execute("SELECT food_id FROM food_item WHERE food_name = %s", (food, ))
        food_id = dbcursor.fetchone()[0]

        review = input("\nEnter your review: ")
        while True:
            try:
                rating = int(input("\nEnter your rating from 1-5: "))
                if 1 <= rating <= 5:
                    break
                else:
                    print("Rating must be between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter an integer between 1 and 5.")
        
        current_date = date.today()

        query = "INSERT INTO food_review (review_text, rating, date_of_review, username, business_id, food_id) VALUES(%s,%s,%s,%s,%s,%s)"
        values = (review, rating, current_date, username, business_id, food_id)
        
        dbcursor.execute(query, values)
        db.commit()

        print("Review added successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

##### FUNCTION: Menu aspect of adding a food review to an establishment, including printing out existing establishments and asking user inputs
def add_review_establishment():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            add_establishment_review(current_user,selected_establishment)
            
        else:
            print("Input invalid. Please enter a valid number.")

##### FUNCTION: Menu aspect of adding a food review to an item, including printing out existing establishments and their food items and asking user inputs
def add_review_item():
     while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            while True:
                selected_establishment = establishments[estab - 1][0]
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Available Food Items              |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
                business_id = dbcursor.fetchone()[0]

                dbcursor.execute("SELECT food_name FROM food_item WHERE business_id = %s", (business_id,))
                food_items = dbcursor.fetchall()

                num_food = len(food_items)

                for i, food in enumerate(food_items, start = 1):
                    print(f"|          [{i}] {food[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
''')
            
                food_choice = int(input("\nEnter number corresponding to your choice: "))

                if(food_choice == 0):
                    break
                elif(1 <= food_choice <= num_food):
                    selected_food = food_items[food_choice - 1][0]
                    print(f"You have selected {selected_food}!")

                    add_item_review(current_user,selected_establishment, selected_food)
                    
                else:
                    print("Input invalid. Please enter a valid number.")
                    
                    
        else:
            print("Input invalid. Please enter a valid number.")

##### FUNCTION: Main menu for adding a food review
def add_review():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|          Establishment or Food Item           |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Establishment                 |
|             [2] Food Item                     | 
|             [3] Go Back                       |                       
|                                               |
●-----------------------------------------------●
    ''')

        add_review = int(input("\nEnter number corresponding to your choice: "))

        if(add_review == 1):
            add_review_establishment()

        elif(add_review == 2):
            add_review_item()
            
        elif(add_review == 3):
            break
        else:
            print("Input invalid. Please enter a valid number.")

##### FUNCTION: Shows all food reviews created by the user
def show_review(username):

    try:
        query = """
        SELECT 
            fr.review_id,
            fr.review_text,
            fr.rating,
            fr.date_of_review,
            fe.business_name,
            fi.food_name
        FROM 
            food_review fr
        JOIN 
            food_establishment fe ON fr.business_id = fe.business_id
        LEFT JOIN 
            food_item fi ON fr.food_id = fi.food_id
        WHERE
            fr.username = %s
        ORDER BY 
            fr.review_id;
""" 
        values = (username,)

        dbcursor.execute(query,values)
        reviews = dbcursor.fetchall()

        # get all the columns of food review
        columns = [col[0] for col in dbcursor.description]

        print("\nFood Reviews you have created:")
        print(
            tabulate(
                reviews,
                headers=columns,
                tablefmt="grid"
            )
        )

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

##### FUNCTION: Updates a food review created by the user
def update_review(username):
    try:
        query = """
        SELECT 
            fr.review_id,
            fr.review_text,
            fr.rating,
            fr.date_of_review,
            fe.business_name,
            fi.food_name
        FROM 
            food_review fr
        JOIN 
            food_establishment fe ON fr.business_id = fe.business_id
        LEFT JOIN 
            food_item fi ON fr.food_id = fi.food_id
        WHERE
            fr.username = %s
        ORDER BY
            fr.review_id;
""" 
        values = (username,)

        dbcursor.execute(query,values)
        reviews = dbcursor.fetchall()

        # get all the columns of food review
        columns = [col[0] for col in dbcursor.description]

        print("\nFood Reviews you have created:")
        print(
            tabulate(
                reviews,
                headers=columns,
                tablefmt="grid"
            )
        )

        review_ids = [review[0] for review in reviews]

        selected = int(input("\nEnter the review id of the review you would like to update: "))

        if selected in review_ids:
            print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|           What would you like to edit?        |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Review Text                   |
|             [2] Rating                        |
|             [3] Both                          |
●-----------------------------------------------● 
                  ''')
            action = int(input("\nEnter number corresponding to your choice: "))

            if(action == 1):
                review = input("\nEnter your review: ")

                query = "UPDATE food_review SET review_text = %s WHERE review_id = %s"
                values = (review, selected)

                dbcursor.execute(query,values)
                db.commit()

                print("Review updated successfully!")

            elif(action == 2):
                while True:
                    try:
                        rating = int(input("\nEnter your rating from 1-5: "))
                        if 1 <= rating <= 5:
                            break
                        else:
                            print("Rating must be between 1 and 5.")
                    except ValueError:
                        print("Invalid input. Please enter an integer between 1 and 5.")
                
                query = "UPDATE food_review SET rating = %s WHERE review_id = %s"
                values = (rating, selected)

                dbcursor.execute(query,values)
                db.commit()

                print("Review updated successfully!")

            elif(action == 3):

                review = input("\nEnter your review: ")
                while True:
                    try:
                        rating = int(input("\nEnter your rating from 1-5: "))
                        if 1 <= rating <= 5:
                            break
                        else:
                            print("Rating must be between 1 and 5.")
                    except ValueError:
                        print("Invalid input. Please enter an integer between 1 and 5.")
                
                query = "UPDATE food_review SET review_text = %s, rating = %s WHERE review_id = %s"
                values = (review, rating, selected)

                dbcursor.execute(query,values)
                db.commit()

                print("Review updated successfully!")

            else:
                print("Invalid option.")

        else:
            print("Review ID not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

##### FUNCTION: Deletes a food review created by the user
def delete_review(username):
    try:
        query = """
        SELECT 
            fr.review_id,
            fr.review_text,
            fr.rating,
            fr.date_of_review,
            fe.business_name,
            fi.food_name
        FROM 
            food_review fr
        JOIN 
            food_establishment fe ON fr.business_id = fe.business_id
        LEFT JOIN 
            food_item fi ON fr.food_id = fi.food_id
        WHERE
            fr.username = %s
        ORDER BY
            fr.review_id;
""" 
        values = (username,)

        dbcursor.execute(query,values)
        reviews = dbcursor.fetchall()

        # get all the columns of food review
        columns = [col[0] for col in dbcursor.description]

        print("\nFood Reviews you have created:")
        print(
            tabulate(
                reviews,
                headers=columns,
                tablefmt="grid"
            )
        )

        review_ids = [review[0] for review in reviews]

        to_delete = int(input("\nEnter the review id of the review you would like to delete: "))

        if to_delete in review_ids:
            delete_query = "DELETE FROM food_review WHERE review_id = %s;"
            delete_values = (to_delete,)
            dbcursor.execute(delete_query, delete_values)
            db.commit()
            print("Review deleted successfully!")
        else:
            print("Review ID not found. No review deleted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

############### Functions for Food Establishment ###############

###### FUNCTION: Shows all existing food establishments (report 1)
def view_establishments():
    dbcursor.execute("SELECT * FROM food_establishment")
    establishments = dbcursor.fetchall()
    # get all the columns of food establishment
    dbcursor.execute("SHOW COLUMNS FROM food_establishment")
    columns = dbcursor.fetchall()
    columns = [col[0] for col in columns]

    print("\nAll Food Establishments:")
    print(
        tabulate(
            establishments,
            headers=columns,
            tablefmt="grid"
        )
    )

###### FUNCTION: Adds a food establishment
###### ADMIN-ONLY
def add_establishment(username):
    try:
        print("\nChecking for admin privileges...")

        query = "SELECT username FROM admin WHERE username = %s"
        value = (username, )

        dbcursor.execute(query, value)
        admin = dbcursor.fetchall()

        admin = len(admin)

        if(admin == 1):
            print("Adding an establishment...")

            bname = input("\nEnter the business name: ")
            address = input("\nEnter the business address: ")
            website = input("\nEnter the business website: ")
            contact = input("\nEnter the business contact number: ")

            query = "INSERT INTO food_establishment (business_name, address, website, contact_number) VALUES (%s, %s, %s, %s)"
            values = (bname, address, website, contact)

            dbcursor.execute(query, values)
            db.commit()

            print("\nSuccessfully added food establishment " + bname + "!")

        else:
            print("\nYou do not have permission to add an establishment.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

###### FUNCTION: Updates a food establishment
###### ADMIN-ONLY
def update_establishment(username):
    try:
        print("\nChecking for admin privileges...")

        query = "SELECT username FROM admin WHERE username = %s"
        value = (username, )

        dbcursor.execute(query, value)
        admin = dbcursor.fetchall()

        admin = len(admin)

        if(admin == 1):
            while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_name FROM food_establishment")
                establishments = dbcursor.fetchall()

                num_establishments = len(establishments)

                for i, establishment in enumerate(establishments, start = 1):
                    print(f"|          [{i}] {establishment[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
        ''')
                
                estab = int(input("\nEnter number corresponding to your choice: "))

                if(estab == 0):
                    break
                elif(1 <= estab <= num_establishments):
                    selected_establishment = establishments[estab - 1][0]
                    print(f"You have selected {selected_establishment}!")

                    print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|           What would you like to edit?        |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Business Name                 |
|             [2] Address                       |
|             [3] Website                       |
|             [4] Contact Number                |
|             [5] All                           |
●-----------------------------------------------● 
                  ''')
                    
                    action = int(input("\nEnter number corresponding to your choice: "))
                    
                    if(action == 1):
                        bname = input("\nEnter the business name: ")

                        query = "UPDATE food_establishment SET business_name = %s WHERE business_name = %s"
                        values = (bname, selected_establishment)

                        dbcursor.execute(query, values)
                        db.commit()

                        print("\nSuccessfully updated food establishment " + bname + "!")

                    elif(action == 2):
                        address = input("\nEnter the business address: ")

                        query = "UPDATE food_establishment SET address = %s WHERE business_name = %s"
                        values = (address, selected_establishment)

                        dbcursor.execute(query, values)
                        db.commit()

                        print("\nSuccessfully updated food establishment " + bname + "!")

                    elif(action == 3):
                        website = input("\nEnter the business website: ")

                        query = "UPDATE food_establishment SET website = %s WHERE business_name = %s"
                        values = (website, selected_establishment)

                        dbcursor.execute(query, values)
                        db.commit()

                        print("\nSuccessfully updated food establishment " + bname + "!")

                    elif(action == 4):
                        contact = input("\nEnter the business contact number: ")

                        query = "UPDATE food_establishment SET contact_number = %s WHERE business_name = %s"
                        values = (contact, selected_establishment)

                        dbcursor.execute(query, values)
                        db.commit()

                        print("\nSuccessfully updated food establishment " + bname + "!")

                    elif(action == 5):
                        bname = input("\nEnter the business name: ")
                        address = input("\nEnter the business address: ")
                        website = input("\nEnter the business website: ")
                        contact = input("\nEnter the business contact number: ")

                        query = "UPDATE food_establishment SET business_name = %s , address = %s , website = %s , contact_number = %s WHERE business_name = %s"
                        values = (bname, address, website, contact,selected_establishment)

                        dbcursor.execute(query, values)
                        db.commit()

                        print("\nSuccessfully updated food establishment " + bname + "!")
                    else:
                        print("Invalid option.")
                    
                else:
                    print("Input invalid. Please enter a valid number.")

        else:
            print("\nYou do not have permission to update an establishment.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

###### FUNCTION: Deletes a food establishment
###### ADMIN-ONLY
def delete_establishment(username):
    try:
        print("\nChecking for admin privileges...")

        query = "SELECT username FROM admin WHERE username = %s"
        value = (username, )

        dbcursor.execute(query, value)
        admin = dbcursor.fetchall()

        admin = len(admin)

        if(admin == 1):
            while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_name FROM food_establishment")
                establishments = dbcursor.fetchall()

                num_establishments = len(establishments)

                for i, establishment in enumerate(establishments, start = 1):
                    print(f"|          [{i}] {establishment[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
        ''')
                
                estab = int(input("\nEnter number corresponding to your choice: "))

                if(estab == 0):
                    break
                elif(1 <= estab <= num_establishments):
                    selected_establishment = establishments[estab - 1][0]
                    print(f"You have selected {selected_establishment}!")

                    print(f"Are you sure you want to delete {selected_establishment}?")

                    print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                   Delete ?                    |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Yes                           |
|             [2] No                            |                      
|                                               |
●-----------------------------------------------●
                    ''')

                    confirm = int(input("\nEnter number corresponding to your choice: "))

                    if(confirm == 1):
                        delete_query = "DELETE FROM food_establishment WHERE business_name = %s;"
                        delete_values = (selected_establishment,)
                        dbcursor.execute(delete_query, delete_values)
                        db.commit()
                        print(f"Food establishment {selected_establishment} deleted successfully!")

                    elif(confirm == 2):
                        print(f"Food establishment {selected_establishment} not deleted.")

                    else:
                        print("\nInvalid input.")


                else:
                    print("Input invalid. Please enter a valid number.")

        else:
            print("\nYou do not have permission to delete an establishment.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

############### Functions for Food Item ###############

###### FUNCTION: Shows all existing food items across all existing food establishments
def view_foods():
    dbcursor.execute('''
        SELECT fi.food_id, fi.food_name, fi.food_type, fi.price, fi.description, fe.business_name
        FROM food_item fi
        JOIN food_establishment fe ON fi.business_id = fe.business_id
    ''')
    food_items = dbcursor.fetchall()

    # get all the columns of food_item
    columns = [col[0] for col in dbcursor.description]

    print("\nAll Food Items:")
    print(
        tabulate(
            food_items,
            headers=columns,
            tablefmt="grid"
        )
    )

###### FUNCTION: Adds a food item on a food establishment
###### ADMIN-ONLY
def add_food(username):
    try:
        print("\nChecking for admin privileges...")

        query = "SELECT username FROM admin WHERE username = %s"
        value = (username, )

        dbcursor.execute(query, value)
        admin = dbcursor.fetchall()

        admin = len(admin)

        if(admin == 1):

             while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_name FROM food_establishment")
                establishments = dbcursor.fetchall()

                num_establishments = len(establishments)

                for i, establishment in enumerate(establishments, start = 1):
                    print(f"|          [{i}] {establishment[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
        ''')
                
                estab = int(input("\nEnter number corresponding to your choice: "))

                if(estab == 0):
                    break
                elif(1 <= estab <= num_establishments):
                    selected_establishment = establishments[estab - 1][0]
                    print(f"You have selected {selected_establishment}!")

                    dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment,))
                    business_id = dbcursor.fetchone()[0]

                    print("Adding an food item...")

                    fname = input("\nEnter the food name: ")

                    ### Type validity for this
                    ftype = input("\nEnter the food type ('Meat', 'Vegetables', 'Appetizer', 'Pasta', 'Dessert', 'Beverage', 'Bread', 'Others'): ")
                    price = float(input("\nEnter the food price: "))
                    description = input("\nEnter the food description: ")

                    query = "INSERT INTO food_item (food_name, food_type, price, description, business_id) VALUES (%s, %s, %s, %s, %s)"
                    values = (fname, ftype, price, description, business_id)

                    dbcursor.execute(query, values)
                    db.commit()

                    print("\nSuccessfully added food " + fname  + " to the "+ selected_establishment)

        else:
            print("\nYou do not have permission to add a food item.")


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

###### FUNCTION: Updates a food item on a food establishment
###### ADMIN-ONLY
def update_food(username):
    try:
        print("\nChecking for admin privileges...")

        query = "SELECT username FROM admin WHERE username = %s"
        value = (username, )

        dbcursor.execute(query, value)
        admin = dbcursor.fetchall()

        admin = len(admin)

        if(admin == 1):
            while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_name FROM food_establishment")
                establishments = dbcursor.fetchall()

                num_establishments = len(establishments)

                for i, establishment in enumerate(establishments, start = 1):
                    print(f"|          [{i}] {establishment[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
        ''')
                
                estab = int(input("\nEnter number corresponding to your choice: "))

                if(estab == 0):
                    break
                elif(1 <= estab <= num_establishments):

                    selected_establishment = establishments[estab - 1][0]
                    print(f"You have selected {selected_establishment}!")

                    while True:
                        selected_establishment = establishments[estab - 1][0]
                        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Available Food Items              |           
|  ==========================================   | ''')               
                        print("|                                               |")

                        dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
                        business_id = dbcursor.fetchone()[0]

                        dbcursor.execute("SELECT food_name FROM food_item WHERE business_id = %s", (business_id,))
                        food_items = dbcursor.fetchall()

                        num_food = len(food_items)

                        for i, food in enumerate(food_items, start = 1):
                            print(f"|          [{i}] {food[0]}")

                        print("|          [0] Go Back                          |")
                        print('''|                                               |
●-----------------------------------------------●
        ''')
                    
                        food_choice = int(input("\nEnter number corresponding to your choice: "))
                        if(food_choice == 0):
                            break
                        elif(1 <= food_choice <= num_food):

                            selected_food = food_items[food_choice - 1][0]
                            print(f"You have selected {selected_food}!")

                            print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|           What would you like to edit?        |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Food Name                     |
|             [2] Food Type                     |
|             [3] Price                         |
|             [4] Description                   |
|             [5] All                           |
●-----------------------------------------------● 
                    ''')
                        
                            action = int(input("\nEnter number corresponding to your choice: "))
                            
                            if(action == 1):
                                fname = input("\nEnter the food name: ")

                                query = "UPDATE food_item SET food_name = %s WHERE food_name = %s"
                                values = (fname, selected_food)

                                dbcursor.execute(query, values)
                                db.commit()

                                print("\nSuccessfully updated food name of " + selected_food + "from "+ selected_establishment)

                            elif(action == 2):
                                ftype = input("\nEnter the food type ('Meat', 'Vegetables', 'Appetizer', 'Pasta', 'Dessert', 'Beverage', 'Bread', 'Others'): ")

                                query = "UPDATE food_item SET food_type = %s WHERE food_name = %s"
                                values = (ftype, selected_food)

                                dbcursor.execute(query, values)
                                db.commit()

                                print("\nSuccessfully updated food type of " + selected_food + "from "+ selected_establishment)

                            elif(action == 3):
                                price = input("\nEnter the food price: ")

                                query = "UPDATE food_item SET price = %s WHERE food_name = %s"
                                values = (price, selected_food)

                                dbcursor.execute(query, values)
                                db.commit()

                                print("\nSuccessfully updated food price of " + selected_food + "from "+ selected_establishment)

                            elif(action == 4):
                                description = input("\nEnter the food description: ")

                                query = "UPDATE food_type SET description = %s WHERE food_name = %s"
                                values = (description, selected_food)

                                dbcursor.execute(query, values)
                                db.commit()

                                print("\nSuccessfully updated food description of " + selected_food +  "from "+ selected_establishment)

                            elif(action == 5):
                                fname = input("\nEnter the food name: ")
                                ftype = input("\nEnter the food type ('Meat', 'Vegetables', 'Appetizer', 'Pasta', 'Dessert', 'Beverage', 'Bread', 'Others'): ")
                                price = input("\nEnter the food price: ")
                                description = input("\nEnter the food description: ")

                                query = "UPDATE food_item SET food_name = %s , food_type = %s , price = %s , description = %s WHERE food_name = %s"
                                values = (fname, ftype, price, description, selected_food)

                                dbcursor.execute(query, values)
                                db.commit()

                                print("\nSuccessfully updated food item " + selected_food + "from "+ selected_establishment)
                            else:
                                print("Invalid option.")
                            
                        else:
                            print("Input invalid. Please enter a valid number.")

        else:
            print("\nYou do not have permission to update a food item.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

###### FUNCTION: Deletes a food item on a food establishment
###### ADMIN-ONLY
def delete_food(username):
    try:
        print("\nChecking for admin privileges...")

        query = "SELECT username FROM admin WHERE username = %s"
        value = (username, )

        dbcursor.execute(query, value)
        admin = dbcursor.fetchall()

        admin = len(admin)

        if(admin == 1):
            while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_name FROM food_establishment")
                establishments = dbcursor.fetchall()

                num_establishments = len(establishments)

                for i, establishment in enumerate(establishments, start = 1):
                    print(f"|          [{i}] {establishment[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
        ''')
                
                estab = int(input("\nEnter number corresponding to your choice: "))

                if(estab == 0):
                    break
                elif(1 <= estab <= num_establishments):

                    selected_establishment = establishments[estab - 1][0]
                    print(f"You have selected {selected_establishment}!")

                    while True:
                        selected_establishment = establishments[estab - 1][0]
                        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Available Food Items              |           
|  ==========================================   | ''')               
                        print("|                                               |")

                        dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
                        business_id = dbcursor.fetchone()[0]

                        dbcursor.execute("SELECT food_name FROM food_item WHERE business_id = %s", (business_id,))
                        food_items = dbcursor.fetchall()

                        num_food = len(food_items)

                        for i, food in enumerate(food_items, start = 1):
                            print(f"|          [{i}] {food[0]}")

                        print("|          [0] Go Back                          |")
                        print('''|                                               |
●-----------------------------------------------●
        ''')
                    
                        food_choice = int(input("\nEnter number corresponding to your choice: "))
                        if(food_choice == 0):
                            break
                        elif(1 <= food_choice <= num_food):

                            selected_food = food_items[food_choice - 1][0]
                            print(f"You have selected {selected_food}!")

                            print(f"Are you sure you want to delete {selected_food}?")

                            print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                   Delete ?                    |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Yes                           |
|             [2] No                            |                      
|                                               |
●-----------------------------------------------●
                            ''')

                            confirm = int(input("\nEnter number corresponding to your choice: "))

                            if(confirm == 1):
                                delete_query = "DELETE FROM food_item WHERE food_name= %s;"
                                delete_values = (selected_food,)
                                dbcursor.execute(delete_query, delete_values)
                                db.commit()
                                print(f"Food item {selected_food} deleted from {selected_establishment} successfully!")

                            elif(confirm == 2):
                                print(f"Food item {selected_food} from {selected_establishment} not deleted.")

                            else:
                                print("\nInvalid input.")

                        else:
                            print("Input invalid. Please enter a valid number.")

        else:
            print("\nYou do not have permission to delete a food item.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()

############### Functions for Reports ###############

###### FUNCTION: Show food reviews on food establishment (report 2)
def show_establishment_reviews():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s",
                                    (selected_establishment,))
            business_id = dbcursor.fetchone()[0]

            dbcursor.execute("SELECT * FROM food_review WHERE business_id = %s", (business_id,))
            reviews = dbcursor.fetchall()

            # get all the columns of food review
            dbcursor.execute("SHOW COLUMNS FROM food_review")
            columns = dbcursor.fetchall()
            columns = [col[0] for col in columns]

            print("\nFood Reviews For An Establishment:")
            print(
                tabulate(
                    reviews,
                    headers=columns,
                    tablefmt="grid"
                )
            )
            
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Show food reviews on food establishment (report 2)
def show_item_reviews():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            while True:
                selected_establishment = establishments[estab - 1][0]
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Available Food Items              |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
                business_id = dbcursor.fetchone()[0]

                dbcursor.execute("SELECT food_name FROM food_item WHERE business_id = %s", (business_id,))
                food_items = dbcursor.fetchall()

                num_food = len(food_items)

                for i, food in enumerate(food_items, start = 1):
                    print(f"|          [{i}] {food[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
''')
            
                food_choice = int(input("\nEnter number corresponding to your choice: "))

                if(food_choice == 0):
                    break
                elif(1 <= food_choice <= num_food):
                    selected_food = food_items[num_food - 1][0]
                    print(f"You have selected {selected_food}!")

                    dbcursor.execute("SELECT food_id FROM food_item WHERE food_name = %s", (selected_food, ))
                    food_id = dbcursor.fetchone()[0]

                    dbcursor.execute("SELECT * FROM food_review WHERE food_id = %s", (food_id,))
                    reviews = dbcursor.fetchall()

                    # get all the columns of food review
                    dbcursor.execute("SHOW COLUMNS FROM food_review")
                    columns = dbcursor.fetchall()
                    columns = [col[0] for col in columns]

                    print("\nFood Reviews For A Food Item:")
                    print(
                        tabulate(
                            reviews,
                            headers=columns,
                            tablefmt="grid"
                        )
                    )
                    
                else:
                    print("Input invalid. Please enter a valid number.")
            
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Menu aspect for (report 2)
def view_food_review():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|          Establishment or Food Item           |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Establishment                 |
|             [2] Food Item                     | 
|             [3] Go Back                       |                       
|                                               |
●-----------------------------------------------●
    ''')

        view_review = int(input("\nEnter number corresponding to your choice: "))

        if(view_review == 1):
            show_establishment_reviews()

        elif(view_review == 2):
            show_item_reviews()
            
        elif(view_review == 3):
            break
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Show food items on food establishment (report 3)
def view_establishment_items():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            selected_establishment = establishments[estab - 1][0]

            dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
            business_id = dbcursor.fetchone()[0]

            dbcursor.execute("SELECT * FROM food_item WHERE business_id = %s", (business_id,))
            food_items = dbcursor.fetchall()
            
            # get all the columns of food item
            dbcursor.execute("SHOW COLUMNS FROM food_item")
            columns = dbcursor.fetchall()
            columns = [col[0] for col in columns]

            print("\nFood Items From An Establishment:")
            print(
                tabulate(
                    food_items,
                    headers=columns,
                    tablefmt="grid"
                )
            )  
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Show food items on food establishment, ordered by price (report 7)
def view_establishment_items_ordered():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            selected_establishment = establishments[estab - 1][0]
            dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
            business_id = dbcursor.fetchone()[0]

            print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                 Ordering                      |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Cheapest to Priciest          |
|             [2] Priciest to Cheapest          |                     
|                                               |
●-----------------------------------------------●
    ''')

            view_review = int(input("\nEnter number corresponding to your choice: "))

            if(view_review == 1):
                dbcursor.execute("SELECT * FROM food_item WHERE business_id = %s ORDER BY price ASC", (business_id,))
                food_items = dbcursor.fetchall()
                
                # get all the columns of food item
                dbcursor.execute("SHOW COLUMNS FROM food_item")
                columns = dbcursor.fetchall()
                columns = [col[0] for col in columns]

                print("\nFood Items From An Establishment:")
                print(
                    tabulate(
                        food_items,
                        headers=columns,
                        tablefmt="grid"
                    )
                )

            elif(view_review == 2):
                dbcursor.execute("SELECT * FROM food_item WHERE business_id = %s ORDER BY price DESC", (business_id,))
                food_items = dbcursor.fetchall()
                
                # get all the columns of food item
                dbcursor.execute("SHOW COLUMNS FROM food_item")
                columns = dbcursor.fetchall()
                columns = [col[0] for col in columns]

                print("\nFood Items From An Establishment:")
                print(
                    tabulate(
                        food_items,
                        headers=columns,
                        tablefmt="grid"
                    )
                )
            else:
                print("Input invalid. Please enter a valid number.")

        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Show recent (within a month) food reviews on food establishment (report 5)
def show_establishment_reviews_recent(month):
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s",
                                    (selected_establishment,))
            business_id = dbcursor.fetchone()[0]

            dbcursor.execute("SELECT * FROM food_review WHERE business_id = %s AND MONTH(date_of_review) = %s", (business_id,month))
            reviews = dbcursor.fetchall()

            # get all the columns of food review
            dbcursor.execute("SHOW COLUMNS FROM food_review")
            columns = dbcursor.fetchall()
            columns = [col[0] for col in columns]

            print("\nFood Reviews For An Establishment:")
            print(
                tabulate(
                    reviews,
                    headers=columns,
                    tablefmt="grid"
                )
            )
            
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Show recent (within a month) food reviews on food establishment (report 5)
def show_item_reviews_recent(month):
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            while True:
                selected_establishment = establishments[estab - 1][0]
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Available Food Items              |           
|  ==========================================   | ''')               
                print("|                                               |")

                dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
                business_id = dbcursor.fetchone()[0]

                dbcursor.execute("SELECT food_name FROM food_item WHERE business_id = %s", (business_id,))
                food_items = dbcursor.fetchall()

                num_food = len(food_items)

                for i, food in enumerate(food_items, start = 1):
                    print(f"|          [{i}] {food[0]}")

                print("|          [0] Go Back                          |")
                print('''|                                               |
●-----------------------------------------------●
''')
            
                food_choice = int(input("\nEnter number corresponding to your choice: "))

                if(food_choice == 0):
                    break
                elif(1 <= food_choice <= num_food):
                    selected_food = food_items[num_food - 1][0]
                    print(f"You have selected {selected_food}!")

                    dbcursor.execute("SELECT food_id FROM food_item WHERE food_name = %s", (selected_food, ))
                    food_id = dbcursor.fetchone()[0]

                    dbcursor.execute("SELECT * FROM food_review WHERE food_id = %s AND MONTH(date_of_review) = %s", (food_id, month))
                    reviews = dbcursor.fetchall()

                    # get all the columns of food review
                    dbcursor.execute("SHOW COLUMNS FROM food_review")
                    columns = dbcursor.fetchall()
                    columns = [col[0] for col in columns]

                    print("\nFood Reviews For A Food Item:")
                    print(
                        tabulate(
                            reviews,
                            headers=columns,
                            tablefmt="grid"
                        )
                    )
                    
                else:
                    print("Input invalid. Please enter a valid number.")
            
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Menu aspect for (report 5)
def recent_reviews():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|          Establishment or Food Item           |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Establishment                 |
|             [2] Food Item                     | 
|             [3] Go Back                       |                       
|                                               |
●-----------------------------------------------●
    ''')

        view_review = int(input("\nEnter number corresponding to your choice: "))

        if(view_review == 1):
            month = input("Enter month to search (e.g. 1-12 ): ")
            show_establishment_reviews_recent(month)

        elif(view_review == 2):
            month = input("Enter month to search (e.g. 1-12 ): ")
            show_item_reviews_recent(month)
            
        elif(view_review == 3):
            break
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Show food establishments with high average rating (report 6)
def recommended_establishments():
    dbcursor.execute(
        "SELECT business_name, AVG(rating) FROM food_review "
        "NATURAL JOIN food_establishment GROUP BY business_name HAVING AVG(rating) >= 4"
    )
    establishments = dbcursor.fetchall()

    # get all the columns of food establishment
    dbcursor.execute("SHOW COLUMNS FROM food_establishment")
    columns = dbcursor.fetchall()
    columns = [col[0] for col in columns]

    print("\nEstablishments with High Average Rating:")
    print(
        tabulate(
            establishments,
            headers=columns,
            tablefmt="grid"
        )
    )

###### FUNCTION: Search food items from any establishment based on a given price range and/or food type (report 8)
def search_items():
    print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|    Search Food Items by Price or Food Type    |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Price Range                   |
|             [2] Food Type                     |   
|             [3] Both                          |                      
|                                               |
●-----------------------------------------------●
                                                ''')
    option = int(input("Enter number corresponding to your choice: "))
    if option == 1:
        min_price = float(input("Enter minimum price: "))
        max_price = float(input("Enter maximum price: "))
        dbcursor.execute(
            "SELECT fi.food_name, fi.food_type, fi.price, fi.description, fe.business_name FROM food_item fi NATURAL JOIN food_establishment fe WHERE price BETWEEN %s AND %s",
            (min_price, max_price)
        )
        items = dbcursor.fetchall()

        # get all the columns of food item
        columns = [col[0] for col in dbcursor.description]

        print("\nFood Items of Price Range:")
        print(
            tabulate(
                items,
                headers=columns,
                tablefmt="grid"
            )
        )

    elif option == 2:
        # search by food type
        food_type = input("Enter food type ('Meat', 'Vegetables', 'Appetizer', 'Pasta', 'Dessert', 'Beverage', 'Bread', 'Others'): ")
        dbcursor.execute(
            "SELECT fi.food_name, fi.food_type, fi.price, fi.description, fe.business_name FROM food_item fi NATURAL JOIN food_establishment fe WHERE food_type = %s",
            (food_type,)
        )
        items = dbcursor.fetchall()

        # get all the columns of food item
        columns = [col[0] for col in dbcursor.description]

        print("\nFood Items of Food Type:")
        print(
            tabulate(
                items,
                headers=columns,
                tablefmt="grid"
            )
        )
    elif option == 3:
        min_price = float(input("Enter minimum price: "))
        max_price = float(input("Enter maximum price: "))
        food_type = input("Enter food type ('Meat', 'Vegetables', 'Appetizer', 'Pasta', 'Dessert', 'Beverage', 'Bread', 'Others'): ")
        
        query = "SELECT fi.food_name, fi.food_type, fi.price, fi.description, fe.business_name FROM food_item fi NATURAL JOIN food_establishment fe WHERE (price BETWEEN %s AND %s) AND food_type = %s"
        values = (min_price, max_price, food_type)
        dbcursor.execute(query, values)

        items = dbcursor.fetchall()

        # get all the columns of food item
        columns = [col[0] for col in dbcursor.description]

        print("\nFood Items of Food Type:")
        print(
            tabulate(
                items,
                headers=columns,
                tablefmt="grid"
            )
        )


    else:
        print("Input invalid. Please enter a valid number.")

###### FUNCTION: Search food items from an establishment based on a food type (report 4)
def search_establishment_items():
    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   | ''')               
        print("|                                               |")

        dbcursor.execute("SELECT business_name FROM food_establishment")
        establishments = dbcursor.fetchall()

        num_establishments = len(establishments)

        for i, establishment in enumerate(establishments, start = 1):
            print(f"|          [{i}] {establishment[0]}")

        print("|          [0] Go Back                          |")
        print('''|                                               |
●-----------------------------------------------●
''')
        
        estab = int(input("\nEnter number corresponding to your choice: "))

        if(estab == 0):
            break
        elif(1 <= estab <= num_establishments):
            selected_establishment = establishments[estab - 1][0]
            print(f"You have selected {selected_establishment}!")

            food_type = input("Enter food type ('Meat', 'Vegetables', 'Appetizer', 'Pasta', 'Dessert', 'Beverage', 'Bread', 'Others'): ")

            selected_establishment = establishments[estab - 1][0]

            dbcursor.execute("SELECT business_id FROM food_establishment WHERE business_name = %s", (selected_establishment, ))
            business_id = dbcursor.fetchone()[0]

            dbcursor.execute("SELECT * FROM food_item WHERE business_id = %s AND food_type = %s", (business_id, food_type))
            food_items = dbcursor.fetchall()
            
            # get all the columns of food item
            dbcursor.execute("SHOW COLUMNS FROM food_item")
            columns = dbcursor.fetchall()
            columns = [col[0] for col in columns]

            print("\nFood Items From An Establishment:")
            print(
                tabulate(
                    food_items,
                    headers=columns,
                    tablefmt="grid"
                )
            )

            
        else:
            print("Input invalid. Please enter a valid number.")

###### FUNCTION: Menu aspect of the reports to be generated.
def reports():

    while True:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                   Reports                     |           
|  ==========================================   |               
|  Options:                                     |
|             [1] View all Food Establishments  |
|             [2] View Food Reviews on Food     |
|                 Establishment/Item            |
|             [3] View Food Items of Food       |
|                 Establishment                 |
|             [4] View Food Items of Food Items |
|                 Belonging to a Food Type      |
|             [5] View Reviews within a Month   |
|             [6] View Establishments with      |
|                 High Average Rating           |
|             [7] View All Food Items From      | 
|                 Establishment Order By Price  |
|             [8] Search Food Items by Price    |
|                 or Food Type                  |    
|             [9] Go Back                       |                   
|                                               |
●-----------------------------------------------●
''')
        option = int(input("Enter number corresponding to your choice: "))

        if(option == 1):
            view_establishments()
        elif(option == 2):
            view_food_review()
        elif(option == 3):
            view_establishment_items()
        elif(option == 4):
            search_establishment_items()
        elif(option == 5):
            recent_reviews()
        elif(option == 6):
            recommended_establishments()
        elif(option == 7):
            view_establishment_items_ordered()
        elif(option == 8):
            search_items()
        elif(option == 9):
            break
        else:
            print("Input invalid. Please enter a valid number.")


############################################### UI ##########################################################

current_user = "none"
login_flag = True


##### LOGGING-IN
while True:
    try:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|            Welcome to Food Pulse!             |
|        A Food Review Management System        |       
|  ==========================================   |               
|                                               |
|             [1] Login                         |
|             [2] Create Account                |
|             [3] Exit                          |
|                                               |
●-----------------------------------------------●
              ''')
        
        choice = int(input("Enter number corresponding to your choice: "))

        ### Logging-in an existing user
        if(choice == 1):
            print("\nEnter your credentials: ")
            username = input("Username: ")
            password = pwinput.pwinput(prompt = 'Password: ')

            dbcursor.execute("SELECT * FROM user WHERE username = %s", (username, ))
            user = dbcursor.fetchone() 

            if (user):
                dbcursor.execute("SELECT password FROM user WHERE username = %s", (username,))
                user_pw = dbcursor.fetchone()[0]

                if password == user_pw:
                    current_user = username
                    print(f"Successfully logged in as " + current_user + "!")
                    break
                else:
                    print("You have entered an invalid password.")

            else:
                print("Username does not exist. Enter a correct username or create an account.")

        ### Creating a new user
        elif(choice == 2):
            print("\nLet's get to know each other, fellow food surveyor!")
            username = input("Username: ")
            email_address = input("Email Address: ")
            first_name = input("First Name: ")
            middle_initial = input("Middle Initial: ")
            last_name = input("Last Name: ")
            password = pwinput.pwinput(prompt = "Password: ")

            dbcursor.execute("INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s)", (username, email_address, first_name, middle_initial, last_name, password,))
            db.commit()

            print("Successfully created user " + username + "!")
            print("Please login using the credentials you have provided.")

        elif (choice == 3):
            print("Goodbye! See you next time.")
            login_flag = False
            break
    
        else:
            print("Input invalid. Please enter a valid number corresponding to your desired action.")
            continue

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()


##### MAIN MENU
while login_flag:
    try:
        print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                 Food Pulse!                   |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Food Review                   |
|             [2] Food Establishments           |
|             [3] Food Items                    |
|             [4] Reports                       |
|             [5] Profile                       |     
|             [6] Exit                          |                 
|                                               |
●-----------------------------------------------●
              ''')
        
        choice = int(input("Enter number corresponding to your choice: "))

        #### Food review related functions
        if (choice == 1):
            while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                 Food Reviews                  |           
|  ==========================================   |               
|  Options:                                     |
|             [1] Add a Food Review             |
|             [2] Update a Food Review          |
|             [3] Delete a Food Review          |
|             [4] Show Food Reviews             |
|             [5] Go Back                       |     
|                                               |
●-----------------------------------------------●
              ''')
            
                review_choice = int(input("\nEnter number corresponding to your choice: "))

                if(review_choice == 1):
                    add_review()
                elif(review_choice == 2):
                    update_review(current_user)
                elif(review_choice == 3):
                    delete_review(current_user)
                elif(review_choice == 4):
                    show_review(current_user)
                elif(review_choice == 5):
                    break
                else:
                    print("Input invalid. Please enter a valid number.")

            
        #### Food establishment related functions
        elif(choice == 2):
            while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|             Food Establishments               |           
|  ==========================================   |               
|  Options:                                     |
|             [1] View All Food Establishments  |
|             [2] Add a Food Establishment      |
|             [3] Update a Food Establishment   |
|             [4] Delete a Food Establishment   |
|             [5] Go Back                       |     
|                                               |
●-----------------------------------------------●
              ''')
            
                estab_choice = int(input("\nEnter number corresponding to your choice: "))

                if(estab_choice == 1):
                    view_establishments()
                elif(estab_choice == 2):
                    add_establishment(current_user)
                elif(estab_choice == 3):
                    update_establishment(current_user)
                elif(estab_choice == 4):
                    delete_establishment(current_user)
                elif(estab_choice == 5):
                    break;
                else:
                    print("Input invalid. Please enter a valid number.")

            
        #### Food item related functions
        elif(choice == 3):
            while True:
                print('''
●-----------------------------------------------● 
|                                               |
|  ==========================================   |
|                 Food Items                    |           
|  ==========================================   |               
|  Options:                                     |
|             [1] View All Food Items           |
|             [2] Add a Food Item               |
|             [3] Update a Food Item            |
|             [4] Delete a Food Item            |
|             [5] Go Back                       |     
|                                               |
●-----------------------------------------------●
              ''')
            
                item_choice = int(input("\nEnter number corresponding to your choice: "))

                if(item_choice == 1):
                    view_foods()
                elif(item_choice == 2):
                    add_food(current_user)
                elif(item_choice == 3):
                    update_food(current_user)
                elif(item_choice == 4):
                    delete_food(current_user)
                elif(item_choice == 5):
                    break;
                else:
                    print("Input invalid. Please enter a valid number.")

        ### Generate reports
        elif(choice == 4):
            reports()
            
        #### Print the user's profile  
        elif(choice == 5):
            profile()

        #### Exiting
        elif(choice == 6):
            print("Goodbye! See you next time.")
            break


        else:
            print("Input invalid. Please enter a valid number.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        db.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        db.rollback()