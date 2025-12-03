# Protein 💪 Money 💰 Time ⏱️

####[`https://github.com/noemirtil/protein_money_time/tree/dev`](https://github.com/noemirtil/protein_money_time/tree/dev)

A Flask web application that helps users find and upload products based on their nutritional value, price, and cooking time. Built with Python, Flask, PostgreSQL, and deployed on Google's Cloud SQL at [`https://test-270421769412.europe-southwest1.run.app/`](https://test-270421769412.europe-southwest1.run.app/)

## 🎯 Project Overview

This recipe recommendation app allows users to:

- Find ready-to-eat products based on price per kg, nutritional values and cooking time
- Compare with home-made recipes and save your prefered meals
- Contribute recipes and product data to the community database
- Earn medals through contributions
- Manage user authentication and profiles

![https://github.com/noemirtil/protein_money_time/blob/dev/app/static/img/about.png](https://github.com/noemirtil/protein_money_time/blob/dev/app/static/img/about.png)

## 🛠️ Technologies

- **Backend:** Python 3.x, Flask
- **Database:** PostgreSQL (Google's Cloud SQL)
- **Forms:** Flask-WTF
- **Authentication:** Flask-Login
- **Database Driver:** psycopg3

## 📋 Prerequisites

### - To only run it as a client:
- Just visit [`https://test-270421769412.europe-southwest1.run.app/`](https://test-270421769412.europe-southwest1.run.app/)

### - To install it on your own computer:
- Python 3.8 or higher
- Psql 18.1 or higher
- Git

## 🚀 Setup Instructions

### 1. Clone the Repository

```
$ git clone https://github.com/noemirtil/protein_money_time.git
$ cd protein_money_time
```

### 2. Create Virtual Environment

```
# Create .venv
$ python -m venv .venv

# Activate .venv (Windows)
$ .\venv\Scripts\Activate.ps1

# Activate .venv (Mac/Linux)
$ source .venv/bin/activate
``` 
    

### 3. Install Dependencies

```
$ pip install -r requirements.txt
```

### 4. Local database setup

More info on this process: [https://www.postgresql.org/docs/current/app-createdb.html](https://www.postgresql.org/docs/current/app-createdb.html)

```
$ createdb your_db_name
```

The database schema `protein_money_time/app/db/app/db/schema.sql` must then be executed against your PostgreSQL instance manually before running the application. Run psql from your `protein_money_time/app/db/` folder and then enter:

```
your_db_name=# \i schema.sql
# And then seed the tables:
your_db_name=# \i seed.sql
```

To allow the app to access your database, create a personal `.env` file in the root directory:

```
$ nano .env
```

With nano editor, edit .env with the following model and save the file:

```
# You can use default 'postgres' username
DB_USER=your_psql_username
# You can leave empty if you don't need a password
DB_PASSWORD=your_psql_password
DB_NAME=your_db_name
# For local dev, leave CLOUD_SQL_INSTANCE empty as following:
CLOUD_SQL_INSTANCE=
```


### 5. Run the Application

```
$ python app.py
```

The app will be available in your browser at: `http://127.0.0.1:8000`

## 🗂️ Project Structure

```
protein_money_time/
├── .venv/ 						# Virtual environment
├── app/
│   ├── __init__.py           # App factory
│   ├── extensions.py         # Flask extensions (CSRF, Login Manager)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── connection.py     # Database connection helpers
│   │   ├── *.csv				# Some seeding files called by seed.sql
│   │   ├── seed.sql			# Database first seed
│   │   ├── queries.sql			# Some queries we might use
│   │   └── schema.sql        # Database architecture
│   ├── forms/
│   │   ├── __init__.py
│   │   └── auth_forms.py     # Authentication forms
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py     		# The User class
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Auth routes (login, register, logout)
│   │   ├── main.py           # Main application routes
│   │   └── presave.py        # Route to feed the db with new products, brands, prices, store
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── extensions.py		# CSRFProtect and LoginManager
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── main/
│   │       ├── index.html
│   │       └── presave.html
│   └── static/
│       ├── css/
│       └── js/
├── .env							# Personal db connection variables (not in github)
├── config.py                 # Configuration settings
├── app.py                    # Application entry point
├── LICENSE						# GNU affero general public license
├── pyproject.toml				# Instructions for pip
├── .gitignore					# Tell git what to ignore
├── requirements.txt			# What you'll need to pip install
├── wsgi.py						# For production mode only
├── Procfile						# For production mode only
└── README.md						# This file

```

## 🧪 Testing Database Connection

Visit these test routes to verify your setup:

- [http://127.0.0.1:8000/](http://127.0.0.1:8000/) - Main page
- [http://127.0.0.1:8000/auth/test](http://127.0.0.1:8000/auth/test) - Auth blueprint test
- [http://127.0.0.1:8000/presave](http://127.0.0.1:8000/presave) - Database feeding page with new products, brands, prices, store


## 🔑 Database Schema

### Currently 10 implemented tables:

- users (User authentication and contributions)

- brands (Product manufacturers)

- products (Nutritional information per 100g)

- currencies (ISO 4217 codes)

- countries (Country names)

- junction_currency_country (Many-to-many link)

- stores (Locations where prices were observed)

- prices (Price, weight, and date data)

- presaved_products (user contributions before INSERT on completion, triggered by plpgsql language)

- presaved_prices (user contributions before INSERT on completion, triggered by plpgsql language)
    
### Take a look at `schema.sql` 


## 🌿 Git Workflow

```
# Main development branch
$ git checkout dev

# Create feature branch
$ git switch -c feature/your-feature-name

# Frequent atomic commits
$ git add .
$ git commit -m "feat: description of changes"
$ git push origin feature/your-feature-name

# Merge to dev
$ git switch dev
$ git merge feature/your-feature-name
$ git push origin dev
```

## 👥 Team

- **Rossana** - Full Stack Developer (Auth, User Management, User Templates)
- **Noémie** - Database Architect (Schema Design, DevOps, Seeding)

## 📚 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-Login Docs](https://flask-login.readthedocs.io/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)

## 🐛 Troubleshooting

### Database connection issues

- Verify your .env file follows instructions.

- Check that your PostgreSQL database server is running and accessible.

- Ensure you have manually run schema.sql and seed.sql inside psql against your database.

### Import errors

- Activate your virtual environment

- Run pip install -r requirements.txt

## 📄 License

This project, begun for educational purposes as part of a Full Stack Development bootcamp, is now licensed under GNU affero general public license.

Status: 🚧 In Development

Last Updated: December 2025