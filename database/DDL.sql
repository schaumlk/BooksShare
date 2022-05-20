--Ariel Rosenthal and Katie Schaumleffle
--Project Step 2
--Due 4/28/2022

--Data Definition Queries

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

--Users table

CREATE TABLE `Users` (
    `user_id` INT AUTO_INCREMENT UNIQUE NOT NULL,
    `username` VARCHAR(70) NOT NULL,
    `password` VARCHAR(15) NOT NULL,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(75) NOT NULL,
    `created_at` TIMESTAMP,
    `modified_at` TIMESTAMP,
    PRIMARY KEY(`user_id`)
);

--Books table

CREATE TABLE `Books` (
    `book_id` INT AUTO_INCREMENT UNIQUE NOT NULL,
    `title` VARCHAR(25) NOT NULL,
    `description` VARCHAR(200),
    `price` DECIMAL(5) NOT NULL,
    `inventory_id` INT NOT NULL,
    `created_at` TIMESTAMP,
    `modified_at` TIMESTAMP,
    PRIMARY KEY(`book_id`),
    FOREIGN KEY(`inventory_id`) REFERENCES `Inventory`(`inventory_id`) ON DELETE CASCADE
);

--Inventory table

CREATE TABLE `Inventory` (
    `inventory_id` INT AUTO_INCREMENT UNIQUE NOT NULL,
    `quantity` INT NOT NULL,
    `book_id` INT NOT NULL,
    `trasaction_id` INT NOT NULL,
    `created_at` TIMESTAMP,
    `modified_at` TIMESTAMP,
    PRIMARY KEY(`inventory_id`),
    FOREIGN KEY(`book_id`) REFERENCES `Books`(`book_id`) ON DELETE CASCADE,
    FOREIGN KEY(`transaction_id`) REFERENCES `Transactions`(`transaction_id`) ON DELETE CASCADE
);

--Transaction table

CREATE TABLE `Transactions`(
    `transaction_id` INT AUTO_INCREMENT UNIQUE,
    `user_id` INT NOT NULL, 
    `inventory_id` INT,
    `total_price` DECIMAL NOT NULL,
    `created_at` TIMESTAMP,
    `modified_at` TIMESTAMP,
    PRIMARY KEY(`transaction_id`),
    FOREIGN KEY(`user_id`) REFERENCES `Users`(`user_id`) ON DELETE CASCADE,
    FOREIGN KEY(`inventory_id`) REFERENCES `Inventory`(`inventory_id`) ON DELETE CASCADE
);

--Authors table

CREATE TABLE `Authors` (
    `author_id` INT AUTO_INCREMENT UNIQUE,
    `author_fname` VARCHAR(50) NOT NULL,
    `author_lname` VARCHAR(50) NOT NULL,
    `book_id` INT NOT NULL,
    PRIMARY KEY(`author_id`),
    FOREIGN KEY(`book_id`) REFERENCES `Books`(`book_id`) ON DELETE CASCADE
);

--Books_Has_Authors table

CREATE TABLE `Books_Has_Authors` (
    `books_book_id` INT,
    `authors_author_id` INT,
    PRIMARY KEY(`books_book_id`)
    FOREIGN KEY(`books_book_id`) REFERENCES `Books`(`book_id`),
    FOREIGN KEY(`authors_author_id`) REFERENCES `Authors`(`author_id`) ON DELETE CASCADE
);

--Sample inserted data

--Inserted into Users

INSERT INTO `Users`(`user_id`, `username`, `password`, `first_name`, `last_name`, `email`)
VALUES
(1423, 'cupcake', 'gabjjsd', 'Abby', 'Miller', 'amiller@gmail.com'),
(56789, 'math72', 'jdhab', 'Jacob', 'Smith', 'jakey@gmail.com'),
(1278, 'doglover411', 'kjnc', 'Kailey', 'Alcott', 'ilovedogs2@gmail.com')

--Inserted into Books

INSERT INTO `Books`(`book_id`, `title`, `description`, `price`, `inventory_id`)
VALUES
(12, 'HOW TO SURVIVE', 'Survival of the fittest', 12.00, SELECT inventory_id FROM Inventory WHERE inventory_id = 123),
(911, 'Science 101', 'The best science book.', 40.00, SELECT inventory_id FROM Inventory WHERE inventory_id = 456),
(1410, 'Python For Everyone', 'The best way to learn Python', 19.99, SELECT inventory_id FROM Inventory WHERE inventory_id = 789),

--Inserted into Inventory

INSERT INTO `Inventory`(`inventory_id`, `quantity`, `book_id`, `transaction_id`)
VALUES
(123, 62, SELECT book_id FROM Books WHERE book_id = 12, SELECT trasaction_id FROM Transactions WHERE transaction_id = 1266),
(456, 12, SELECT book_id FROM Books WHERE book_id = 911, SELECT trasaction_id FROM Transactions WHERE transaction_id = 8762),
(789, 76, SELECT book_id FROM Books WHERE book_id = 1410, SELECT trasaction_id FROM Transactions WHERE transaction_id = 9826)

--Inserted into Transactions

INSERT INTO `Transactions`(`transaction_id`, `user_id`, `inventory_id`, `total_price`)
VALUES
(1266, SELECT user_id FROM Users WHERE user_id = 1423, SELECT inventory_id FROM Inventory WHERE inventory_id = 123, 12.00),
(8762, SELECT user_id FROM Users WHERE user_id = 56789, SELECT inventory_id FROM Inventory WHERE inventory_id = 456, 40.00),
(9826, SELECT user_id FROM Users WHERE user_id = 1278, SELECT inventory_id FROM Inventory WHERE inventory_id = 789, 19.99)

--Inserted into Authors

INSERT INTO `Authors`(`author_id`, `author_fname`, `author_lname`, `book_id`)
VALUES
(1231, 'Samuel', 'Keaton', SELECT book_id FROM Books WHERE book_id = 654),
(987, 'Gabriel', 'Van Hess', SELECT book_id FROM Books WHERE book_id = 911),
(7182, 'Alexa', 'Koe', SELECT book_id FROM Books WHERE book_id = 1410)

--Inserted into Books_Has_Authors

INSERT INTO `Books_Has_Authors`(`books_book_id`, `authors_author_id`)
VALUES
(SELECT book_id FROM Books WHERE book_id = 12, SELECT author_id FROM Authors WHERE author_id = 1231),
(SELECT book_id FROM Books WHERE book_id = 911, SELECT author_id FROM Authors WHERE author_id = 987),
(SELECT book_id FROM Books WHERE book_id = 1410, SELECT author_id FROM Authors WHERE author_id = 7182)

SET FOREIGN_KEY_CHECKS=1;
COMMIT;