import bcrypt  # for password hashing
from collections import defaultdict


# Password hashing and verification
def hash_user_password(password):
    """
    Hashes a plaintext password using bcrypt.

    :param password: Plaintext password.
    :return: Hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_user_password(plain_password, hashed_password):
    """
    Verifies a plaintext password against a hashed password.

    :param plain_password: The plaintext password.
    :param hashed_password: The hashed password to verify against.
    :return: True if passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)


def transform_wine_list(wine_list):
    """
    Transforms the wine list into the desired structure.

    :param wine_list: Raw SQL query results.
    :return: Structured map of wine data.
    """
    wine_map = defaultdict(lambda: {
        "img_url": "",
        "counter": 0,
        "details": "",
        "sites": {}
    })
    for wine_name, img_url, counter, details, site_name, site_url, regular_price, club_price, sale_price in wine_list:
        wine_entry = wine_map[wine_name]
        wine_entry["img_url"] = img_url
        wine_entry["counter"] = counter
        wine_entry["details"] = details
        wine_entry["sites"][site_name] = {
            "site_url": site_url,
            "prices": [regular_price, club_price, sale_price]
        }
    return dict(wine_map)