#!/usr/bin/python3
"""Render static pages and a dynamic list of items loaded from JSON."""

import json
from pathlib import Path

from flask import Flask, render_template

app = Flask(__name__)
DATA_DIR = Path(__file__).resolve().parent


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


@app.route('/items')
def items():
    """Read items from JSON and render the list or its empty state."""
    with open(DATA_DIR / 'items.json', 'r', encoding='utf-8') as data_file:
        data = json.load(data_file)
    return render_template('items.html', items=data.get('items', []))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
