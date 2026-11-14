# Python - Server-Side Rendering

This Holberton School project uses Python, Flask, Jinja2, JSON, CSV, and
SQLite to generate HTML on the server and produce personalized invitations.

## Tasks

- `task_00_intro.py`: generate invitations from a text template.
- `task_01_jinja.py`: render Home, About, and Contact pages with shared templates.
- `task_02_logic.py`: render an items list loaded from `items.json`.
- `task_03_files.py`: display and filter products loaded from JSON or CSV.
- `task_04_db.py`: also display and filter products from SQLite.

## Setup and run

Install Flask: `python -m pip install Flask`

Run an app from inside the `python-server_side_rendering` folder:

```sh
python task_01_jinja.py
python task_02_logic.py
python task_03_files.py
python task_04_db.py
```

Each application uses port 5000; start only one at a time.

Examples:

- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/about`
- `http://127.0.0.1:5000/contact`
- `http://127.0.0.1:5000/items` (task 2)
- `http://127.0.0.1:5000/products?source=json` (tasks 3 and 4)
- `http://127.0.0.1:5000/products?source=csv&id=2` (tasks 3 and 4)
- `http://127.0.0.1:5000/products?source=sql` (task 4)

`products.db` contains the example database. `create_db.py` can safely
initialize it again without duplicating the example rows.
