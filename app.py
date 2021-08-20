import os

import pytz
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

#  Configure application
app = Flask(__name__)

#  Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#  Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#  Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#  Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mixer.db")

@app.route("/")
@login_required
def index():

    users = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    post = db.execute("SELECT * FROM post ORDER BY date DESC, time DESC LIMIT 20")
    Myreact = db.execute("SELECT * from react WHERE user_id = ?",session["user_id"])
    react_id = []
    likeCount = 0


    for Myreacts in Myreact:
        if Myreacts["post_id"] not in react_id:
            react_id.append(Myreacts["post_id"])


    return render_template("index.html", user=users, post=post, react_id=react_id,)

@app.route("/login", methods=["GET", "POST"])
def login():

    #  Forget any user_id
    session.clear()

    #  User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        error = ""
        #  Ensure username was submitted
        if not request.form.get("username"):
            error = "Must provide username"
            return render_template("login.html", errors=error)

        #  Ensure password was submitted
        elif not request.form.get("password"):
            error= "Must provide password"
            return render_template("login.html", errors=error)

        #  Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        username = request.form.get("username")

        #  Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            error = "Invalid username and/or password"
            return render_template("login.html", errors=error)

        #  Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        #  Redirect user to home page
        flash("You were successfully logged in")
        return redirect("/")

    #  User reached route via GET (as by clicking a link or via redirect)
    else:
        noError = ""
        return render_template("login.html", errors=noError)

# Log Out Route
@app.route("/logout")
def logout():
    """Log user out"""

    #  Forget any user_id
    session.clear()

    #  Redirect user to login form
    return redirect("/")

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():

    # Check if the user submit the form with the method of POST
    if request.method == "POST":

        # Setting the variable to user's input
        firstname = (str(request.form.get("firstname")))
        lastname = (str(request.form.get("lastname")))
        username = (str(request.form.get("username")))
        password = (str(request.form.get("password")))
        confirmation = (str(request.form.get("confirmation")))
        full_name = firstname + " " + lastname

        GENDERS = ["Male", "male", "M", "m", "Female", "female", "F", "f"]
        gender = (str(request.form.get("genders")))
        profile = 0


        # Checking Errors
        if confirmation != password:
            flash("Password didn't match")
            return redirect("/register")

        check = db.execute("SELECT * FROM users WHERE username = ?", username)

        if not firstname or not lastname:
            flash("Input Firstname or Lastname")
            return redirect("/register")

        if len(check) > 0:
            flash("Username already exist")
            return redirect("/register")

        if not username or not password:
           flash("Input username/password")
           return redirect("/register")

        if len(username) < 8:
            flash("Username must have atleast 8 character")
            return redirect("/register")

        if len(password) < 8:
            flash("Password must have atleast 8 character")
            return redirect("/register")

        if len(password) > 20:
            flash("Password should be not be greater than 20")
            return redirect("/register")

        if not any(char.isdigit() for char in password):
            flash('Password should have at least one numeral')
            return redirect("/register")

        if not any(char.islower() for char in password):
            flash('Password should have at least one lowercase letter')
            return redirect("/register")

        if not any(char.isupper() for char in password):
            flash('Password should have at least one uppercase letter')
            return redirect("/register")

        if password == username:
            flash("Password and Username must be different")
            return redirect("/register")

        if gender not in GENDERS:
            flash("Gender is invalid")
            return redirect("/register")

        if not gender:
            flash("Input Gender")
            return redirect("/register")

        if gender == "Male" or gender == "male" or gender == "M" or gender == "m":
            profile = 1

        if gender == "Female" or gender == "female" or gender == "F" or gender == "f":
            profile = 2



        # Hashing the password to protect it from intruders
        hpass = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Inserting a new row for the user
        db.execute("INSERT INTO users (username, password, firstname, lastname, gender, profile, full_name) VALUES (?, ?, ?, ?, ?, ?, ?)", username, hpass, firstname, lastname, gender, profile, full_name)
        rows = db.execute("SELECT * FROM users WHERE username=?", username)

        # Setting the session to the id of the user
        session["user_id"] = rows[0]["id"]

        # Flashing message and redirecting to index
        flash("You were sucessfully registered")
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/mix", methods=["GET", "POST"])
@login_required
def mix():

    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    if request.method == "POST":

        name = users[0]["firstName"] + " " + users[0]["lastName"]

        now = datetime.now(tz=pytz.UTC)
        Manila = now.astimezone(pytz.timezone('Asia/Manila'))

        date = Manila.strftime("%x")
        time = Manila.strftime("%X")
        profile = users[0]["profile"]
        content = (str(request.form.get("content")))
        action = "Post"


        if not content:
            flash("Put some text in post section")
            return redirect("/mix")

        db.execute("INSERT INTO post(user_id, name, content, time, date, profile, action) VALUES (?, ?, ?, ?, ?, ?, ?)", session["user_id"], name, content, time, date, profile, action)
        return redirect("/")

    else:
        return render_template("mix.html", user= users)

