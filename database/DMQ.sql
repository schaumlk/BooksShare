--Ariel Rosenthal and Katie Schaumleffle
--Project Step 3
--Due 5/5/2022

--Add a new User

INSERT INTO Users (user_id, username, password, first_name, last_name, email, created_at, modified_at)
VALUES (:user_id_box, :username_box, :password_box, :first_name_box, :last_name_box, :email_box, :created_at_box, :modified_at_box)

--Display all Users

SELECT user_id, username, password, first_name, last_name, email, created_at, modified_at FROM Users

--Create menu information that will be used in transactions

SELECT user_id, first_name, last_name, email FROM Users

--Update a User

UPDATE Users
SET user_id = :user_id_box, username = :username_box, password = :password_box, first_name = :first_name_box, last_name = :last_name_box, email = :email_box, created_at = :created_at_box, modified_at = :modified_at_box
WHERE user_id = :user_id_selected

--Delete a User

DELETE FROM Users WHERE user_id = :user_id_selected

--Dynamic Search

SELECT user_id, username, password, first_name, last_name, email, created_at, modified_at FROM Users
WHERE [user_id = :user_id_box]
[AND] [username = :username_box]
[AND] [password = :password_box]
[AND] [first_name = :first_name_box]
[AND] [last_name = :last_name_box]
[AND] [email =:email_box]
[AND] [created_at = :created_at_box]
[AND] [modified_at = :modified_at_box]

-----------------------------------------------------------------------------------------------------------------------

-- Add a new Book

INSERT INTO Books (book_id, title, description, price, inventory_id, created_at, modified_at)
VALUES (:book_id_box, :title_box, :description_box, :price_box, :inventory_id_box, :created_at_book, :modified_at_book)

-- Display all Books

SELECT book_id, title, description, price, inventory_id, created_at, modified_at FROM Books

--Create dropdown information for Books

SELECT book_id, title, price FROM Books

-- Update a Book

UPDATE Books
SET book_id = :book_id_box, title = :title_box, description = :description_box, price = :price_box, inventory_id = :inventory_id_box, created_at = :created_at_book, modified_at = :modified_at_book
WHERE book_id = :book_id_selected

--Delete a Book

DELETE FROM Books WHERE book_id = :book_id_selected

-- Join Books and Inventory

SELECT Books.inventory_id FROM Books
INNER JOIN Inventory ON Books.inventory_id = Inventory.inventory_id

--Dynamic search for Books

SELECT book_id, title, description, price, inventory_id, created_at, modified_at FROM Books
WHERE [book_id = :book_id_box]
[AND] [title = :title_box]
[AND] [description = :description_box]
[AND] [price = :price_box]
[AND] [inventory_id = :inventory_id_box]
[AND] [created_at = :created_at_book]
[AND] [modified_at = :modified_at_book]

-------------------------------------------------------------------------------------------------------------

-- Add entry to Inventory

INSERT INTO Inventory (inventory_id, quantity, book_id, trasaction_id, created_at, modified_at)
VALUES (:inventory_id_in, :quantity_drop_in, :book_id_in, :transaction_id_in, :created_at_in, :modified_at_in)

--Display the Inventory

SELECT inventory_id, quantity, book_id, trasaction_id, created_at, modified_at FROM Inventory

-- Create Inventory drop down

SELECT inventory_id, quantity, book_id FROM Inventory

--Update Inventory

UPDATE Inventory
SET inventory_id = :inventory_id_in, quantity = :quantity_in, book_id = :book_id_in, transaction_id = :transaction_id_in, created_at = :created_at_in, modified_at = :modified_at_in
WHERE inventory_id = :inventory_id_selected

--Delete Inventory selection

DELETE FROM Inventory WHERE inventory_id = :inventory_id_selected

-- Join Inventory and Books

SELECT Inventory.book_id FROM Inventory
INNER JOIN Books ON Inventory.book_id = Books.book_id

-- Join Inventory and Transactions

SELECT Inventory.transaction_id FROM Inventory
INNER JOIN Transactions ON Inventory.transaction_id = Transactions.transaction_id

--Dynamic search for Inventory

