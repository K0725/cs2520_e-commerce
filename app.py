from flask import Flask, render_template, request, redirect, url_for
import sqlite3, hashlib, os

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Get the form data from the request object
    username = request.form['username']
    password = request.form['password']

    # Print the value of username to check if it's being passed correctly
    print(f"Username: {username}")

    # Connect to the SQLite database and create a cursor object
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Query the users table in the database to find a user with the submitted username
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    # If a user with the submitted username was found in the database
    if user is not None:
        # Check if the submitted password matches the password in the database
        if password == user[0]:  # user[0] contains the password value
            # If the credentials are valid, redirect to the home page
            return redirect(url_for('search'))
        else:
            # If the password is incorrect, re-render the login page with an error message
            return render_template('login.html', message='Incorrect password. Please try again.')
    else:
        # If the user is not found, re-render the login page with an error message
        return render_template('login.html', message='User not found. Please try again.')


@app.route('/', methods=['GET'])
def login_form():
    # Render the login page
    return render_template('login.html')


#Create Post and Get between the database
@app.route('/create-user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        # Get the form data from the request object
        username = request.form['username']
        password = request.form['password']

        # Connect to the SQLite database and create a cursor object
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insert the user data into the "users" table
        try:
            cursor.execute('''INSERT INTO users (username, password)
                            VALUES (?, ?)''',
                            (username, password))
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()

        # Set the message variable
        message = 'User created successfully!'

        # Return the template with the message variable
        return redirect(url_for('login_form', message=message))

    # If the request method is GET, just render the template without setting the message variable
    return render_template('create_user.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        return redirect(url_for('search_results', query=query))
    return render_template('search.html')

@app.route('/search-results', methods=['GET'])
def search_results():
    category = request.args.get('category')
    print("Category:", category)

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to filter products based on search query and category
    query = "SELECT * FROM products WHERE category = ?"
    cursor.execute(query, (category,))
    products = cursor.fetchall()
    
    print("Products: ", products)

    conn.close()

    return render_template('search.html', products=products)

@app.route('/addProduct', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        image = request.form.get('image')
        stock = request.form.get('stock')
        category = request.form.get('category')

        # Connect to the SQLite database and create a cursor object
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insert the user data into the "users" table
        try:
            cursor.execute('''INSERT INTO products (name, price, image, stock, category)
                            VALUES (?, ?, ?, ?, ?)''',
                            (name, price, image, stock, category))
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)


        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()


        return redirect(url_for('search'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)

