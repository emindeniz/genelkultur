import os
import pyodbc, struct
from azure import identity
import click
from flask import current_app, g
from flask.cli import with_appcontext
from typing import Union

connection_string = os.environ["AZURE_SQL_CONNECTIONSTRING"]

def get_db():
    if "db" not in g:
        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=True)
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
        g.db = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})

    return g.db

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)