@app.route("/profile")
@login_required
def profile():

    users = db.execute("SELECT * from users WHERE id = ?", session["user_id"])

    post = db.execute("SELECT * FROM post WHERE user_id=? ORDER BY date DESC, time DESC", session["user_id"])
    hpostCount = db.execute("SELECT COUNT(*) FROM post WHERE user_id=? ORDER BY date DESC, time DESC", session["user_id"])
    postCount = (int(hpostCount[0]["COUNT(*)"]))

    following = db.execute("SELECT * from follower WHERE user_id = ?",session["user_id"])
    hfollowingCount = db.execute("SELECT COUNT(*) from follower WHERE user_id = ?",session["user_id"])
    followingCount = (int(hfollowingCount[0]["COUNT(*)"]))

    followers = db.execute("SELECT * from follower WHERE follower_id = ?",session["user_id"])
    hfollowersCount = db.execute("SELECT COUNT(*) from follower WHERE follower_id = ?",session["user_id"])
    followersCount = (int(hfollowersCount[0]["COUNT(*)"]))

    Myreact = db.execute("SELECT * from react WHERE user_id = ?",session["user_id"])
    react_id = []
    likeCount = 0


    for Myreacts in Myreact:
        if Myreacts["post_id"] not in react_id:
            react_id.append(Myreacts["post_id"])



    return render_template("profile.html", user=users, post=post, postCount=postCount,
                            following=following, followingCount=followingCount,
                            followers=followers, followersCount=followersCount, react_id=react_id)


@app.route("/friends_profile/<int:id>")
@login_required
def friends_profile(id):


    if id == session["user_id"]:
        return redirect("/profile")

    users = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    Myfollowing = db.execute("SELECT * from follower WHERE user_id = ?",session["user_id"])
    user_following = []

    for Myfollowings in Myfollowing:
        if Myfollowings["follower_id"] not in user_following:
            user_following.append(Myfollowings["follower_id"])

    friends = db.execute("SELECT * from users WHERE id = ?",id)

    post = db.execute("SELECT * FROM post WHERE user_id=? ORDER BY date DESC, time DESC", id)
    hpostCount = db.execute("SELECT COUNT(*) FROM post WHERE user_id=? ORDER BY date DESC, time DESC", id)
    postCount = (int(hpostCount[0]["COUNT(*)"]))

    following = db.execute("SELECT * from follower WHERE user_id = ?",id)
    hfollowingCount = db.execute("SELECT COUNT(*) from follower WHERE user_id = ?",id)
    followingCount = (int(hfollowingCount[0]["COUNT(*)"]))

    followers = db.execute("SELECT * from follower WHERE follower_id = ?",id)
    hfollowersCount = db.execute("SELECT COUNT(*) from follower WHERE follower_id = ?",id)
    followersCount = (int(hfollowersCount[0]["COUNT(*)"]))

    Myreact = db.execute("SELECT * from react WHERE user_id = ?",session["user_id"])
    react_id = []
    likeCount = 0


    for Myreacts in Myreact:
        if Myreacts["post_id"] not in react_id:
            react_id.append(Myreacts["post_id"])

    return render_template("friends_profile.html", user=users, friends=friends, post=post,
                            postCount=postCount, following=following, followingCount=followingCount,
                            followers=followers, followersCount=followersCount, user_following=user_following,
                            react_id=react_id)


@app.route("/delete/<int:id>")
@login_required
def delete(id):

    db.execute("DELETE FROM post WHERE id=?",id)
    db.execute("DELETE FROM comment WHERE post_id=?",id)
    db.execute("DELETE FROM react WHERE post_id=?",id)
    flash("Successfully Deleted")
    return redirect("/profile")


@app.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit(id):

    users = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    post = db.execute("SELECT * FROM post WHERE id=? ORDER BY date DESC, time DESC", id)

    if request.method == "POST":

        content = (str(request.form.get("content")))
        action = "Edited"
        now = datetime.now(tz=pytz.UTC)
        Manila = now.astimezone(pytz.timezone('Asia/Manila'))

        date = Manila.strftime("%x")
        time = Manila.strftime("%X")

        db.execute("UPDATE post SET content = ?, time = ?, date = ?, action = ? WHERE id = ?", content,time,date,action,id)
        flash("Successfully Edited")
        return redirect("/profile")
    else:
        return render_template("edit.html", user=users, post=post, id=id)

