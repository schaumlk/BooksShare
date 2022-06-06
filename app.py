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
    
    query2 = "SELECT book_id FROM `Books` ORDER BY book_id ASC;"
    cur = mysql.connection.cursor()
    cur.execute(query2)
    all_books_id = cur.fetchall()
    
    return render_template("Authors.html", data=data, Books_id=all_books_id)

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

        return render_template("edit_authors.html", data=data, authorID = id)

    # commit changes
    if request.method == "POST":
        if request.form.get("Edit_Author"):
            author_id = request.form['author_id']
            author_fname = request.form['author_fname']
            author_lname = request.form['author_lname']
            book_id = request.form['book_id']

            query = "UPDATE Authors SET author_id = %s, author_fname = %s, author_lname = %s, book_id = %s WHERE Authors.author_id = %s"
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

    
@app.route("/Transaction", methods=["POST", "GET"])
def transactions():
    # insert (add)
    if request.method == 'POST':
        if request.form.get("Add_Transaction"):
            transaction_id = request.form['transaction_id']
            user_id = request.form['user_id']            
            inventory_id = request.form['inventory_id']
            total_price = request.form['total_price']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = 'INSERT INTO Transactions (transaction_id, user_id, inventory_id, total_price, created_at, modified_at) VALUES (%s, %s, %s, %s, %s, %s)'
       
            cur = mysql.connection.cursor()
            cur.execute(query, (transaction_id, user_id, inventory_id, total_price, created_at, modified_at))
            mysql.connection.commit()

            return redirect("Transaction")

    # display
    query = "SELECT transaction_id, user_id, inventory_id, total_price, created_at, modified_at from Transactions"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return render_template("Transactions.html",data=data)

# update
@app.route("/edit_transactions/<int:id>", methods=["POST", "GET"])
def update_transactions(id):
    
    if request.method == "GET":
        query = "SELECT transaction_id, user_id, inventory_id, total_price, created_at, modified_at from Transactions where transaction_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_transactions.html", data=data, transactionID = id)

    # commit changes
    if request.method == "POST":
        if request.form.get("Edit_Transaction"):
            transaction_id = request.form['transaction_id']
            user_id = request.form['user_id']            
            inventory_id = request.form['inventory_id']
            total_price = request.form['total_price']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = "UPDATE Transactions SET transaction_id = %s, user_id = %s, inventory_id = %s, total_price = %s, created_at = %s, modified_at = %s WHERE Transactions.transaction_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (transaction_id, user_id, inventory_id, total_price, created_at, modified_at, transaction_id))
            mysql.connection.commit()

            return redirect("/Transaction")

@app.route("/delete_transactions/<int:id>", methods=["POST", "GET"])
def delete_transaction(id):

    if request.method == "GET":
        query = "SELECT transaction_id, user_id, inventory_id, total_price, created_at, modified_at from Transactions where transaction_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("delete_transactions.html", data=data, transactionID=id)

    if request.method == "POST":
        
        transaction_id = request.form["transaction_id"]
        #return f"{request.form}"
        query = f"DELETE FROM Transactions WHERE Transactions.transaction_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (transaction_id,))
        mysql.connection.commit()

        return redirect("/Transaction")


@app.route("/Book", methods=["POST", "GET"])
def books():
    # insert (add)
    if request.method == 'POST':
        if request.form.get("Add_Book"):
            book_id = request.form['book_id']
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = 'INSERT INTO Books (book_id, title, description, price, created_at, modified_at) VALUES (%s, %s, %s, %s, %s, %s)'
       
            cur = mysql.connection.cursor()
            cur.execute(query, (book_id, title, description, price, created_at, modified_at))
            mysql.connection.commit()

            return redirect("Book")

    # display
    query = "SELECT book_id, title, description, price, created_at, modified_at from Books"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return render_template("Books.html", data=data)

# update
@app.route("/edit_books/<int:id>", methods=["POST", "GET"])
def update_books(id):
    
    if request.method == "GET":

        query = "SELECT book_id, title, description, price, created_at, modified_at from Books where book_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_books.html", data=data, bookID = id)

    # commit changes
    if request.method == "POST":
        if request.form.get("Edit_Book"):
            book_id = request.form['book_id']
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = "UPDATE Books SET book_id = %s, title = %s, description = %s, price = %s, created_at = %s, modified_at = %s WHERE Books.book_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (book_id, title, description, price, created_at, modified_at, book_id))
            mysql.connection.commit()

            return redirect("/Book")

@app.route("/delete_books/<int:id>", methods=["POST", "GET"])
def delete_book(id):

    if request.method == "GET":

        query = "SELECT book_id, title, description, price from Books where book_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("delete_books.html", data=data, bookID=id)

    if request.method == "POST":
        
        book_id = request.form["book_id"]
        #return f"{request.form}"
        query = f"DELETE FROM Books WHERE Books.book_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (book_id,))
        mysql.connection.commit()

        return redirect("/Book")


