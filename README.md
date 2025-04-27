# Python Web Development Techdegree  
### Project 4 - Store Inventory with SQLAlchemy  
**Author** - Hans Steffens  

---

## Project Overview

This is a Python console application that allows you to easily manage a store's inventory.
It enables users to view product details, add new products, and backup the inventory to a CSV file.
The application reads initial data from a CSV, stores it in a SQLite database using SQLAlchemy ORM, and provides a user-friendly menu to interact with the data.

## Tools and Technologies Used

- Python 3.12
- SQLAlchemy 2.0 (ORM for database interaction)
- SQLite (local database)
- CSV module (for reading and writing CSV files)
- Datetime module (for handling dates and timestamps)

## Features

- **Load data** from an existing `inventory.csv` file into the database.
- **View product details** by selecting a product ID.
- **Add a new product** into the database.
- **Update existing products** if a duplicate name is found and has a more recent date.
- **Backup** the entire inventory into a `backup.csv` file.
- **Automatic** date handling and price conversion (stored as cents for accuracy).

## Getting Started
Follow these steps to set up and run the application locally.

### 1. Clone the Repository
```bash
git clone https://github.com/hanscode/store-inventory
cd store-inventory
```

### 2. Set Up a Virtual Environment
Create a virtual environment to isolate project dependencies:

```bash
python -m venv env
```

### 3. Activate the Virtual Environment
Create a virtual environment to isolate project dependencies:

- On Mac/Linux:
```bash
source ./env/bin/activate
```
- On Windows:
```bash
.\env\Scripts\activate
```
You should now see the environment activated, e.g., `(env)` in your terminal prompt.

### 4. Install Project Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```
### 5. Run the Application
Once inside the project folder and with your virtual environment active:

```sh
python app.py
```
You will see the application menu and can start interacting with the inventory!

## Project File Structure
```sh
.
store-inventory/
│
├── app.py               # Main application file
├── models.py            # SQLAlchemy models (Product class)
├── inventory.csv        # Source inventory data (initial load)
├── backup.csv           # File generated when creating a backup
├── inventory.db         # File generated when running the app
├── requirements.txt     # Project dependencies
└── README.md            # This file
```
## Notes
- When adding new products, if the product name already exists in the database, the app will only update the existing record if the new data has a more recent date_updated.
- All prices are stored internally as integer cents for better precision (e.g., $9.99 is stored as 999 cents).
- Date fields are stored as proper datetime.date objects in the database.

## License
This project is licensed under the [MIT LICENSE](LICENSE).