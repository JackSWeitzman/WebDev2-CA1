# ADMIN ACCOUNT:
# username = admin
# password = admin
# A breakdown of content on each page can be on the home page
# Some pages have content that you need to scroll down for (it might not be obvious it is there).
# To add an affliction in the controller page you need to include the name of the affliction including the brackets and what is within the brackets.
# A list of all afflictions can be found on the List page

from flask import Flask, render_template, session, redirect, url_for, g, request
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from form import AfflictionAddForm, AfflictionRemoveForm, AfflictionListForm, LoginForm, RegistrationForm, AdminAddForm, AdminRemoveForm, AdminCharacterSearchForm, AfflictionRemoveAllForm, ChangeDescriptionForm, GiveAdminForm, TakeAdminForm
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "1"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def logged_in_user():
    g.user = session.get("username", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
def index():
    if session.get("admin", None) == 1:
        nav = 1
    elif session.get("username", None) is not None:
        nav = 2
    else:
        nav = 3
    g.user = session.get("username", None)
    if g.user is None:
        username = "Sign In"
    else:
        username = session["username"]
    return render_template("index.html", username = username, nav=nav)

@app.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if session.get("admin", None) == 1:
        nav = 1
    elif session.get("username", None) is not None:
        nav = 2
    else:
        nav = 3
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        clashing_user = db.execute("""SELECT * FROM users WHERE username = ?;""", ([username])).fetchone()
        if clashing_user is None:
            form.username.errors.append("Username does not exist!")
        elif not check_password_hash(clashing_user["password"], password):
            form.password.errors.append("Incorrect password!")
        else:
            session.clear()
            session["username"] = username
            adminBit = db.execute("""SELECT * FROM users WHERE username = ?;""", ([username])).fetchone()
            session["admin"] = adminBit["admin"]
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("controller")
            return redirect(next_page)
    return render_template("login.html", form=form, nav=nav)
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/register", methods=["POST","GET"])
def register():
    form = RegistrationForm()
    if session.get("admin", None) == 1:
        nav = 1
    elif session.get("username", None) is not None:
        nav = 2
    else:
        nav = 3
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        db = get_db()
        if len(username) > 16:
            form.username.errors.append("Username is too long")
            return render_template("register.html", form=form, nav=nav)
        clashing_user = db.execute("""SELECT * FROM users WHERE username = ?;""", ([username])).fetchone()
        if clashing_user is not None:
            form.username.errors.append("Username is already in use")
        else:
            bodyHealth = {"Whole Body":440,"Head":20,"Neck":15,"Thorax":85,"Stomach":50,"Groin":20,"Left Upper Arm":30,"Right Upper Arm":30,"Left Lower Arm":20,"Right Lower Arm":20,"Left Hand":10,"Right Hand":10,"Left Upper Leg":30,"Right Upper Leg":30,"Left Lower Leg":20,"Right Lower Leg":20,"Left Foot":15,"Right Foot":15}
            db.execute("""INSERT INTO users (username, password, admin) VALUES (?, ?, 0);""", (username, generate_password_hash(password)))
            db.commit()
            for item in bodyHealth:
                db.execute("""INSERT INTO body_part_health (username, body_part, body_part_health_total, body_part_health_active) VALUES (?, ?, ?, ?);""", (username, item, bodyHealth[item], bodyHealth[item]))
                db.commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=form, nav=nav)

