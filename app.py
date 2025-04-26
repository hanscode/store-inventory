from models import Base, engine, Session, Product


if __name__ == "__main__":
    Base.metadata.create_all(engine) # Create the database and tables