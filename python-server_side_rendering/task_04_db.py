#!/usr/bin/python3
"""Render product data from JSON, CSV, or a SQLite database."""

import csv
import json
import sqlite3
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
DATA_DIR = Path(__file__).resolve().parent


def read_json_products():
    """Read product dictionaries from JSON."""
    with open(DATA_DIR / 'products.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def read_csv_products():
    """Read product dictionaries from CSV."""
    with open(DATA_DIR / 'products.csv', 'r', encoding='utf-8',
              newline='') as file:
        return list(csv.DictReader(file))


def read_sql_products():
    """Read product dictionaries from the SQLite Products table."""
    database_path = DATA_DIR / 'products.db'
    if not database_path.is_file():
        raise sqlite3.OperationalError('products.db does not exist')

    with sqlite3.connect(str(database_path)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            'SELECT id, name, category, price FROM Products ORDER BY id'
        ).fetchall()
        return [dict(row) for row in rows]


@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html')


@app.route('/products')
def products():
    """Display and optionally filter products for the selected data source."""
    source = request.args.get('source')
    product_id = request.args.get('id')
    readers = {
        'json': read_json_products,
        'csv': read_csv_products,
        'sql': read_sql_products
    }

    if source not in readers:
        return render_template('product_display.html',
                               products=[], error='Wrong source')

    try:
        records = readers[source]()
    except (OSError, ValueError, csv.Error, sqlite3.Error) as error:
        return render_template('product_display.html',
                               products=[], error='Database or file error: {}'.format(error))

    if product_id is not None:
        records = [product for product in records
                   if str(product.get('id')) == product_id]
        if not records:
            return render_template('product_display.html',
                                   products=[], error='Product not found')

    return render_template('product_display.html',
                           products=records, error=None)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
