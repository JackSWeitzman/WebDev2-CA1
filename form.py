from flask_wtf import FlaskForm
from wtforms import widgets, StringField, IntegerField, SelectField, SelectMultipleField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

class CheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class AfflictionAddForm(FlaskForm):
    bodyPartAdd = SelectField("Choose a body part to add to:",
        choices = ("Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"))
    afflictionAdd = StringField("Enter an affliction here:")
    health = IntegerField("Enter health loss here:")
    submitAdd = SubmitField("Submit")

class AfflictionRemoveForm(FlaskForm):
    bodyPartRemove = SelectField("Choose a body part to remove from:",
        choices = ("Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"))
    afflictionRemove = StringField("Enter an affliction here:")
    submitRemove = SubmitField("Submit")

class AfflictionListForm(FlaskForm):
    bodyPartChoice = SelectField("Choose a list of afflictions:",
        choices = ("Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"),
        validators=[InputRequired()])
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    password2 = PasswordField("Confirm Password:", validators=[InputRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

class AdminAddForm(FlaskForm):
    bodyPartAdd = CheckboxField("Choose which body parts to add to:",
        choices = ("Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"))
    afflictionAdd = StringField("Enter an affliction here:")
    descriptionAdd = StringField("Enter description of affliction here:")
    submitAdd = SubmitField("Submit")

class AdminRemoveForm(FlaskForm):
    bodyPartRemove = CheckboxField("Choose which body parts to remove from:",
        choices = ("Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"))
    afflictionRemove = StringField("Enter an affliction here:")
    submitRemove = SubmitField("Submit")

class AdminCharacterSearchForm(FlaskForm):
    usernameSearch = StringField("Enter the username of the character you want to view:")
    submit = SubmitField("Submit")

class AfflictionRemoveAllForm(FlaskForm):
    removeAllConfirm = StringField("To Confirm Removal Of All Active Afflictions Type: 'DELETE ALL'")
    submit = SubmitField("Remove All Afflictions")

class ChangeDescriptionForm(FlaskForm):
    bodyPart = CheckboxField("Choose which body parts to remove from:",
    choices = ("Whole Body","Head","Neck","Thorax","Stomach","Groin","Left Upper Arm","Right Upper Arm","Left Lower Arm","Right Lower Arm","Left Hand","Right Hand","Left Upper Leg","Right Upper Leg","Left Lower Leg","Right Lower Leg","Left Foot","Right Foot"))
    affliction = StringField("Affliction Name:")
    description = StringField("New Description:")
    submitChange = SubmitField("Submit")

class GiveAdminForm(FlaskForm):
    usernameGive = StringField("Enter the username of the user who you would like to give admin:")
    confirmGive = StringField("To Confirm Giving Admin Type: CONFIRM")
    submitGive = SubmitField("Submit")

class TakeAdminForm(FlaskForm):
    usernameTake = StringField("Enter the username of the user who you would like to take admin from:")
    confirmTake = StringField("To Confirm Giving Admin Type: CONFIRM")
    submitTake = SubmitField("Submit")