SELECT inventory_id, quantity, book_id, trasaction_id, created_at, modified_at FROM Inventory
WHERE [inventory_id = :inventory_id_in]
[AND] [quantity = :quantity_in]
[AND] [book_id = :book_id_in]
[AND] [transaction_id = :transaction_id_in]
[AND] [created_at = :created_at_in]
[AND] [modified_at = :modified_at_in]

--------------------------------------------------------------------------------------------------------------------------------------------------

-- Add into Transactions

INSERT INTO Transactions (transaction_id, user_id, inventory_id, total_price, created_at, modified_at)
VALUES (:transaction_id_trans, :user_id_trans, :inventory_id_trans, :total_price_trans, :created_at_trans, :modified_at_trans)

-- Display all Transaction details

SELECT transaction_id, user_id, inventory_id, total_price, created_at, modified_at FROM Transactions

-- Create a dropdown for Transactions

SELECT transaction_id, user_id, inventory_id, total_price FROM Transactions

-- Update a Transaction

UPDATE Transactions
SET transaction_id, user_id, inventory_id, total_price, created_at, modified_at
WHERE transaction_id = transaction_id_selected

-- Delete a Transaction

DELETE FROM Transactions WHERE transaction_id = transaction_id_selected

-- Join Transactions and Users

SELECT Transactions.user_id FROM Transactions
INNER JOIN Users ON Transactions.user_id = Users.user_id

-- Join Transactions and Inventory

SELECT Transactions.inventory_id FROM Transactions
INNER JOIN Inventory ON Transactions.inventory_id = Inventory.inventory_id

-- Dynamic search for Transactions

SELECT transaction_id, user_id, inventory_id, total_price, created_at, modified_at FROM Transactions
WHERE [transaction_id = :transaction_id_trans]
[AND] [user_id = :user_id_trans]
[AND] [inventory_id = :inventory_id_trans]
[AND] [total_price = :total_price_trans]
[AND] [created_at = :created_at_trans]
[AND] [modified_at = :modified_at_trans]

---------------------------------------------------------------------------------------------------------------

-- Add an Author

INSERT INTO Authors (author_id, author_fname, author_lname, book_id)
VALUES (:author_id_auth, :author_fname_auth, :author_lname_auth, :book_id_auth)

-- Display all Author information

SELECT author_id, author_fname, author_lname, book_id FROM Authors

-- Update Author

UPDATE Authors
SET author_id = :author_id_auth, author_fname = :author_fname_auth, author_lname = :author_lname_auth, book_id = :book_id_auth
WHERE author_id = :author_id_selected

-- Delete an Author

DELETE FROM Authors WHERE author_id = :author_id_selected

-- Join Authors and Books

SELECT Authors.book_id FROM Authors
INNER JOIN Books ON Authors.book_id = Books.book_id

--Dynamic search for Authors table

SELECT author_id, author_fname, author_lname, book_id FROM Authors
WHERE [author_id = :author_id_auth]
[AND] [author_fname = :author_fname_auth]
[AND] [author_lname = :author_lname_auth]
[AND] [book_id = :book_id_auth]

------------------------------------------------------------------------------------------------------------------------------

--Add to Books_Has_Authors table

INSERT INTO Books_Has_Authors (books_book_id, authors_author_id)
VALUES (:books_book_id_bha, :authors_author_id_bha)

--Display all information from the Books_Has_Authors table

SELECT books_book_id, authors_author_id FROM Books_Has_Authors

--Update the Books_Has_Authors table

UPDATE Books_Has_Authors
SET books_book_id = :books_book_id_bha, authors_author_id = :authors_author_id_bha
WHERE books_has_authors_id = :books_has_authors_id_selected

--Delete from Books_Has_Authors

DELETE FROM Books_Has_Authors WHERE books_has_authors_id = :books_has_authors_id_selected

-- Join Books_Has_Authors and Books

SELECT Books_Has_Authors.books_book_id FROM Books_Has_Authors
INNER JOIN Books ON Books_Has_Authors.books_book_id = Books.book_id

-- Join Books_Has_Authors and Authors

SELECT Books_Has_Authors.authors_author_id FROM Books_Has_Authors
INNER JOIN Authors ON Books_Has_Authors.authors_author_id = Authors.author_id

--Dynamic search for Books_Has_Authors

SELECT books_book_id, authors_author_id FROM Books_Has_Authors
WHERE [books_book_id = :books_book_id_bha]
[AND] [authors_author_id = :authors_author_id_bha]