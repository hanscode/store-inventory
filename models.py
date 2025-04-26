from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Create a model called Product that the SQLAlchemy ORM will use to build the database. The Product model should have five attributes: product_id, product_name, product_quantity, product_price, and date_updated. Use SQLALchemy’s built-in primary_key functionality for the product_id field, so that each product will have an automatically generated unique identifier.

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_quantity = Column(Integer)
    product_price = Column(Integer)
    date_updated = Column(Date)

    def __repr__(self): # 
        return f'Product ID: {self.product_id}, Name: {self.product_name}, Quantity: {self.product_quantity}, Price: {self.product_price}, Date Updated: {self.date_updated}'