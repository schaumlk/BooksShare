from flask import Flask, render_template, json, redirect
import os
from flask_mysqldb import MySQL
import MySQLdb
from flask import request
from dotenv import load_dotenv, find_dotenv
from datetime import datetime


# Configuration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_schaumlk'
app.config['MYSQL_PASSWORD'] = '2860' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_schaumlk'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

host = 'classmysql.engr.oregonstate.edu'
user = 'cs340_schaumlk'
password = '2860' #last 4 of onid
db = 'cs340_schaumlk'
cursorClass = "DictCursor"

mysql = MySQL(app)
#######

# Routes 

@app.route("/")
def landingPage():
    return render_template("base.html")

@app.route("/User", methods=["POST", "GET"])
def users():
    # insert (add)
    if request.method == 'POST':
        if request.form.get("Add_User"):
            user_id = request.form['user_id']
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = 'INSERT INTO Users (user_id, username, password, first_name, last_name, email, created_at, modified_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
       
            cur = mysql.connection.cursor()
            cur.execute(query, (user_id, username, password, first_name, last_name, email, created_at, modified_at))
            mysql.connection.commit()

            return redirect("User")

    # display
    query = "SELECT user_id, username, password, first_name, last_name, email, created_at, modified_at from Users"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return render_template("Users.html",data=data)

# update
@app.route("/edit_users/<int:id>", methods=["POST", "GET"])
def update_users(id):
    
    if request.method == "GET":

        query = "SELECT user_id, username, password, first_name, last_name, email, created_at, modified_at from Users where user_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_users.html", data=data, userID = id)

    # commit changes
    if request.method == "POST":
        if request.form.get("Edit_User"):
            user_id = request.form['user_id']
            username = request.form['username']
            password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = "UPDATE Users SET user_id = %s, username = %s, password = %s, first_name = %s, last_name = %s, email = %s, created_at = %s, modified_at = %s WHERE Users.user_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (user_id, username, password, first_name, last_name, email, created_at, modified_at, user_id))
            mysql.connection.commit()

            return redirect("/User")

# delete
@app.route("/delete_users/<int:id>", methods=["POST", "GET"])
def delete_user(id):

    if request.method == "GET":

        query = "SELECT user_id, username, password, first_name, last_name, email, created_at, modified_at from Users WHERE user_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("delete_users.html", data=data, userID=id)

    if request.method == "POST":

        
        user_id = request.form["user_id"]
        #return f"{request.form}"
        query = f"DELETE FROM Users WHERE Users.user_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id,))
        mysql.connection.commit()

        return redirect("/User")

@app.route("/Author", methods=["GET"])
def authors():
    # display
    query = "SELECT author_id, author_fname, author_lname, book_id from Authors"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return render_template("Authors.html", data=data)

@app.route("/Author", methods=["POST"])
def postAuthors():
    # insert (add)
    try:
    
        author_id = request.form['author_id']
        author_fname = request.form['author_fname']
        author_lname = request.form['author_lname']
        book_id = request.form['book_id']

        query = 'INSERT INTO Authors (author_id, author_fname, author_lname, book_id) VALUES (%s, %s, %s, %s)'

        cur = mysql.connection.cursor()
        cur.execute(query, (author_id, author_fname, author_lname, book_id))
        mysql.connection.commit()
    except Exception as E:
        return E
    return redirect("Author")

# update
@app.route("/edit_authors/<int:id>", methods=["POST", "GET"])
def update_authors(id):
    
    if request.method == "GET":

        query = "SELECT author_id, author_fname, author_lname, book_id from Authors where author_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_authors.html", data=data, AuthorID = id)

    # commit changes
    if request.method == "POST":
        if request.form.get("Edit_Author"):
            author_id = request.form['author_id']
            author_fname = request.form['author_fname']
            author_lname = request.form['author_lname']
            book_id = request.form['book_id']

            query = "UPDATE Users SET author_id = %s, author_fname = %s, author_lname = %s, book_id = %s WHERE Authors.author_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (author_id, author_fname, author_lname, book_id, author_id))
            mysql.connection.commit()

            return redirect("/Author")

@app.route("/delete_authors/<int:id>", methods=["POST", "GET"])
def delete_author(id):

    if request.method == "GET":

        query = "SELECT author_id, author_fname, author_lname, book_id from Authors where author_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("delete_authors.html", data=data, authorID=id)

    if request.method == "POST":
        
        author_id = request.form["author_id"]
        #return f"{request.form}"
        query = f"DELETE FROM Authors WHERE Authors.author_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (author_id,))
        mysql.connection.commit()

        return redirect("/Author")

    
@app.route("/Transaction")
def transactions():
    return render_template("Transactions.html") #Transactions = Transaction.query.all())

@app.route("/Book")
def books():
    return render_template("Books.html") # Books = Book.query.all())

@app.route("/Inventory")
def inventory():
    return render_template("Inventory.html") # Inventory = Inventory.query.all())

@app.route("/Books_Has_Authors")
def book_has_author():
    return render_template("Books_Has_Authors.html") #Books_Has_Authors = Books_has_Authors.query.all())

def executeQuery(query = None, queryParams = ()):
    db_connection = MySQLdb.connect(host,user,password,db)
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, queryParams)
    db_connection.commit()
    return cursor


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 52285)) #58285
    #                                 ^^^^
    #              You can replace this number with any valid port
    app.run(port=port, debug = True)
    #app.run(host = "flip1.engr.oregonstate.edu", port= port, debug = True) 