@app.route("/follow/<int:id>")
@login_required
def follow(id):
    user = db.execute("SELECT * FROM users WHERE id = ?",session["user_id"])
    follower = db.execute("SELECT * FROM users WHERE id = ?",id)

    user_name = user[0]["firstName"] + " " + user[0]["lastName"]
    follower_name = follower[0]["firstName"] + " " + follower[0]["lastName"]
    follower_profile = follower[0]["profile"]
    user_profile = user[0]["profile"]

    db.execute("INSERT INTO follower (user_id ,follower_id, user_name, follower_name, follower_profile, user_profile) VALUES (?, ?, ?, ?, ?, ?)",
    session["user_id"], id, user_name, follower_name, follower_profile, user_profile)


    return redirect(url_for('friends_profile', id=id))

@app.route("/unfollow/<int:id>")
@login_required
def unfollow(id):
    db.execute("DELETE FROM follower WHERE user_id = ? AND follower_id = ?",session["user_id"], id)

    return redirect(url_for('friends_profile', id=id))


@app.route("/comment/<int:id>", methods=["GET","POST"])
@login_required
def comment(id):

    users = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    post = db.execute("SELECT * FROM post WHERE id=?",id)
    Myreact = db.execute("SELECT * from react WHERE user_id = ?",session["user_id"])
    react_id = []
    likeCount = 0
    comment = db.execute("SELECT * FROM comment WHERE post_id = ? ORDER BY date DESC, time DESC", id)


    for Myreacts in Myreact:
        if Myreacts["post_id"] not in react_id:
            react_id.append(Myreacts["post_id"])


    if request.method == "POST":
        userComment = (str(request.form.get("comment")))
        now = datetime.now(tz=pytz.UTC)
        Manila = now.astimezone(pytz.timezone('Asia/Manila'))

        date = Manila.strftime("%x")
        time = Manila.strftime("%X")
        profile = users[0]["profile"]
        name = users[0]["firstName"] + " " + users[0]["lastName"]
        comment_count = post[0]["comment_count"]
        totalcomment = comment_count + 1


        db.execute("INSERT INTO comment (user_id, comment, date, time, post_id, profile_id, name) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    session["user_id"], userComment, date, time, id, profile, name)

        db.execute("UPDATE post SET comment_count = ? WHERE id = ?",totalcomment, id)

        comments = db.execute("SELECT * FROM comment WHERE post_id = ? ORDER BY date DESC, time DESC", id)
        return redirect(url_for('comment', id=id))
    else:
        return render_template("comment.html",user=users, post=post, react_id=react_id, comment=comment)



@app.route("/like/<int:id>")
@login_required
def like(id):

    db.execute("INSERT INTO react (user_id ,post_id) VALUES (?, ?)",session["user_id"], id)

    hreact_count = db.execute("SELECT * FROM post WHERE id = ?", id)

    reacts_count = (int(hreact_count[0]["react_count"]))
    total_react = reacts_count + 1

    db.execute("UPDATE post SET react_count = ? WHERE id = ?",total_react, id)

    if request.args.get("react") == "index":
        return redirect("/")

    if request.args.get("profile") == "profile":
        return redirect("/profile")

    if request.args.get("friends"):
        friends_id = (int(request.args.get("friends")))
        return redirect(url_for('friends_profile', id=friends_id))

    if request.args.get("following") == "followings":
        return redirect("/following")

    if request.args.get("commentName"):
        post_id = (int(request.args.get("commentName")))
        return redirect(url_for('comment', id=post_id))

    return redirect("/")

@app.route("/unliked/<int:id>")
@login_required
def unliked(id):
    db.execute("DELETE FROM react WHERE user_id = ? AND post_id = ?",session["user_id"], id)

    hreact_count = db.execute("SELECT * FROM post WHERE id = ?", id)

    reacts_count = (int(hreact_count[0]["react_count"]))
    total_react = reacts_count - 1

    db.execute("UPDATE post SET react_count = ? WHERE id = ?",total_react, id)

    if request.args.get("react") == "index":
        return redirect("/")

    if request.args.get("profile") == "profile":
        return redirect("/profile")

    if request.args.get("friends"):
        friends_id = (int(request.args.get("friends")))
        return redirect(url_for('friends_profile', id=friends_id))

    if request.args.get("following") == "followings":
        return redirect("/following")

    if request.args.get("commentName"):
        post_id = (int(request.args.get("commentName")))
        return redirect(url_for('comment', id=post_id))


    return redirect("/")


@app.route("/following")
@login_required
def friends():
    users = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    followingPost = db.execute("SELECT follower_id FROM follower WHERE user_id =?",session["user_id"])

    following = []

    for followingPosts in followingPost:
        if followingPosts["follower_id"] not in following:
            following.append(followingPosts["follower_id"])

    post = []
    for followings in following:
        hpost = db.execute("SELECT * FROM post WHERE user_id=? ORDER BY date DESC, time DESC LIMIT 20",followings)
        post.append(hpost)
    Myreact = db.execute("SELECT * from react WHERE user_id = ?",session["user_id"])

    react_id = []
    for Myreacts in Myreact:
        if Myreacts["post_id"] not in react_id:
            react_id.append(Myreacts["post_id"])

    size = {}
    totalPost = 0
    sizeFollowing = len(post)

    for index in range(sizeFollowing):
        for sizepost in range(len(post[index])):
            size[totalPost] = (post[index][sizepost])
            totalPost += 1

    return render_template("following.html", user=users, size=size, totalPost=totalPost, react_id=react_id)

@app.route("/userfollower/<int:id>")
@login_required
def userfollower(id):

    follower = db.execute("SELECT * FROM follower WHERE user_id=?", id)
    user = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    return render_template("userfollower.html", user=user, follower=follower)


@app.route("/userfollowing/<int:id>")
@login_required
def userfollowing(id):

    follower = db.execute("SELECT * FROM follower WHERE follower_id=?", id)
    user = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    return render_template("userfollowing.html", user=user, follower=follower)


@app.route("/search", methods=["POST"])
@login_required
def search():

    searchName = request.form.get("search")
    searchName2 = "%"+ searchName +"%"
    user = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    searched = db.execute("SELECT * FROM users WHERE full_name LIKE ? ORDER BY full_name ASC", searchName2)
    print(searched)

    return render_template("search.html", user=user, searched=searched, searchName=searchName)



@app.route("/account", methods=["GET"])
@login_required
def account():

    user = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    return render_template("account.html", user=user)

@app.route("/edit_account/password", methods=["GET","POST"])
@login_required
def edit_account_password():

    user = db.execute("SELECT * from users WHERE id = ?", session["user_id"])
    if request.method == "POST":

        username = user[0]["username"]
        password = (str(request.form.get("oldpassword")))
        newpassword = (str(request.form.get("newpassword")))
        confirmation = (str(request.form.get("confirmation")))



        if not password or not newpassword or not confirmation:
            flash("Invalid Input")
            return redirect("/")

        if not check_password_hash(user[0]["password"], password):
            flash("Wrong Password")
            return redirect("/")

        if newpassword != confirmation:
            flash("New Password didn't match")
            return redirect("/")

        if len(newpassword) < 8:
            flash("Password must have atleast 8 character")
            return redirect("/")

        if len(newpassword) > 20:
            flash("Password should be not be greater than 20")
            return redirect("/")

        if not any(char.isdigit() for char in newpassword):
            flash('Password should have at least one numeral')
            return redirect("/")

        if not any(char.islower() for char in newpassword):
            flash('Password should have at least one lowercase letter')
            return redirect("/")

        if not any(char.isupper() for char in newpassword):
            flash('Password should have at least one uppercase letter')
            return redirect("/")

        if newpassword == username:
            flash("Password and Username must be different")
            return redirect("/")

        hpass = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=8)

        db.execute("UPDATE users SET password = ? WHERE id = ?",hpass, session["user_id"])
        flash("Password successfully changed")
        return redirect("/account")
    else:
        return render_template("edit_account_password.html", user=user)

