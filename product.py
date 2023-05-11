import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Insert a user into the "users" table
user_data = (1, 'password123', 'johndoe@example.com', 'John', 'Doe')
cursor.execute('''INSERT INTO users (userId, password, email, firstName, lastName)
                  VALUES (?, ?, ?, ?, ?)''', user_data)


# Insert a product into the "products" table
product_data = ('Shirt', 19.99, 'shirt.jpg', 100, 1)
cursor.execute('''INSERT INTO products (name, price, image, stock, categoryId)
                  VALUES (?, ?, ?, ?, ?)''', product_data)

# Commit the changes
conn.commit()

cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

# Retrieve all products
cursor.execute('SELECT * FROM products')
products = cursor.fetchall()

for user in users:
    print (user)

for product in products:
    print(product)


# Close the connection
conn.close()
