import random
import sqlite3
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from flask import Flask, request, jsonify
import linked_list
import random
# RDM- relation database mapper / your code manipulates sql object
import hash_table
import binary_search_tree
import customer_queue
import stack
# from sqlalchemy import db
from sqlalchemy import event
import sqlalchemy.engine
from flask_sqlalchemy import SQLAlchemy

# app / instance of the database module
from sqlalchemy.engine import Engine

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0


# configure sqlite3 to enforce foreign key constraints
@event.listens_for(Engine, "connect")
# Allowing to configure the db connection to enforce foreign key constrains
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_key=ON;")
        cursor.close()


db = SQLAlchemy(app)
now = datetime.now()


# models
# user table
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


# Second table
class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# routes


@app.route("/user", methods=["POST"])
def create_user():
    # variable to store our request data //request object is provided by flask
    # get.json method -parse our request method as json allowing us to access our parameters via the key value

    data = request.get_json()
    new_user = User(
        name=data["name"],
        email=data["email"],
        address=data["address"],
        phone=data["phone"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 200  # 200 means that the request was successful


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users_linked_list = linked_list.LinkedList()

    # loop through the users in the db for each user , insert at the beginning a dictionary and convert into an
    # array/list in descending order /Returns 200->1

    for user in users:
        all_users_linked_list.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
        # convert the linked list into an array

    return jsonify(all_users_linked_list.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()
    all_users_linked_list = linked_list.LinkedList()

    # loop through the users in the db
    # for each user , insert at the beginning a dictionary and convert into an array/list in ascending order 1->200
    for user in users:
        all_users_linked_list.insert_at_end(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )
        # convert the linked list into an array

    return jsonify(all_users_linked_list.to_list()), 200


@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    users = User.query.all()
    # Create another instance of a linked list

    all_users_linked_list = linked_list.LinkedList()

    for user in users:
        all_users_linked_list.insert_beginning(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "phone": user.phone,
            }
        )

    user = all_users_linked_list.get_user_by_id(user_id)

    # convert the linked list into an array

    return jsonify(user), 200


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # not using the linked list /Query the db directly to delete the user - Filter id = user_id ,
    # filter by the first rec that we find

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
        user_id=ht.get_value("user_id"),
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message": "new blog post created"}), 200


@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_post = BlogPost.query.all()
    random.shuffle(blog_post)

    bst = binary_search_tree.BinarySearchTree()

    for post in blog_post:
        # insert dictionaries as our blog posts
        bst.insert({

            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id": post.user_id,
        })

    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "post not found"})

    return jsonify(post)


# Convert our body to a numeric value
@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_body():
    blog_post = BlogPost.query.all()

    q = customer_queue.Queue()

    for post in blog_post:
        q.enqueue(post)

    return_list = []

    for _ in range(len(blog_post)):
        post = q.dequeue()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.data.body = numeric_body

        return_list.append({
            "id": post.data.id,
            "title": post.data.title,
            "body": post.data.body,
            "user_id": post.data.user_id,
        })

    return jsonify(return_list)


@app.route("/blog_post/delete_last_10", methods=["DELETE"])
def delete_last_10():

    blog_post = BlogPost.query.all()

    s = stack.Stack()

    for post in blog_post:
        s.push(post)

    for _ in range(10):
        post_to_delete = s.pop()
        db.session.delete(post_to_delete.data)
        db.session.commit()

    return jsonify({"message": "success"})


if __name__ == "__main__":
    app.run(debug=True)