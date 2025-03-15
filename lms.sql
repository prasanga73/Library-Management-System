
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
SET time_zone = "+00:00";
START TRANSACTION;
CREATE DATABASE IF NOT EXISTS lms;
USE lms;
COMMIT;

START TRANSACTION;
CREATE TABLE IF NOT EXISTS `admins` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(250) NOT NULL,
  `mobile` int(10) NOT NULL
)ENGINE=InnoDB;



INSERT INTO `admins` (`id`, `name`, `email`, `password`, `mobile`) VALUES
(1, 'admin', 'admin@gmail.com', 'admin@1234', 1148458757);


CREATE TABLE IF NOT EXISTS `authors` (
  `author_id` int(11) NOT NULL,
  `author_name` varchar(250) NOT NULL,
  PRIMARY KEY (`author_id`)
) ENGINE=InnoDB;



INSERT INTO `authors` (`author_id`, `author_name`) VALUES
(102, 'Dostoevsky'),
(103, 'Chetan Bhagat'),
(104, 'Jane Austen'),
(105,'Oscar Wilde');




CREATE TABLE IF NOT EXISTS `books` (
  `book_id` int(11) NOT NULL,
  `book_name` varchar(250) NOT NULL,
  `author_id` int(11) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `book_no` int(11) NOT NULL,
  `book_price` int(11) NOT NULL,
  PRIMARY KEY (`book_id`),
  FOREIGN KEY (`author_id`) REFERENCES `authors`(`author_id`)
) ENGINE=InnoDB;



INSERT INTO `books` (`book_id`,`book_name`, `author_id`, `cat_id`, `book_no`, `book_price`) VALUES
( 1,'Pride and Prejudice', 104, 1, 4518, 270),
( 2,'Picture of Dorian Gray', 105, 2, 6541, 300);





CREATE TABLE IF NOT EXISTS `category` (
  `cat_id` int(11) NOT NULL,
  `cat_name` varchar(100) NOT NULL
) ENGINE=InnoDB; 



INSERT INTO `category` (`cat_id`, `cat_name`) VALUES
(1, 'Computer Science'),
(2, 'Novel'),
(4, 'Motivational'),
(5, 'Story');

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `mobile` int(25) NOT NULL,
  `address` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;



INSERT INTO `users` (`id`, `name`, `email`, `password`, `mobile`, `address`) VALUES
(4, 'user', 'user@gmail.com', 'user@1234', 9847483644, 'Dharan'),
(7, 'prasanga', 'prasanga@gmail.com', 'prasanga', 9847483644, 'Itahari');



CREATE TABLE IF NOT EXISTS `issued_books` (
  `s_no` int(11) NOT NULL,
  `book_id` int(11) NOT NULL, 
  `student_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `issue_date` longtext NOT NULL,
  FOREIGN KEY (`book_id`) REFERENCES `books`(`book_id`),  
  FOREIGN KEY (`student_id`) REFERENCES `users`(`id`)
)ENGINE=InnoDB;

INSERT INTO `issued_books` (`s_no`, `book_id`, `student_id`, `status`, `issue_date`) VALUES
(1, 1, 7, 1, '2025-03-12'),
(18, 2, 7, 1, '2020-04-22');


ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `category`
  ADD PRIMARY KEY (`cat_id`);


ALTER TABLE `issued_books`
  ADD PRIMARY KEY (`s_no`);


ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;


ALTER TABLE `category`
  MODIFY `cat_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;


ALTER TABLE `issued_books`
  MODIFY `s_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

COMMIT;

START TRANSACTION;

CREATE TABLE admins_backup LIKE admins;
ALTER TABLE admins_backup ADD COLUMN deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE authors_backup LIKE authors;
ALTER TABLE authors_backup ADD COLUMN deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE books_backup LIKE books;
ALTER TABLE books_backup ADD COLUMN deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE category_backup LIKE category;
ALTER TABLE category_backup ADD COLUMN deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE issued_books_backup LIKE issued_books;
ALTER TABLE issued_books_backup ADD COLUMN deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE users_backup LIKE users;
ALTER TABLE users_backup ADD COLUMN deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
COMMIT;

DELIMITER //
CREATE TRIGGER before_admin_delete
BEFORE DELETE ON admins
FOR EACH ROW
BEGIN
    INSERT INTO admins_backup SELECT *, NOW() FROM admins WHERE id = OLD.id;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_author_delete
BEFORE DELETE ON authors
FOR EACH ROW
BEGIN
    INSERT INTO authors_backup SELECT *, NOW() FROM authors WHERE author_id = OLD.author_id;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_book_delete
BEFORE DELETE ON books
FOR EACH ROW
BEGIN
    INSERT INTO books_backup SELECT *, NOW() FROM books WHERE book_id = OLD.book_id;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_category_delete
BEFORE DELETE ON category
FOR EACH ROW
BEGIN
    INSERT INTO category_backup SELECT *, NOW() FROM category WHERE cat_id = OLD.cat_id;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_issued_book_delete
BEFORE DELETE ON issued_books
FOR EACH ROW
BEGIN
    INSERT INTO issued_books_backup SELECT *, NOW() FROM issued_books WHERE s_no = OLD.s_no;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER before_user_delete
BEFORE DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO users_backup SELECT *, NOW() FROM users WHERE id = OLD.id;
END;
//
DELIMITER ;

DELIMITER //

-- Trigger whihc deletes issued books when a book is deleted
CREATE TRIGGER delete_issued_books_on_book_delete
BEFORE DELETE ON books
FOR EACH ROW
BEGIN
    DELETE FROM issued_books WHERE book_id = OLD.book_id;
END;
//

-- Trigger to delete issued books when a user is deleted
CREATE TRIGGER delete_issued_books_on_user_delete
BEFORE DELETE ON users
FOR EACH ROW
BEGIN
    DELETE FROM issued_books WHERE student_id = OLD.id;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER delete_books_on_author_delete
BEFORE DELETE ON authors
FOR EACH ROW
BEGIN
    DELETE FROM books WHERE author_id = OLD.author_id;
END;

//

DELIMITER ;
