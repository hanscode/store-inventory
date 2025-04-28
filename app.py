"""
Store Inventory Application
----------------------------

This is the main entry point of the Store Inventory application.

The app allows users to:
- View product details by selecting a product ID.
- Add new products to the inventory.
- Backup the current database into a CSV file.
- Exit the application gracefully.

Technologies Used:
- Python 3
- SQLAlchemy ORM
- SQLite Database

Usage:
- Run the app inside a virtual environment.
- Follow the interactive menu prompts to manage the store inventory.

Author: Hans Steffens
"""

from models import Base, engine, session, Product

import datetime
import csv
import time


def menu():
    """
    Displays the menu options to the user and returns the user's choice.
    """
    while True:
        print(
            """
            \n======== MENU ========
            \rPlease choose one of the options below:
            \rv - View product details
            \ra - Add a new product
            \rb - Backup products database
            \rq - Quit
            \r========================
            """
        )

        choice = input("What would you like to do? ").lower()
        if choice in ['v', 'a', 'b', 'q']:
            return choice
        else:
            print(f"""
                  \n====== INPUT ERROR ======
                  \rThe option '{choice}' is not valid.
                  \rPlease choose v, a, b, or q.
                  \r==========================""")
            time.sleep(1.5)


def clean_product_name():
    """
    Prompts the user for a product name and returns it.

    Returns:
        str: The cleaned product name.
    """
    try:
        product_name = input("Product name: ").strip()
        if not product_name:
            raise ValueError("Product name cannot be empty.")
    except ValueError as e:
        print(f"""
              \n====== NAME ERROR ======
              \r{e}
              \r==========================""")
        time.sleep(1.5)
        return clean_product_name()
    return product_name


def clean_price(price_str):
    """
    Cleans the price string by removing the dollar sign and converts it
    to an integer in cents.

    Args:
        price_str (str): Price as a string, e.g., "$9.99" or "9.99".

    Returns:
        int: Price in cents as an integer.
    """
    try:
        price_float = float(price_str.replace('$', '').strip())
    except ValueError:
        input("""
              \n====== PRICE ERROR ======
              \rThe price should be in the format of 10.99 or $10.99.
              \rPress Enter to try again.
              \r==========================""")
        return None
    else:
        return int(price_float * 100)


def clean_date(date_str):
    """
    Cleans the date string and converts it to a datetime.date object.

    Args:
        date_str (str): Date as a string, e.g., "01/01/2023".

    Returns:
        datetime.date: Date as a datetime.date object.
    """
    return datetime.datetime.strptime(date_str, '%m/%d/%Y').date()


def clean_id(id_str, options):
    """
    Validates and converts a string input into a valid product ID.

    Args:
        id_str (str): The input ID as a string.
        options (list): A list of valid product IDs.

    Returns:
        int or None: The valid product ID as an integer if valid,
        otherwise None.
    """
    try:
        product_id = int(id_str)
    except ValueError:
        input("""
              \n====== ID ERROR ======
              \rThe id should be a number.
              \rPress Enter to try again.
              \r==========================""")
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f"""
                  \n====== ID ERROR ======
                  \rThe product id {product_id} is not in the database.
                  \rPlease choose one of the following ids: {options}
                  \rPress Enter to try again.
                  \r==========================""")
            return


def convert_date(date_obj):
    """
    Converts a datetime.date object into a formatted string.

    Args:
        date_obj (datetime.date): The date object to format.

    Returns:
        str: The formatted date as 'M/D/YYYY'.
    """
    return date_obj.strftime('%-m/%-d/%Y')


def read_csv():
    """
    Reads the inventory CSV file and processes each product entry.

    Returns:
        list: A list of product dictionaries with cleaned and formatted values.
    """
    with open('inventory.csv', newline='') as csvfile:
        data = csv.DictReader(csvfile, delimiter=',')
        products = []
        for row in data:
            product = {
                'product_name': row['product_name'],
                'product_quantity': int(row['product_quantity']),
                'product_price': clean_price(row['product_price']),
                'date_updated': clean_date(row['date_updated'])
            }
            products.append(product)
        return products