@app.route("/a-controller", methods=["GET","POST"])
@login_required
def adminController():
    username = session["username"]
    if session["admin"] != 1:
        return redirect(url_for("index"))
    form = AdminAddForm()
    form2 = AdminRemoveForm()
    form3 = AdminCharacterSearchForm()
    form4 = ChangeDescriptionForm()
    form5 = GiveAdminForm()
    form6 = TakeAdminForm()
    if session.get("admin", None) == 1:
        nav = 1
    elif session.get("username", None) is not None:
        nav = 2
    else:
        nav = 3
    if form.validate_on_submit() and form.submitAdd.data:
        if not form.bodyPartAdd.data or not form.afflictionAdd.data or not form.descriptionAdd.data:
            form.afflictionAdd.errors.append("You did not fill out all fields")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        db = get_db()
        selectedPart = form.bodyPartAdd.data
        afflictionAdd = form.afflictionAdd.data
        descriptionAdd = form.descriptionAdd.data
        for item in selectedPart:
            in_db = db.execute("""SELECT * FROM afflictions WHERE affliction = ? AND body_part = ?""",(afflictionAdd, item,)).fetchone()
            if in_db is not None:
                form.afflictionAdd.errors.append("This affliction already exists on: " + str(item))
            else:
                db.execute("""INSERT INTO afflictions (body_part, affliction, debuff) VALUES (?, ?, ?)""", (item, afflictionAdd, descriptionAdd))
                db.commit()
                form.afflictionAdd.errors.append("Affliction added to: " + str(item))
        return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
    if form2.validate_on_submit() and form2.submitRemove.data:
        if not form2.bodyPartRemove.data or not form2.afflictionRemove.data:
            form2.afflictionRemove.errors.append("You did fill out all fields")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        db = get_db()
        selectedPart = form2.bodyPartRemove.data
        afflictionRemove = form2.afflictionRemove.data
        for item in selectedPart:
            in_db = db.execute("""SELECT * FROM afflictions WHERE affliction = ? AND body_part = ?;""",(afflictionRemove, item,)).fetchone()
            if in_db is None:
                form2.afflictionRemove.errors.append("This affliction does not exist on:" + str(item))
            else:
                db.execute("""DELETE FROM afflictions WHERE body_part = ? AND affliction = ?;""",(item, afflictionRemove,))
                db.commit()
                form2.afflictionRemove.errors.append("Affliction removed from: " + str(item))
        return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
    if form3.validate_on_submit() and form3.submit.data:
        username = session["username"]
        if not form3.usernameSearch.data:
            form3.usernameSearch.errors.append("You did not enter a username")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        db = get_db()
        selectedUser = form3.usernameSearch.data
        orderedDict = []
        bodyParts = ["Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"]
        activeAffliction = (db.execute("""SELECT * FROM active WHERE username = ?;""", (selectedUser,)).fetchall())
        activeHealth = (db.execute("""SELECT * FROM body_part_health WHERE username = ?;""", (selectedUser,)).fetchall())
        for item in bodyParts:
            emptyDict = {}
            emptyDict2 = {}
            for i in activeAffliction:
                if i["body_part"] == item:
                    holder = i["affliction"]
                    holder2 = i["health"]
                    emptyDict[holder] = holder2
            sortedDict = dict(sorted(emptyDict.items(), key=lambda x: x[0].lower()))
            holder = item
            emptyDict2[holder] = sortedDict
            orderedDict.append(emptyDict2)
        return render_template("affliction_active.html", healthList = activeHealth, list2=activeAffliction, part=bodyParts, orderedDict = orderedDict, username = username, nav=nav)
    if form4.validate_on_submit() and form4.submitChange.data:
        if not form4.affliction.data or not form4.description.data or not form4.bodyPart.data:
            form4.affliction.errors.append("You did not fill all the fields")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        db = get_db()
        affliction = form4.affliction.data
        description = form4.description.data
        selectedPart = form4.bodyPart.data
        for item in selectedPart:
            in_db = db.execute("""SELECT * FROM afflictions WHERE affliction = ? AND body_part = ?;""",(affliction, item,)).fetchone()
            if not in_db:
                form4.affliction.errors.append("This affliction does not exist on: " + str(item))
            else:
                db.execute("""UPDATE afflictions SET debuff = ? WHERE affliction = ? AND body_part = ?;""",(description, affliction, item,))
                db.commit()
                form4.affliction.errors.append("Description of " + str(affliction) + " changed on " + str(item))
        return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
    if form5.validate_on_submit() and form5.submitGive.data:
        if not form5.confirmGive.data and not form5.usernameGive.data:
            form5.usernameGive.errors.append("You did not fill all the fields")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        elif form5.confirmGive.data != "CONFIRM":
            form5.usernameGive.errors.append("Confirmation Message Typed Incorrectly")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        else:
            db = get_db()
            if session["username"] == form5.usernameGive.data:
                form5.usernameGive.errors.append("You can't select yourself")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
            in_db = db.execute("""SELECT * FROM users WHERE username = ?;""",(form5.usernameGive.data,)).fetchone()
            if not in_db:
                form5.usernameGive.errors.append("User Does Not Exist")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
            elif in_db["admin"] == 1:
                form5.usernameGive.errors.append("User Is Already An Admin")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)           
            else:
                db.execute("""UPDATE users SET admin = 1 WHERE username = ?;""",(form5.usernameGive.data,))
                db.commit()
                form5.usernameGive.errors.append("User is now an admin!")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
    if form6.validate_on_submit() and form6.submitTake.data:
        if not form6.confirmTake.data and not form6.usernameTake.data:
            form6.usernameTake.errors.append("You did not fill all the fields")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        elif form6.confirmTake.data != "CONFIRM":
            form6.usernameTake.errors.append("Confirmation Message Typed Incorrectly")
            return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
        else:
            db = get_db()
            if session["username"] == form6.usernameTake.data:
                form6.usernameTake.errors.append("You can't select yourself")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
            in_db = db.execute("""SELECT * FROM users WHERE username = ?;""",(form6.usernameTake.data,)).fetchone()
            if not in_db:
                form6.usernameTake.errors.append("User Does Not Exist")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
            elif in_db["admin"] == 0:
                form6.usernameTake.errors.append("User Is Not An Admin")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)           
            else:
                db.execute("""UPDATE users SET admin = 0 WHERE username = ?;""",(form6.usernameTake.data,))
                db.commit()
                form6.usernameTake.errors.append("User is no longer an admin!")
                return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)
    return render_template("admin_controller.html", form=form, form2=form2, form3=form3, form4=form4, form5=form5, form6=form6, username = username, nav=nav)

