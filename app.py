from models import Base, engine, session, Product

import datetime
import csv
import time

def menu():
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
             input("""
              \rPlease choose one of the options above.
              \r v, a, b, or q
              \rPress Enter to try again.""")


def clean_price(price_str):
    if ',' in price_str:
        price_str = price_str.replace(',', '.')
    if '$' in price_str:
        price_str = price_str.replace('$', '')
    price = float(price_str)
    return int(price * 100)
    
def clean_date(date_str):
    return datetime.datetime.strptime(date_str, '%m/%d/%Y').date()

def clean_id(id_str, options):
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
    return date_obj.strftime('%-m/%-d/%Y')
    
def read_csv():
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
    data = read_csv()
    for row in data:
        product_in_db = session.query(Product).filter_by(product_name=row['product_name']).one_or_none()
        if product_in_db == None:
            new_product = Product(
                product_name=row['product_name'],
                product_quantity=row['product_quantity'],
                product_price=row['product_price'],
                date_updated=row['date_updated']
            )
            session.add(new_product)
    session.commit()

def display_product_by_id():
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
            the_product = session.query(Product).filter(Product.product_id == id_choice).first()
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
    name = input("Product name: ")
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

def app():
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
            pass
        else:
            # Quit the app
            print("GOODBYE!")
            app_running = False

if __name__ == "__main__":
    Base.metadata.create_all(engine) # Create the database and tables
    add_csv_to_db() # Add the products from the CSV file to the database
    app() # Start the app


    # for product in session.query(Product):
    #     print(f'{product.product_id} | {product.product_name} | {product.product_quantity} | {product.product_price}| {product.date_updated}')
