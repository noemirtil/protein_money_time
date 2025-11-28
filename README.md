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
    pip install flask flask-wtf flask-login python-dotenv psycopg2-binary
    ```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

    ```bash
    SECRET_KEY=your-secret-key-here
    DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
    ```

**Get your DATABASE_URL from Neon:**

1. Go to [neon.tech](https://neon.tech/)
2. Sign in and select your project
3. Copy the connection string from the dashboard
4. Paste it into your `.env` file

### 5. Initialize Database

    ```bash
    flask init-db
    ```

This command will:

- Connect to your PostgreSQL database
- Drop existing tables (if any)
- Create fresh tables from `app/db/schema.sql`

### 6. Run the Application

    ```bash
    python run.py
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
    ├── run.py                    # Application entry point
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
    # Initialize/reset database
    flask init-db

    # Run development server
    python run.py
    ```

## 🔑 Database Schema

Currently implemented tables:

### Users Table

- `id` (SERIAL, PRIMARY KEY)
- `username` (VARCHAR(32), UNIQUE)
- `email` (VARCHAR(320))
- `password` (VARCHAR(64), hashed)
- `contributions` (INTEGER)

*More tables (products, brands, stores, prices, currencies) will be added as the project develops.*

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
- [Neon Docs](https://neon.tech/docs)

## 🐛 Troubleshooting

### Database connection issues

- Verify your `.env` file has the correct DATABASE_URL
- Check that Neon database is active (free tier may sleep)
- Ensure `sslmode=require` is in your connection string

### "relation does not exist" errors

- Run `flask init-db` to create tables
- Check that `schema.sql` has no commented-out DROP statements

### Import errors

- Activate your virtual environment
- Run `pip install -r requirements.txt`

## 📄 License

This project is for educational purposes as part of a Full Stack Development bootcamp.

---

**Status:** 🚧 In Development

**Last Updated:** November 2025
