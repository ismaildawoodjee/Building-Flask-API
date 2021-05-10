# Dependencies
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flask app
app = Flask(__name__)

# Configure SQLite database file
# SQLAlchemy is object-relational mapper, OOP for SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# Configure SQLite3 to enforce foreign key constraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """Looks like once the DB Engine is connected, 
    foreign key constraints are turned on.
    """

    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


# Create a database instance to connect DB with Flask App
db = SQLAlchemy(app)
now = datetime.now()

# Class models for each table in the database
class User(db.Model):
    """Model for creating the User table with columns"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    address = db.Column(db.String(256))
    phone = db.Column(db.String(64))
    posts = db.relationship("BlogPost")  # foreign key for BlogPost
