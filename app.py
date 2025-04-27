from models import Base, engine, session, Product

import datetime
import csv

def menu():
    while True:
        print(
        """
            \nINVENTORY MANAGEMENT SYSTEM
            \rPlease choose one of the options below:
            \rv - View product details
            \ra - Add a new product
            \rb - Backup products database
            \rq - Quit
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

if __name__ == "__main__":
    Base.metadata.create_all(engine) # Create the database and tables
    products = read_csv() # Read the CSV file
    for product in products:
        print(product)
     