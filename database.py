import sqlite3

conn = sqlite3.connect('database.db')

#Create table for user 
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
        username TEXT,
		password TEXT
		)''')


conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')

#Create Product table
conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		image BLOB,
		stock INTEGER,
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES 
        categories(categoryId)
		)''')



#Create Cart Table
conn.execute('''CREATE TABLE cart
		(userId INTEGER,
		productId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')





conn.close()
