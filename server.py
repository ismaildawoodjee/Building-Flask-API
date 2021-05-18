# Dependencies
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import linked_list
import hash_table
import binary_search_tree
import custom_queue

import random

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
    """Model for creating the User table with columns."""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    address = db.Column(db.String(256))
    phone = db.Column(db.String(64))
    # foreign key for BlogPost
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):
    """Table class for BlogPost model, 
    since this is going to be an API for blogs. Should inherit db.Model.
    """
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(256))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@app.route("/user", methods=["POST"])
def create_user():
    """Create route to route the POST request to this function,
    whenever the `/user` rule is appended to the URL. In simple
    terms, this function creates a new user and puts the data on the DB.
    """
    data = request.get_json()  # request object provided by Flask
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    """Get all users in descending order, after first storing their
    data within a linked list. Returning 200 if successful.
    """

    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    """Get all users in ascending order, after first storing their
    data within a linked list. Returning 200 if successful.
    """

    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):

    users = User.query.all()
    all_users_ll = linked_list.LinkedList()

    for user in users:
        all_users_ll.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone
            }
        )

    user = all_users_ll.get_user_by_id(user_id)
    return jsonify(user), 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Query user and delete them. But if user table references another
    blog post table via foreign key, the blog posts also need to be deleted.
    """

    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()

    return jsonify({}), 200


@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "user does not exist!"}), 400

    ht = hash_table.HashTable(10)
    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id")
    )
    db.session.add(new_blog_post)
    db.session.commit()

    return jsonify({"message": "new blog post created!"}), 200

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()  # get all blogs in asc order
    random.shuffle(blog_posts)
    bst = binary_search_tree.BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id
        })
    post = bst.search(blog_post_id)
    
    if not post:
        return jsonify({"message": "post not found"})
    return jsonify(post), 200


@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    """Convert all characters in a blog post into a number and sum them
    up. For what?
    """
    blog_posts = BlogPost.query.all()

    q = custom_queue.Queue()
    for post in blog_posts:
        q.enqueue(post)

    return_list = []
    for _ in range(len(blog_posts)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.data.body = numeric_body

        return_list.append({
            "id": post.data.id,
            "title": post.data.title,
            "body": post.data.body,
            "user_ud": post.data.user_id
        })

    return jsonify(return_list), 200


@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
