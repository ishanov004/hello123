# Warehouse Inventory Manager

A small Flask web application for tracking equipment purchases, sales, and stock levels. The interface is in Russian and uses a simple SQLite database.

## Features

- Record equipment purchases and sales
- Organize products by category
- Browse and manage countries of origin
- View current warehouse stock
- Generate revision reports over date ranges

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Optionally create a `.env` file to configure the application:

```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE=equipment.db
DELETE_SECRET=<secret code for deletions>
```

## Running

Initialize the database and start the development server:

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

## Project Structure

See `structure.txt` for an overview of folders and template files.

Enjoy using the app! 🎉
