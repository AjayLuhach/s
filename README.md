# s# Flask User Authentication with Google OAuth Documentation

This documentation provides an overview of a Flask web application that uses Google OAuth for user authentication. The application allows users to log in using their Google accounts and performs basic user management tasks, such as user registration, login, logout, profile viewing, and updates.

## Table of Contents

1. **Introduction**
   - Application Overview
   - Prerequisites

2. **Installation and Setup**
   - Installing Dependencies
   - Configuration

3. **Application Structure**
   - Project Structure
   - Key Components

4. **Google OAuth Configuration**
   - Setting up Google OAuth Credentials
   - Configuring OAuth in Flask

5. **User Management**
   - User Registration
   - User Login
   - User Logout
   - Profile Viewing and Updates

6. **Running the Application**
   - Starting the Development Server
   - Accessing the Application

---

## 1. Introduction

### Application Overview

This Flask application demonstrates how to integrate Google OAuth into a web application for user authentication. It includes features like user registration, login, and management of user profiles. Users can sign in using their Google accounts, and their Google-provided information is used to create and update user profiles within the application.

### Prerequisites

Before you begin, make sure you have the following prerequisites installed:

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Login
- Flask-SQLAlchemy
- psycopg2-binary (for PostgreSQL support)
- Flask-Bcrypt
- Flask-OAuthlib

## 2. Installation and Setup

### Installing Dependencies

Create a virtual environment and install the required dependencies listed in the `requirements.txt` file. Use the following command:

```bash
pip install -r requirements.txt
```

### Configuration

In the application code, ensure that you configure your Google OAuth credentials and other settings appropriately.

## 3. Application Structure

### Project Structure

- `app.py`: The main application file containing Flask routes and OAuth configuration.
- `services/`: Directory for services handling CRUD operations on user data.
- `domain/`: Contains the user model (e.g., `user_model.py`).
- `infrastructure/`: Configuration files for the database (e.g., `user_database.py`).
- `templates/`: HTML templates for the application's web pages.

### Key Components

- `Flask`: The core Flask web framework for routing and handling HTTP requests.
- `Flask-Login`: Extension for managing user sessions.
- `Flask-OAuthlib`: Extension for OAuth2 integration, specifically for Google OAuth.
- `SQLAlchemy`: ORM (Object-Relational Mapping) library for database interactions.
- `Flask-Bcrypt`: Used for hashing user passwords securely.

## 4. Google OAuth Configuration

### Setting up Google OAuth Credentials

To use Google OAuth, you need to create a project on the Google Developers Console and configure OAuth credentials. Ensure that you set the correct redirect URIs for your Flask application. The credentials typically include a **Client ID** and a **Client Secret**.

### Configuring OAuth in Flask

In the `app.py` file, you'll find the OAuth configuration for Google. Replace the placeholders for `consumer_key` and `consumer_secret` with your actual Google OAuth credentials.

## 5. User Management

### User Registration

Users can register on the application by providing a username, password, first name, last name, and email address. Passwords are securely hashed before storage.

### User Login

Registered users can log in using their usernames and passwords. Passwords are hashed and checked for authentication.

### User Logout

Logged-in users can log out of their accounts, terminating their sessions.

### Profile Viewing and Updates

- Users can view their profiles, which include their username, first name, last name, and email.
- Users can update their profiles, including their first name, last name, email, and password.

## 6. Running the Application

### Starting the Development Server

To start the development server, run the following command:

```bash
python app.py
```

The application should be accessible at `http://localhost:80` in your web browser.

### Accessing the Application

1. Access the home page at `http://localhost:80`.
2. Click on the "Google Login" button to initiate Google OAuth login.
3. Upon successful login, users will be redirected to the "All Users" page, displaying a list of users.
4. Users can navigate to the "Profile" page to view and update their information.
5. Users can log out by clicking the "Logout" button.

---

You've successfully set up a Flask web application with Google OAuth for user authentication and basic user management features. Customize and expand upon this foundation to build more complex applications as needed.
