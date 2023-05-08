from flask import Flask, render_template, request, redirect, url_for, sqlite3

app = Flask(__name__)


# when opening the site, users should see a search bar, login button, a shopping cart. Some other potential buttons and features could be recommended
# selections(random) and some potential filters (sports, clothes, toys)
# The user can 
@app.route('/')
def index():
    # render template is a function from flask that is used to render HTML templates
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')



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


if __name__ == '__main__':
    app.run(debug=True)

