import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Add users to the table
"""
users_data = [
    (1, 'user1', 'password1'),
    (2, 'user2', 'password2'),
    (3, 'user3', 'password3')
]

cursor.executemany('''INSERT INTO users (userId, username, password)
                      VALUES (?, ?, ?)''', users_data)

# Commit the changes
conn.commit()
"""
"""
products_data = [
    (1, 'Product A', 10.99, 'image1.jpg', 50, "Entertainment"),
    (2, 'Product B', 5.99, 'image2.jpg', 20, "Food"),
    (3, 'Product C', 15.99, 'image3.jpg', 10, "Food"),
    (4, 'Product D', 8.99, 'image4.jpg', 30, "Clothes"),
    (5, 'Product E', 12.99, 'image5.jpg', 15, "Sports")
]
cursor.executemany('''INSERT INTO products (productId, name, price, image, stock, category) 
                      VALUES (?, ?, ?, ?, ?, ?)''', products_data)
"""
# Retrieve users from the table
cursor.execute('SELECT * FROM products')
products = cursor.fetchall()

# Print the retrieved users
for prod in products:
    print(prod)

conn.commit()

# Close the connection
conn.close()
