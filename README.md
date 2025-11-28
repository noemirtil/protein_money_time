# Protein Money Time 🍽️

A Flask web application that helps users find and upload products based on their nutritional value, price, and cooking time. Built with Python, Flask, and PostgreSQL.

## 🎯 Project Overview

This recipe recommendation app allows users to:

- Find ready-to-eat products based on health value and cooking time
- Compare products by price and nutritional information
- Contribute product data to the community database
- Manage user authentication and profiles

## 🛠️ Technologies

- **Backend:** Python 3.x, Flask
- **Database:** PostgreSQL (Neon Cloud)
- **Forms:** Flask-WTF
- **Authentication:** Flask-Login
- **Database Driver:** psycopg2

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- A Neon account (for cloud PostgreSQL database)

## 🚀 Setup Instructions

### 1. Clone the Repository

    ```bash
    git clone https://github.com/noemirtil/protein_money_time.git
    cd protein_money_time
    ```

### 2. Create Virtual Environment

    ```bash
    # Create venv
    python -m venv venv

    # Activate (Windows)
    .\venv\Scripts\Activate.ps1

    # Activate (Mac/Linux)
    source venv/bin/activate
    ```

### 3. Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

If `requirements.txt` doesn't exist yet, install manually:

    ```bash
    pip install flask flask-wtf flask-login python-dotenv psycopg
    ```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

    ```bash
    SECRET_KEY=your-secret-key-here
    # Example for a secure cloud connection (recommended)
    # DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
    # Example for a local/unsecured connection
    DATABASE_URL=postgresql://user:password@localhost:5432/database_name
    ```

Database Setup: The database schema (app/db/schema.sql) must be executed against your PostgreSQL instance manually before running the application.

Database Connection String:

Obtain the connection string (URL) for your PostgreSQL database from your provider or local setup.

Ensure the URL is correctly formatted for use with psycopg.

Paste it into your .env file as the DATABASE_URL.

### 5. Run the Application

    ```bash
    python app.py
    ```

The app will be available at: `http://localhost:5000`

## 🗂️ Project Structure

    ```
    protein_money_time/
    ├── app/
    │   ├── __init__.py           # App factory
    │   ├── extensions.py         # Flask extensions (CSRF, Login Manager)
    │   ├── db/
    │   │   ├── __init__.py
    │   │   ├── connection.py     # Database connection helpers
    │   │   └── schema.sql        # Database schema
    │   ├── forms/
    │   │   ├── __init__.py
    │   │   └── auth_forms.py     # Authentication forms
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   ├── auth.py           # Auth routes (login, register, logout)
    │   │   └── main.py           # Main application routes
    │   ├── templates/
    │   │   ├── base.html
    │   │   └── auth/
    │   │       ├── login.html
    │   │       └── register.html
    │   └── static/
    │       ├── css/
    │       └── js/
    ├── config.py                 # Configuration settings
    ├── app.py                    # Application entry point
    ├── .env                      # Environment variables (not in git)
    ├── .gitignore
    ├── requirements.txt
    └── README.md
    ```

## 🧪 Testing Database Connection

Visit these test routes to verify your setup:

- `http://localhost:5000/` - Main page
- `http://localhost:5000/auth/test` - Auth blueprint test
- `http://localhost:5000/auth/test-connection` - Database connection info
- `http://localhost:5000/auth/test-db` - Users table test

## 📝 Available Flask Commands

    ```bash
    # Run development server
    python run.py
    ```

## 🔑 Database Schema

    - Currently implemented tables:

    - users (User authentication and contributions)

    - brands (Product manufacturers)

    - products (Nutritional information per 100g)

    - currencies (ISO 4217 codes)

    - countries (Country names)

    - junction_currency_country (Many-to-many link)

    - stores (Locations where prices were observed)

    - prices (Price, weight, and date data)

## 🌿 Git Workflow

    ```bash
    # Main development branch
    git checkout dev

    # Create feature branch
    git checkout -b feature/your-feature-name

    # After completing work
    git add .
    git commit -m "feat: description of changes"
    git push origin feature/your-feature-name

    # Merge to dev
    git checkout dev
    git merge feature/your-feature-name
    git push origin dev
    ```

## 👥 Team

- **Rossana** - Full Stack Developer (Auth, User Management, User Templates)
- **Noémie** - Database Architect (Schema Design)

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-Login Docs](https://flask-login.readthedocs.io/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)

## 🐛 Troubleshooting

### Database connection issues

- Verify your .env file has the correct DATABASE_URL format.

- Check that your PostgreSQL database server is running and accessible.

- If connecting to a cloud database, ensure you have the correct host, port, credentials, and sslmode=require if necessary.

- Ensure you have manually run schema.sql against your database.

### Import errors

- Activate your virtual environment

- Run pip install -r requirements.txt

## 📄 License

This project is for educational purposes as part of a Full Stack Development bootcamp.

Status: 🚧 In Development

Last Updated: November 2025