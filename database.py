import sqlite3

conn = sqlite3.connect('database.db')

#Create table
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
        username TEXT,
		password TEXT
		)''')


#Create Product table
conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL,
		image TEXT,
		stock INTEGER,
<<<<<<< HEAD
		categoryId INTEGER,
		FOREIGN KEY(categoryId) REFERENCES 
        categories(categoryId)
=======
		category TEXT
>>>>>>> d4e449e0612a12b1ef2ccb8aeacd06effe2bf879
		)''')



#Create Cart Table
conn.execute('''CREATE TABLE cart
		(userId INTEGER,
		productId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')

<<<<<<< HEAD

conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')



=======
>>>>>>> d4e449e0612a12b1ef2ccb8aeacd06effe2bf879
conn.close()