@app.route("/edit_account/name", methods=["GET","POST"])
@login_required
def edit_account_name():

    user = db.execute("SELECT * from users WHERE id = ?", session["user_id"])

    if request.method == "POST":
        firstname = (str(request.form.get("firstname")))
        lastname = (str(request.form.get("lastname")))

        password = (str(request.form.get("password")))
        full_name = firstname + " " + lastname

        if not firstname or not lastname or not password:
            flash("Invalid Input")
            return redirect("/")

        if not check_password_hash(user[0]["password"], password):
            flash("Wrong Password")
            return redirect("/")

        if any(char.isdigit() for char in firstname) or any(char.isdigit() for char in lastname):
            flash("Name should not contain numbers")
            return redirect("/")

        db.execute("UPDATE users SET firstname = ?, lastname = ?, full_name = ? WHERE id = ?",firstname, lastname, full_name, session["user_id"])
        db.execute("UPDATE post SET name = ? WHERE user_id = ?",full_name, session["user_id"])
        db.execute("UPDATE comment SET name = ? WHERE user_id = ?",full_name, session["user_id"])
        db.execute("UPDATE follower SET user_name = ? WHERE user_id = ?",full_name, session["user_id"])

        flash("Name successfully changed")
        return redirect("/account")
    else:
        return render_template("edit_account_name.html", user=user)


if __name__ == "__main__":
    app.run()