@app.route("/controller", methods=["GET","POST"])
@login_required
def controller():
    username = session["username"]
    form = AfflictionAddForm()
    form2 = AfflictionRemoveForm()
    form3 = AfflictionRemoveAllForm()
    if session.get("admin", None) == 1:
        nav = 1
    elif session.get("username", None) is not None:
        nav = 2
    else:
        nav = 3
    if form.validate_on_submit() and form.submitAdd.data:
        if not form.bodyPartAdd.data or not form.afflictionAdd.data:
            form.afflictionAdd.errors.append("You did not fill all the fields")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
        db = get_db()
        selectedPart = form.bodyPartAdd.data
        addedAffliction = form.afflictionAdd.data
        in_db = db.execute("""SELECT affliction FROM afflictions WHERE affliction = ? AND body_part = ?;""", (addedAffliction, selectedPart,)).fetchone()
        if in_db is None:
            form.afflictionAdd.errors.append("That affliction is not in the database")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
        in_db = db.execute("""SELECT affliction FROM active WHERE affliction = ? AND body_part = ? AND username = ?;""", (addedAffliction, selectedPart, session["username"],)).fetchone()
        if in_db is not None:
            form.afflictionAdd.errors.append("That affliction is already active")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
        else:
            health = abs(form.health.data)
            if selectedPart == "Whole Body":
                health = 0
            db.execute("""INSERT INTO active (username, body_part, affliction, health) VALUES (?, ?, ?, ?)""", (session["username"], selectedPart, addedAffliction, health))
            selectedPartHealth = db.execute("""SELECT * FROM body_part_health WHERE username = ? AND body_part = ?;""", (session["username"], selectedPart,)).fetchone()
            newHealth = selectedPartHealth["body_part_health_active"] - health
            if newHealth < 0:
                newHealth = 0
            db.execute("""UPDATE body_part_health SET body_part_health_active = ? WHERE username = ? AND body_part = ?;""", (newHealth, session["username"], selectedPart))
            wholeBodyHealth = db.execute("""SELECT * FROM body_part_health WHERE username = ? AND body_part = "Whole Body";""", (session["username"],)).fetchone()
            newHealth = wholeBodyHealth["body_part_health_active"] - health
            if newHealth < 0:
                newHealth = 0
            db.execute("""UPDATE body_part_health SET body_part_health_active = ? WHERE username = ? AND body_part = "Whole Body";""", (newHealth, session["username"],))
            db.commit()
            form.afflictionAdd.errors.append("Added Affliction!")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
    if form2.validate_on_submit() and form2.submitRemove.data:
        if not form2.bodyPartRemove.data or not form2.afflictionRemove.data:
            form2.afflictionRemove.errors.append("You did not fill all the fields")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
        db = get_db()
        selectedPart = form2.bodyPartRemove.data
        removedAffliction = form2.afflictionRemove.data
        in_db = db.execute("""SELECT affliction FROM afflictions WHERE affliction = ? AND body_part = ?;""", (removedAffliction, selectedPart,)).fetchone()
        if in_db is None:
            form2.afflictionRemove.errors.append("That affliction is not in the database")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
        in_db = db.execute("""SELECT affliction FROM active WHERE affliction = ? AND body_part = ? AND username = ?;""", (removedAffliction, selectedPart, session["username"],)).fetchone()
        if in_db is None:
            form2.afflictionRemove.errors.append("That affliction is not currently active")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
        else:
            afflictionHealth = db.execute("""SELECT * FROM active WHERE username = ? AND body_part = ? AND affliction = ?;""", (session["username"], selectedPart, removedAffliction)).fetchone()
            selectedPartHealth = db.execute("""SELECT * FROM body_part_health WHERE username = ? AND body_part = ?;""", (session["username"], selectedPart)).fetchone()
            newHealth = afflictionHealth["health"] + selectedPartHealth["body_part_health_active"]
            if newHealth > selectedPartHealth["body_part_health_total"]:
                newHealth = selectedPartHealth["body_part_health_total"]
            db.execute("""UPDATE body_part_health SET body_part_health_active = ? WHERE username = ? AND body_part = ?;""", (newHealth, session["username"], selectedPart))
            wholeBodyHealth = db.execute("""SELECT * FROM body_part_health WHERE username = ? AND body_part = "Whole Body";""", (session["username"],)).fetchone()
            newHealth = afflictionHealth["health"] + wholeBodyHealth["body_part_health_active"]
            if newHealth > wholeBodyHealth["body_part_health_total"]:
                newHealth = wholeBodyHealth["body_part_health_total"]
            db.execute("""UPDATE body_part_health SET body_part_health_active = ? WHERE username = ? AND body_part = "Whole Body";""", (newHealth, session["username"],))
            db.execute("""DELETE FROM active WHERE username = ? AND body_part = ? AND affliction = ?""", (session["username"], selectedPart, removedAffliction))
            db.commit()
            form2.afflictionRemove.errors.append("Removed Affliction!")
            return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)
    if form3.validate_on_submit() and form3.submit.data:
        if form3.removeAllConfirm.data == "DELETE ALL":
            db = get_db()
            db.execute("""DELETE FROM active WHERE username = ?""", (session["username"],))
            db.execute("""UPDATE body_part_health SET body_part_health_active = body_part_health_total WHERE username = ?""", (session["username"],))
            db.commit()
            form3.removeAllConfirm.errors.append("Removed All Active Afflictions")
        else:
            form3.removeAllConfirm.errors.append("Confirmation Message Typed Incorrectly")
    return render_template("affliction_controller.html", form=form, form2=form2, form3=form3, username = username, nav=nav)