def add_csv_to_db():
    """
    Adds or updates products from the CSV file into the database.

    If a product already exists, updates it only if the CSV data is more
    recent.
    Otherwise, inserts new products.
    """
    data = read_csv()
    for row in data:
        product_in_db = session.query(Product).filter_by(
            product_name=row['product_name']
        ).one_or_none()
        if product_in_db:
            if row['date_updated'] > product_in_db.date_updated:
                product_in_db.product_quantity = row['product_quantity']
                product_in_db.product_price = row['product_price']
                product_in_db.date_updated = row['date_updated']
                session.commit()
        else:
            new_product = Product(
                product_name=row['product_name'],
                product_quantity=row['product_quantity'],
                product_price=row['product_price'],
                date_updated=row['date_updated']
            )
            session.add(new_product)
    session.commit()


def display_product_by_id():
    """
    Prompts the user to enter a product ID and displays the corresponding
    product details.

    Displays product name, price, quantity, and last update date.
    """
    id_options = []
    for product in session.query(Product):
        id_options.append(product.product_id)
    id_error = True
    while id_error:
        id_choice = input(f"""
            \nId Options: {id_options}
            \rProduct id: """)
        id_choice = clean_id(id_choice, id_options)
        if type(id_choice) == int:
            id_error = False
            the_product = session.query(Product).filter(
                Product.product_id == id_choice
            ).first()
            print(f"""
                  \n====== PRODUCT DETAILS ======
                  \rProduct ID: {the_product.product_id}
                  \rName: {the_product.product_name}
                  \rPrice: ${the_product.product_price / 100}
                  \rQuantity: {the_product.product_quantity}
                  \rDate Updated: {convert_date(the_product.date_updated)}
                  \r==========================""")
            time.sleep(2)


def add_product_to_db():
    """
    Adds a new product to the database.

    Prompts the user for product name, price, and quantity.
    The current date is used for 'date_updated'.
    """
    name = clean_product_name()
    product_in_db = session.query(Product).filter_by(
        product_name=name
    ).one_or_none()
    if product_in_db:
        print(
            f"The product '{name}' already exists. It was last updated on "
            f"{convert_date(product_in_db.date_updated)}."
        )
        update_prompt = "Do you want to update the product details? (y/n): "
        update_choice = input(update_prompt).lower()
        if update_choice == 'y':
            price_error = True
            while price_error:
                price = input("Product price (e.g. 10.99 or $10.99): ")
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            quantity = input("Product quantity: ")
            date_updated = datetime.datetime.now().date()
            product_in_db.product_price = price
            product_in_db.product_quantity = quantity
            product_in_db.date_updated = date_updated
            session.commit()
            print(f"Product {name} updated successfully!")
            time.sleep(2)
        else:
            print("No changes made.")
            time.sleep(2)
            return
    else:
        price_error = True
        while price_error:
            price = input("Product price (e.g. 10.99 or $10.99): ")
            price = clean_price(price)
            if type(price) == int:
                price_error = False
        quantity = input("Product quantity: ")
        date_updated = datetime.datetime.now().date()

        new_product = Product(
            product_name=name,
            product_price=price,
            product_quantity=quantity,
            date_updated=date_updated
        )

        session.add(new_product)
        session.commit()
        print(f"Product {name} added successfully!")
        time.sleep(2)


def backup_db():
    """
    Creates a backup of the database by exporting all products to a CSV file.

    The backup file is named 'backup.csv' and will overwrite any existing
    backup.
    """
    with open('backup.csv', 'w', newline='') as csvfile:
        fieldnames = [
            'product_name',
            'product_price',
            'product_quantity',
            'date_updated'
        ]
        product_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        product_writer.writeheader()
        for product in session.query(Product):
            product_writer.writerow({
                'product_name': product.product_name,
                'product_price': f"${product.product_price / 100:.2f}",
                'product_quantity': product.product_quantity,
                'date_updated': convert_date(product.date_updated)
            })
    print("Backup completed successfully!")
    time.sleep(2)


def app():
    """
    Main app loop.

    Presents a menu to the user, processes the selected option, and performs
    actions like viewing a product, adding a product, backing up the database,
    or exiting the app.
    """
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            # View product details
            display_product_by_id()
        elif choice == 'a':
            # Add a new product
            add_product_to_db()
        elif choice == 'b':
            # Backup products database
            backup_db()
        else:
            # Quit the app
            print("GOODBYE!")
            app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv_to_db()
    app()

    # The following code is for testing purposes only
    # Uncomment to see all products in the database
    # for product in session.query(Product):
    #     print(
    #         f'{product.product_id} | {product.product_name} | '
    #         f'{product.product_quantity} | {product.product_price} | '
    #         f'{product.date_updated}'
    #     )
