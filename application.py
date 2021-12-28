from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from flask_login import LoginManager
import os


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
login_manager = LoginManager()
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL(os.getenv("postgres://ankizvkmkycunc:4d71a6af9f4ab4e333ba720340866f539e58713fec6c8b6552d28db9de9a9912@ec2-3-213-76-170.compute-1.amazonaws.com:5432/ded5npgbq3phdf
"))

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("user_id") is None:
        return redirect("/login")

    if request.method == "POST":
        ID = request.form.get("disn")
        form_name = request.form['form-name']
        if form_name == "form1":
            title = request.form.get("note_title")
            note = request.form.get("the_note")
            h_id = db.execute("SELECT user_id FROM many WHERE note_id =?", ID)
            mate_id = list()
            for i in h_id:
                mate_id.append(i["user_id"])
            mate_id= list(set(mate_id) | set(mate_id))
            return redirect(url_for("edit_note", title=title, ID=ID, note=note, logged=True, innote=True, mate_id=mate_id))
        else:
            db.execute("PRAGMA foreign_keys = ON")
            db.execute("DELETE FROM note WHERE id =?", ID)
            db.execute("DELETE FROM many WHERE note_id =?", ID)
            return redirect("/")

    else:
        all_id = list()
        id_holder = db.execute("SELECT note_id FROM many WHERE user_id = ?", session["user_id"])
        for i in id_holder:
            all_id.append(i["note_id"])
        all_text = db.execute("SELECT content, id, note_name FROM note WHERE id IN(?)", all_id)
        return render_template("index.html", logged=True, innote=False, info=all_text, user_id=session["user_id"])


@app.route("/edit", methods=["GET", "POST"])
def edit_note():
    if session.get("user_id") is None:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title")
        ID = request.form.get("disn")
        note = request.form.get("note")
        db.execute("UPDATE note SET note_name = ?, content = ? WHERE id = ?", title, note, ID)

        join_id = request.form.get("share")
        join_id = join_id.split(",")
        db.execute("DELETE FROM many WHERE note_id =?", ID)
        for x in join_id:
            db.execute("INSERT INTO many(user_id,note_id) VALUES(?,?)", x, ID)
        return redirect("/")
    else:
        title= request.args['title']
        ID = request.args['ID']
        note = request.args['note']
        mate_id = request.args.getlist("mate_id")
        print("dsfafds")
        print(list(request.args['mate_id']))
        return render_template("edit.html", title=title, ID=ID, note=note, logged=True, innote=True,user_id=session["user_id"], lis=mate_id)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session['logged_in'] = True

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", logged=False)

@app.route("/add_note", methods=["GET", "POST"])
def add_note():
    if session.get("user_id") is None:
        return redirect("/login")
    if request.method == "POST":
        sh_id = request.form.get("shared")
        boo = False
        if not sh_id == "":
            share_id = sh_id.split(",")
            boo = True
        title = request.form.get("title")
        note = request.form.get("note")
        db.execute("INSERT INTO note(note_name, user_id, content) VALUES(?,?,?)", title, session["user_id"], note)
        note_id = db.execute("SELECT id FROM note WHERE user_id = ? ORDER BY(id) DESC LIMIT 1", session["user_id"])
        db.execute("INSERT INTO many(user_id,note_id) VALUES(?,?)", session["user_id"], note_id[0]["id"])
        if boo == True:
            for i in share_id:
                db.execute("INSERT INTO many(user_id,note_id) VALUES(?,?)", i, note_id[0]["id"])
        return redirect("/")
    return render_template("add_note.html", logged=True, innote=True, user_id=session["user_id"])


if __name__ == "__main__":
  app.run()

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not name or not confirmation or not password:
            return render_template("error.html", message="missing input")
        if len(password) < 8:
            return render_template("error.html", message="passsword must be atleast 8 characters")
        if not password == confirmation:
            return render_template("error.html", message="passsword and password confirmation are not the same")
        namer = db.execute("SELECT COUNT(username) FROM users where username=?", name)
        if namer[0]['COUNT(username)'] >= 1:
            return render_template("error.html", message="username is already token")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(password))
            return redirect("/login")
    else:
        return render_template("register.html", logged=None)