@app.route("/list", methods=["POST","GET"])
def list():
    if session.get("admin", None) == 1:
        nav = 1
    elif session.get("username", None) is not None:
        nav = 2
    else:
        nav = 3
    g.user = session.get("username", None)
    if g.user is None:
        username = "Sign In"
    else:
        username = session["username"]
    form = AfflictionListForm()
    showAfflictions = False
    if form.validate_on_submit():
        db = get_db()
        showAfflictions = True
        selectedPart = form.bodyPartChoice.data
        listOfAfflictions = db.execute("""SELECT * FROM afflictions WHERE body_part = ?;""", (selectedPart,)).fetchall()
        emptyDict = {}
        for i in listOfAfflictions:
            holder = i["affliction"]
            holder2 = i["debuff"]
            emptyDict[holder] = holder2
        sortedDict = dict(sorted(emptyDict.items(), key=lambda x: x[0].lower()))
        return render_template("affliction_list.html", form=form, sortedDict = sortedDict, showAfflictions = showAfflictions, selectedPart = selectedPart, username = username, nav=nav)
    return render_template("affliction_list.html", form=form, username = username, nav=nav)

@app.route("/active")
@login_required
def active():
    if session.get("admin", None) == 1:
        nav = 1
    elif session.get("username", None) is not None:
        nav = 2
    else:
        nav = 3
    username = session["username"]
    db = get_db()
    orderedDict = []
    bodyParts = ["Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"]
    activeAffliction = (db.execute("""SELECT * FROM active WHERE username = ?;""", (session["username"],)).fetchall())
    activeHealth = (db.execute("""SELECT * FROM body_part_health WHERE username = ?;""", (session["username"],)).fetchall())
    for item in bodyParts:
        emptyDict = {}
        emptyDict2 = {}
        for i in activeAffliction:
            if i["body_part"] == item:
                holder = i["affliction"]
                holder2 = i["health"]
                emptyDict[holder] = holder2
        sortedDict = dict(sorted(emptyDict.items(), key=lambda x: x[0].lower()))
        holder = item
        emptyDict2[holder] = sortedDict
        orderedDict.append(emptyDict2)
    return render_template("affliction_active.html", healthList = activeHealth, list2=activeAffliction, part=bodyParts, orderedDict = orderedDict, username = username, nav=nav)
