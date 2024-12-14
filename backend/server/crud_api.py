import sqlite3
import datetime
import json
from contextlib import closing
import helper

DATABASE_PATH = "..\\database\\wine_tracker.db"

# Helper function for executing database queries
def execute_query(query, params=(), fetchone=False, commit=False):
    """
    Execute a SQL query with parameters and manage the database connection.

    :param query: SQL query to execute.
    :param params: Parameters for the query.
    :param fetchone: If True, return only one record.
    :param commit: If True, commit changes to the database.
    :return: Query results or None if no data is fetched.
    """
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if commit:
                conn.commit()
                return cursor.lastrowid  # Return the last inserted ID for INSERT queries.

            if fetchone:
                return cursor.fetchone()

            return cursor.fetchall()

    except sqlite3.Error as e:
        raise Exception(f"Database error: {e}")
    
# User login and authentication
def fetch_user_login_details_with_wines(email, password):
    """
    Validates user credentials and retrieves user details along with their wine list.

    :param email: User's email address.
    :param password: Plaintext password.
    :return: User details and structured wine list if credentials are valid.
    """
    query_user = "SELECT * FROM Users WHERE email = ?"
    try:
        # Fetch user details
        user = execute_query(query_user, (email,), fetchone=True)
        if not user:
            raise Exception("User not found")
        
        if not helper.check_user_password(password, user[3]):
            raise Exception("Incorrect password")
        
        # Fetch wine list using the refactored function
        wines_transformed = fetch_user_wine_list(user[0])
        
        
        return {
            "user": {
                "id": user[0],
                "username": user[1],
                "email": user[2],
            },
            "wines": wines_transformed
        }
    except Exception as e:
        raise Exception(f"Error fetching user details or wine list: {e}")

# User wine list retrieval
def fetch_user_wine_list(user_id):
    """
    Fetches the user's wine list by user ID and transforms it into a structured format.

    :param user_id: The ID of the user.
    :return: A structured map of wine data.
    """
    query = """
    SELECT 
        Wines.wine_name, 
        Wines.img_url, 
        Wines.counter, 
        Wines.details,
        Sites.site_name, 
        CurrentPrice.site_url, 
        CurrentPrice.regular_price, 
        CurrentPrice.club_price, 
        CurrentPrice.sale_price
    FROM 
        CurrentPrice
    JOIN 
        UserWineList ON UserWineList.wine_id = CurrentPrice.wine_id
    JOIN 
        Wines ON Wines.id = CurrentPrice.wine_id
    JOIN 
        Sites ON Sites.id = CurrentPrice.site_id
    WHERE 
        UserWineList.user_id = ?
    """
    try:
        wine_list = execute_query(query, (user_id,))
        return helper.transform_wine_list(wine_list)
    except Exception as e:
        raise Exception(f"Error fetching wine list: {e}")

def add_user(name, email, password):
    """
    Adds a new user to the Users table.

    :param name: The name of the user.
    :param email: The email of the user (must be unique).
    :param password: The plaintext password of the user.
    :return: Success message or error message.
    """
    hashed_password = helper.hash_user_password(password)  # Hash the password before storing
    query = """
    INSERT INTO Users (name, email, password)
    VALUES (?, ?, ?);
    """
    try:
        last_inserted_id = execute_query(query, (name, email, hashed_password), commit=True)
        return f"User '{name}' added successfully with ID {last_inserted_id}!"
    except sqlite3.IntegrityError:
        return f"Error: A user with email '{email}' already exists."
    except Exception as e:
        return f"Database error: {e}"

def add_wine_to_user_list(user_id, wine_id, desire_price):
    """Add a wine to the user's list."""
    query = """
    INSERT OR IGNORE INTO UserWineList (user_id, wine_id, desire_price)
    VALUES (?, ?, ?);
    """
    execute_query(query, (user_id, wine_id, desire_price), commit=True)

def remove_wine_from_user_list(user_id, wine_id):
    """Remove a wine from the user's list."""
    query = """
    DELETE FROM UserWineList
    WHERE user_id = ? AND wine_id = ?;
    """
    execute_query(query, (user_id, wine_id), commit=True)

def add_wine_data(name, regular_price, club_price, sale_price, img_url, site_url, site_id):
    """Add wine data to the database."""
    wine_query = """
    INSERT OR IGNORE INTO Wines (wine_name, img_url, details)
    VALUES (?, ?, ?);
    """
    wine_id = execute_query(wine_query, (name, img_url, ""), commit=True)

    price_query = """
    INSERT INTO CurrentPrice (wine_id, site_id, date, regular_price, club_price, sale_price, site_url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT (wine_id, site_id) DO UPDATE SET
        regular_price = excluded.regular_price,
        club_price = excluded.club_price,
        sale_price = excluded.sale_price;
    """
    date_today = datetime.today().strftime('%Y-%m-%d')
    execute_query(price_query, (wine_id, site_id, date_today, regular_price, club_price, sale_price, site_url), commit=True)

    history_query = """
    INSERT INTO HistoryPrice (wine_id, site_id, date, regular_price, club_price, sale_price)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    execute_query(history_query, (wine_id, site_id, date_today, regular_price, club_price, sale_price), commit=True)

def update_product_prices(wine_id, site_id, regular_price, club_price, sale_price):
    """Update product prices in CurrentPrice and add to HistoryPrice."""
    date_today = datetime.today().strftime('%Y-%m-%d')

    price_query = """
    UPDATE CurrentPrice
    SET regular_price = ?, club_price = ?, sale_price = ?, date = ?
    WHERE wine_id = ? AND site_id = ?;
    """
    execute_query(price_query, (regular_price, club_price, sale_price, date_today, wine_id, site_id), commit=True)

    history_query = """
    INSERT INTO HistoryPrice (wine_id, site_id, date, regular_price, club_price, sale_price)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    execute_query(history_query, (wine_id, site_id, date_today, regular_price, club_price, sale_price), commit=True)

def get_all_wines():
    """Retrieve all wines from the database."""
    query = """
    SELECT Wines.id, Wines.wine_name, Wines.img_url, Wines.details,
           CurrentPrice.regular_price, CurrentPrice.club_price, CurrentPrice.sale_price,
           Sites.site_name, CurrentPrice.site_url
    FROM Wines
    LEFT JOIN CurrentPrice ON Wines.id = CurrentPrice.wine_id
    LEFT JOIN Sites ON CurrentPrice.site_id = Sites.id;
    """
    return execute_query(query)

if __name__ == "__main__":
    try:
        result = add_user("fffsss" , "fsafssss13eran@gmail.com", "12fsafsa3456")
        print(result)
    except Exception as e:
        print(e)