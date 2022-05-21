# # 
# from flask import Flask, render_template
# import os
# from flask_sqlalchemy import SQLAlchemy
# import database.db_connector as db


# # Configuration

# app = Flask(__name__)
# db_connection = db.connect_to_database()

# app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
# app.config['MYSQL_USER'] = 'cs340_schaumlk'
# app.config['MYSQL_PASSWORD'] = '2860'
# app.config['MYSQL_DB'] = 'cs340_schaumlk'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# class User(db.Model):
#     user_id = db.Column('user_id', db.Integer, primary_key = True)
#     username = db.Column(db.String(70))
#     password = db.Column(db.String(15))
#     first_name = db.Column(db.String(50))
#     last_name = db.Column(db.String(50))
#     email = db.Column(db.String(75))
#     created_at = db.Column(db.String(50))
#     modified_at = db.Column(db.String(50))

#     def __repr__(self):
#         return f"User: {self.username} name: {self.first_name} {self.last_name} email: {self.email} joined on: {str(self.created_at)}" 

# class Inventory(db.Model):
#     inventory_id = db.Column('inventory_id', db.Integer, primary_key = True)
#     quantity = db.Column(db.Integer)
#     created_at = db.Column(db.String(50))
#     modified_at = db.Column(db.String(50))

# class Transaction(db.Model):
#     transaction_id = db.Column('transaction_id', db.Integer, primary_key = True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
#     inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'))
#     total_price = db.Column(db.Numeric(10,2))
#     created_at = db.Column(db.String(50))
#     modified_at = db.Column(db.String(50))
    

# class Book(db.Model):
#     book_id = db.Column('book_id', db.Integer, primary_key = True)
#     title = db.Column(db.String(25))
#     description = db.Column(db.String(200))
#     price = db.Column(db.Numeric(10,2))
#     inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'))
#     created_at = db.Column(db.String(50))
#     modified_at = db.Column(db.String(50))
    

# class Author(db.Model):
#     author_id = db.Column('author_id', db.Integer, primary_key = True)
#     author_fname = db.Column(db.String(50))
#     author_lname = db.Column(db.String(50))
#     #book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))
 
# class Books_has_Authors(db.Model):
#     author_id = db.Column(db.Integer, db.ForeignKey('author.author_id'))
#     book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'))

###########
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
            cur.execute(query, (user_id, username, password, first_name, last_name, email, created_at, modified_at))
            mysql.connection.commit()

            return redirect("User")

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

        if request.form.get("Delete_User"):
            user_id = request.form["user_id"]
            
        query = "DELETE FROM Users WHERE Users.user_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (user_id,))
        mysql.connection.commit()

        return redirect("/User")

@app.route("/Author")
def authors():
    return render_template("Authors.html") #Authors = Author.query.all())

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
    port = int(os.environ.get('PORT', 58285)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(host = "flip2.engr.oregonstate.edu", port= port, debug = True) 

# app = Flask(__name__)


