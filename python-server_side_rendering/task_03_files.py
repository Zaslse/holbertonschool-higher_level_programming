#!/usr/bin/python3
"""Display and filter product data from JSON or CSV using Flask."""

import csv
import json
from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)
DATA_DIR = Path(__file__).resolve().parent


def read_json_products():
    """Load the product records from the JSON file."""
    with open(DATA_DIR / 'products.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def read_csv_products():
    """Load the product records from the CSV file."""
    with open(DATA_DIR / 'products.csv', 'r', encoding='utf-8',
              newline='') as file:
        return list(csv.DictReader(file))


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
    """Render products selected by source and optional product identifier."""
    source = request.args.get('source')
    product_id = request.args.get('id')

    if source not in ('json', 'csv'):
        return render_template('product_display.html',
                               products=[], error='Wrong source')

    try:
        if source == 'json':
            records = read_json_products()
        else:
            records = read_csv_products()
    except (OSError, ValueError, csv.Error) as error:
        return render_template('product_display.html',
                               products=[], error='Error reading data: {}'.format(error))

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
