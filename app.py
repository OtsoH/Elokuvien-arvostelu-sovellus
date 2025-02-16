import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items = all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user = user, items = items)


@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    return render_template("show_item.html", item = item, classes = classes)
    
@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    if len("title") > 50:
        abort(403)
    description = request.form["description"]
    if len(description) > 2000:
        abort(403)
    user_id = session["user_id"]

    classes = []
    category = request.form["category"]
    if category:
        classes.append(("Kategoria", category))
    stars = request.form["stars"]
    if stars:
        classes.append(("Tähtiä", stars))
    items.add_item(title, description, user_id, classes)
    return redirect("/")

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id = request.form["item_id"]
    item =items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    title = request.form["title"]
    description = request.form["description"]
    items.update_item(item_id, title, description)
    return redirect("/item/" + str(item_id))

@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        return render_template("delete_item.html", item=item)
    
    if request.method == "POST":
        if "delete" in request.form:
            items.delete_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
        
@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")
