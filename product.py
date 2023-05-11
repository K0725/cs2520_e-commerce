import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
"""
# Add users to the table
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
# Retrieve users from the table
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

# Print the retrieved users
for user in users:
    print(user)

# Close the connection
conn.close()
