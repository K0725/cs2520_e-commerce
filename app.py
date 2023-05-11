from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn =  sqlite3.connect('database.db')

cursor = conn.cursor()


# when opening the site, users should see a search bar, login button, a shopping cart. Some other potential buttons and features could be recommended
# selections(random) and some potential filters (sports, clothes, toys)
# The user can 
@app.route('/')
def index():
    error_msg = request.args.get('error')
    error_flag = request.args.get('error_flag')
    # render template is a function from flask that is used to render HTML templates
    return render_template('login.html', error=error_msg, error_flag=error_flag)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # retrieve the submitted username and password from the form
        username = request.form['username']
        password = request.form['password']

        # connect to database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # SQL query to select the user with the username
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        result = cursor.fetchall()

        # close connection to database
        conn.close()

        if len(result) > 0:
            return render_template('search.html')
        
        else:
            error_msg = "Invalid username or password"
            return redirect(url_for('index', error=error_msg, error_flag=True))
        
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
        return render_template('search.html', message=message)

    # If the request method is GET, just render the template without setting the message variable
    return render_template('create_user.html')


@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        return redirect(url_for('search_results', query=query))
    return render_template('search.html')

@app.route('/search-results')
def search_results():
    query = request.args.get('query')
    # Perform search logic here
    results = []
    return render_template('search_results.html', query=query, results=results)

@app.route('/addProduct')
def add_product():
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)