@app.route("/Inventory", methods=["POST", "GET"])
def inventory():
    # insert (add)
    if request.method == 'POST':
        if request.form.get("Add_Inventory"):
            inventory_id = request.form['inventory_id']
            quantity = request.form['quantity']
            book_id = request.form['book_id']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = 'INSERT INTO Inventory (inventory_id, quantity, book_id, created_at, modified_at) VALUES ( %s, %s, %s, %s, %s)'
       
            cur = mysql.connection.cursor()
            cur.execute(query, (inventory_id, quantity, book_id, created_at, modified_at))
            mysql.connection.commit()

            return redirect("Inventory")

    # display
    query = "SELECT inventory_id, quantity, book_id, created_at, modified_at from Inventory"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return render_template("Inventory.html", data=data)

# update
@app.route("/edit_inventory/<int:id>", methods=["POST", "GET"])
def update_inventory(id):
    
    if request.method == "GET":

        query = "SELECT inventory_id, quantity, book_id, created_at, modified_at from Inventory where inventory_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_inventory.html", data=data, inventoryID = id)

    # commit changes
    if request.method == "POST":
        if request.form.get("Edit_Inventory"):
            inventory_id = request.form['inventory_id']
            quantity = request.form['quantity']
            book_id = request.form['book_id']
            created_at = datetime.now()
            modified_at = datetime.now()

            query = "UPDATE Inventory SET inventory_id = %s, quantity = %s, book_id = %s, created_at = %s, modified_at = %s WHERE Inventory.inventory_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (inventory_id, quantity, book_id, created_at, modified_at, inventory_id))
            mysql.connection.commit()

            return redirect("/Inventory")

# delete
@app.route("/delete_inventory/<int:id>", methods=["POST", "GET"])
def delete_inventory(id):

    if request.method == "GET":
        query = "SELECT inventory_id, quantity, book_id, created_at, modified_at from Inventory WHERE inventory_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("delete_inventory.html", data=data, inventoryID=id)

    if request.method == "POST":        
        inventory_id = request.form["inventory_id"]
        query = f"DELETE FROM Inventory WHERE Inventory.inventory_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (inventory_id,))
        mysql.connection.commit()

        return redirect("/Inventory")

@app.route("/Books_Has_Authors", methods=["POST", "GET"])
def book_has_author():
    # insert (add)
    if request.method == 'POST':
        if request.form.get("Add_Book_Has_Authors"):
            books_book_id = request.form['books_book_id']
            authors_author_id = request.form['authors_author_id']
            
            query = 'INSERT INTO Books_Has_Authors (books_book_id, authors_author_id) VALUES ( %s, %s)'
       
            cur = mysql.connection.cursor()
            cur.execute(query, (books_book_id, authors_author_id))
            mysql.connection.commit()

            return redirect("Books_Has_Authors")

    # display
    query = "SELECT books_book_id, authors_author_id from Books_Has_Authors"
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return render_template("Books_Has_Authors.html", data=data)

# update
@app.route("/edit_BookHasAuthors/<int:id>", methods=["POST", "GET"])
def update_books_has_authors(id):
    
    if request.method == "GET":

        query = "SELECT books_book_id, authors_author_id from Books_Has_Authors where books_book_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_books_has_authors.html", data=data, books_book_id = id)

    # commit changes
    if request.method == "POST":
        if request.form.get("edit_books_has_authors"):
            books_book_id = request.form['books_book_id']
            authors_author_id = request.form['authors_author_id']

            query = "UPDATE Books_Has_Authors SET books_book_id = %s, authors_author_id = %s WHERE Books_Has_Authors.books_book_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (books_book_id, authors_author_id))
            mysql.connection.commit()

            return redirect("/Books_Has_Authors")

# delete
@app.route("/delete_BookHasAuthors/<int:id>", methods=["POST", "GET"])
def delete_BookHasAuthors(id):

    if request.method == "GET":
        query = "SELECT books_book_id, authors_author_id from Books_Has_Authors WHERE books_book_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("delete_books_has_authors.html", data=data, books_book_id = id)

    if request.method == "POST":        
        books_book_id = request.form["books_book_id"]
        query = f"DELETE FROM Books_Has_Authors WHERE Books_Has_Authors.books_book_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (books_book_id,))
        mysql.connection.commit()

        return redirect("/Books_Has_Authors")

    

def executeQuery(query = None, queryParams = ()):
    db_connection = MySQLdb.connect(host,user,password,db)
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, queryParams)
    db_connection.commit()
    return cursor


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 58288)) #58285
    #                                 ^^^^
    #              You can replace this number with any valid port
    #app.run(port=5000, debug = True)
    app.run(host = "flip3.engr.oregonstate.edu", port= port, debug = True) 




