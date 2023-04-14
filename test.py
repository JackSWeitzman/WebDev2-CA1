from flask import Flask, render_template, session, redirect, url_for, g, request
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from form import AfflictionAddForm, AfflictionRemoveForm, AfflictionListForm, LoginForm, RegistrationForm, AdminAddForm, AdminRemoveForm, AdminCharacterSearchForm, AfflictionRemoveAll, ChangeDescription
from functools import wraps


db = get_db()
# DELETES FROM MENU
a = form.nameOfFood.data
db.execute("""DELETE FROM afflictions WHERE nameOfFood= ?""", (a))
db.commit()

# INSERTS INTO MENU
x = form.nameOfFood.data
y = form.calories.data
z = form.allergies.data
db.execute("""INSERT INTO afflictions (body_part, affliction, debuff) VALUES (?, ?, ?)""", (x,y,z))
db.commit()


def removeFromTable(meal_id):
    db.execute("""DELETE FROM afflictions WHERE nameOfFood= ?""", (meal_id))
    db.commit()

