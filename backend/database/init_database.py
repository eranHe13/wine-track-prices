import sqlite3

# Connect to SQLite database (or create one if it doesn't exist)
conn = sqlite3.connect('./wine_tracker.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Wines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wine_name TEXT NOT NULL,
    img_url TEXT,
    counter INTEGER DEFAULT 0,
    details TEXT, -- New column for wine details
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS CurrentPrice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wine_id INTEGER NOT NULL,
    site_id INTEGER NOT NULL,
    date DATE NOT NULL,
    regular_price REAL NOT NULL,
    club_price REAL,
    sale_price REAL,
    site_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wine_id) REFERENCES Wines(id),
    FOREIGN KEY (site_id) REFERENCES Sites(id),
    UNIQUE (wine_id, site_id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS HistoryPrice (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wine_id INTEGER NOT NULL,
    site_id INTEGER NOT NULL,
    date DATE NOT NULL,
    regular_price REAL NOT NULL,
    club_price REAL,
    sale_price REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wine_id) REFERENCES Wines(id),
    FOREIGN KEY (site_id) REFERENCES Sites(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS UserWineList (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    wine_id INTEGER NOT NULL,
    desire_price INTEGER NOT NULL , 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (wine_id) REFERENCES Wines(id),
    UNIQUE (user_id, wine_id)
);
''')

# Commit and close
conn.commit()
conn.close()
