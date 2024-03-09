# Library Management System

This project is a simple library management system developed as a high school project using Python and SQL. It allows users to sign up, log in, view their issue history, and issue books from the library.

## Features

- **Sign Up**: Users can create a new account by providing a username and password.
- **Log In**: Existing users can log in securely to access their accounts.
- **Issue Books**: Users can search for books by title and author, view book details, and issue books from the library.
- **View Issue History**: Users can view their recently issued books and currently issued books.

## Technologies Used

- **Python**: The backend of the application is written in Python, utilizing libraries such as `pymysql` for interacting with the MySQL database and `tkinter` for building the GUI.
- **MySQL**: The database management system used for storing user information and book details.
- **Selenium**: Used for web scraping to fetch book details from Goodreads.
- **Chrome WebDriver**: Required for Selenium to interact with the Chrome browser.

## Project Structure

- **main.py**: Contains the main functionality of the library management system, including sign up, log in, and issue history.
- **bookdetails.py**: Handles web scraping using Selenium to fetch book details from Goodreads.
- **booknames.txt**: Contains a list of book titles and authors to be used for book searches.
- **secrets.py**: Stores sensitive information such as database credentials (not committed to version control).
