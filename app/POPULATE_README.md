Usage notes for `populate_db.py` script

This file explains how to run the population script included at `app/populate_db.py`.

How to run

- Use the module name (no `.py` suffix) when using `-m`:

```bash
python3 -m app.populate_db
```

- Or run the file directly from the project root:

```bash
python3 app/populate_db.py
```

Notes

- The script is idempotent: it checks existing records before creating duplicates.
- It requires your Flask app configuration to be correct (database URI etc) and a virtual environment with dependencies installed (see `requirements.txt`).
- The script will create tables via the `create_app` call in `app/__init__.py`, so it is safe for fresh databases.

Troubleshooting

- If you see a ModuleNotFoundError mentioning `__path__` when using `python -m app.populate_db.py`, that means you included the `.py` suffix. Use `python -m app.populate_db` instead.
