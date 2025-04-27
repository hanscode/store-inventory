"""
Models for Store Inventory Application
--------------------------------------

This file defines the database structure for the Store Inventory app using SQLAlchemy ORM.

It includes:
- Database connection setup
- Session creation
- Product model definition with attributes:
    - product_id
    - product_name
    - product_quantity
    - product_price
    - date_updated

Author: Hans Steffens
"""

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Product(Base):
    """
    A SQLAlchemy ORM model representing a product in the store inventory.
    This model is used to interact with the 'products' table in the database.
    
    Attributes:
        product_id (int): Unique identifier for the product (Primary Key).
        product_name (str): Name of the product.
        product_quantity (int): Quantity of the product available in stock.
        product_price (int): Price of the product.
        date_updated (date): Date when the product information was last updated.
    """
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)

    def __repr__(self):
        """
        Returns a string representation of the Product object.
        This method is used for debugging and logging purposes.
        """
        return f'Product ID: {self.product_id}, Name: {self.product_name}, Quantity: {self.product_quantity}, Price: {self.product_price}, Date Updated: {self.date_updated}'