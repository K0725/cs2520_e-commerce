from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'cs2520'  # Replace this with your own secret key

@app.route('/login', methods=['POST'])
def login():
    # Get the form data from the request object
    username = request.form['username']
    password = request.form['password']

    # Hash the password using the same method used during user creation
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Connect to the SQLite database and create a cursor object
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Query the users table in the database to find a user with the submitted username
    cursor.execute('SELECT userId, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    conn.close()

    # If a user with the submitted username was found in the database
    if user is not None:
        # Check if the submitted password matches the password in the database
        if hashed_password == user[1]:  # user[1] contains the hashed password value
            # If the credentials are valid, store the user_id in the session and redirect to the home page
            session['user_id'] = user[0]  # user[0] contains the user_id
            return redirect(url_for('home'))
        else:
            # If the password is incorrect, re-render the login page with an error message
            return render_template('login.html', message='Incorrect password. Please try again.')
    else:
        # If the user is not found, re-render the login page with an error message
        return render_template('login.html', message='User not found. Please try again.')

##login page
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

        # Hash the password using the SHA-256 algorithm
        # This will make it much more difficult to crack
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Insert the user data into the "users" table
        try:
            cursor.execute('''INSERT INTO users (username, password)
                            VALUES (?, ?)''',
                            (username, password))

            # Commit the changes to the database and close the connection
            conn.commit()
            conn.close()

            # Set the message variable
            message = 'User created successfully!'

            # Return the template with the message variable
            return redirect(url_for('login_form', message=message))

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

            # If there's an error, rollback any changes
            conn.rollback()
            conn.close()

            # Set the error message
            error_message = 'There was an error creating your account. Please try again.'

            # Redirect to the login page with the error message
            return redirect(url_for('login_form', error_message=error_message))

    # If the request method is GET, just render the template without setting the message variable
    return render_template('create_user.html')


@app.route('/home')
def home():
    # Connect to the SQLite database and create a cursor object
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query the products table in the database to fetch recommended products
    cursor.execute('SELECT * FROM products ORDER BY productId DESC LIMIT 5')
    recommended_products = cursor.fetchall()

    conn.close()

    # Pass the recommended products to the template
    return render_template('home.html', recommended_products=recommended_products)



@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    # Fetch product details based on product_id
    # Render a template with the product details
    pass

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


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addProduct', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        image = request.files['image']
        stock = request.form.get('stock')
        category = request.form.get('category')

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':  # Ensure filename exists
                if not allowed_file(image.filename):  # Ensure file type is allowed
                    return 'File type not allowed! Please upload a valid image file.', 400
                filename = secure_filename(image.filename)  # Make sure the filename is secure
                # Define path if not already defined
                if not os.path.exists('static/images'):
                    os.makedirs('static/images')
                image.save(os.path.join('static/images', filename))  # Save the image in the static/images directory
            else:
                return 'No selected file'
        else:
            return 'No file part'


        # Connect to the SQLite database and create a cursor object
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Insert the user data into the "users" table
        try:
            cursor.execute('''INSERT INTO products (name, price, image, stock, category)
                            VALUES (?, ?, ?, ?, ?)''',
                            (name, price, filename, stock, category))  # Save the filename in the database
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()

        return redirect(url_for('search'))

    return render_template('add.html')

@app.route('/deleteProduct/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    # Connect to the SQLite database and create a cursor object
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Delete the product from the "products" table
    try:
        cursor.execute('''DELETE FROM products WHERE productId = ?''', (product_id,))

    except sqlite3.Error as error:
        print("Failed to delete product from sqlite table", error)
        return 'Failed to delete product', 400

    # Commit the changes to the database and close the connection
    conn.commit()
    conn.close()

    # Redirect the user back to the homepage after the product is deleted
    return redirect(url_for('home'))

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    user_id = request.form['userId']  # You need to provide a method to get the logged in user's ID
    conn = None
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO cart (userId, productId) VALUES (?, ?)''', (user_id, product_id))
        conn.commit()
    except NameError as e:
        print(e)
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'message': 'Failed to add item to cart'})
    finally:
        if conn:
            conn.close()
    return jsonify({'success': True, 'message': 'Item added to cart'})



@app.route('/cart', methods=['GET'])
def view_cart():
    user_id = request.args.get('userId')  
    print(f"Fetching cart items for user {user_id}")

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM cart INNER JOIN products ON cart.productId = products.productId WHERE userId = ?', (user_id,))
    print(f"SQL statement: SELECT * FROM cart INNER JOIN products ON cart.productId = products.productId WHERE userId = {user_id}")
    cart_items = cursor.fetchall()

    conn.close()

    
    print(f"userId: {user_id}")
    return render_template('cart.html', cart_items=cart_items, user_id=user_id, checkout_url=url_for('checkout', userId=user_id))


@app.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    user_id = request.form['userId']  # You need to provide a method to get the logged in user's ID

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM cart WHERE userId = ? AND productId = ?', (user_id, product_id))
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)

    conn.commit()
    conn.close()

    return redirect(url_for('view_cart', userId=user_id))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user_id = request.form['userId']  # You need to provide a method to get the logged in user's ID
        

        # Here, ideally you would handle order processing, like reducing item stock
        # and saving the order in an 'orders' table in your database.

        return redirect(url_for('confirmation'))

    user_id = request.args.get('userId')  # You need to provide a method to get the logged in user's ID
    print(f"This is user {user_id}")
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM cart INNER JOIN products ON cart.productId = products.productId WHERE userId = ?', (user_id,))
    cart_items = cursor.fetchall()

    total_price = round(sum(item['price'] for item in cart_items), 2)

    conn.close()

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price, user_id=user_id)


@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


if __name__ == '__main__':
    app.run(debug=True)

