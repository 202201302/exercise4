-- Create database
CREATE DATABASE IF NOT EXISTS library;

-- Use the library database
USE library;

-- Create Books table
CREATE TABLE IF NOT EXISTS Books (
  BookID INT AUTO_INCREMENT PRIMARY KEY,
  Title VARCHAR(255) NOT NULL,
  Author VARCHAR(255) NOT NULL,
  ISBN VARCHAR(255) NOT NULL,
  Status VARCHAR(255) NOT NULL
);

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
  UserID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  Email VARCHAR(255) NOT NULL
);

-- Create Reservations table
CREATE TABLE IF NOT EXISTS Reservations (
  ReservationID INT AUTO_INCREMENT PRIMARY KEY,
  BookID INT NOT NULL,
  UserID INT NOT NULL,
  ReservationDate DATE,
  FOREIGN KEY (BookID) REFERENCES Books(BookID),
  FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Insert sample data
INSERT INTO Books (Title, Author, ISBN, Status)
VALUES
  ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Available'),
  ('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'Reserved'),
  ('1984', 'George Orwell', '9780451524935', 'Available'),
  ('Pride and Prejudice', 'Jane Austen', '9780141439518', 'Available'),
  ('The Catcher in the Rye', 'J.D. Salinger', '9780316769174', 'Reserved');

INSERT INTO Users (Name, Email)
VALUES
  ('John Smith', 'john@example.com'),
  ('Emma Johnson', 'emma@example.com'),
  ('Michael Williams', 'michael@example.com'),
  ('Sophia Brown', 'sophia@example.com'),
  ('William Taylor', 'william@example.com');

INSERT INTO Reservations (BookID, UserID, ReservationDate)
VALUES
  (2, 1, '2023-09-01'),
  (4, 3, '2023-09-05');