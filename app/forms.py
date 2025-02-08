from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):  # ✅ Added this class
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class MeasurementForm(FlaskForm):
    chest = FloatField('Chest (in inches)', validators=[DataRequired()])
    waist = FloatField('Waist (in inches)', validators=[DataRequired()])
    inseam = FloatField('Inseam (in inches)', validators=[DataRequired()])
    head = FloatField('Head (in inches)', validators=[DataRequired()])
    neck_circumference = FloatField('Neck Circumference (in inches)', validators=[DataRequired()])
    shoulder_width = FloatField('Shoulder Width (in inches)', validators=[DataRequired()])
    sleeve_length = FloatField('Sleeve Length (in inches)', validators=[DataRequired()])
    buba_length = FloatField('Buba Length (in inches)', validators=[DataRequired()])
    submit = SubmitField('Save Measurements')



class RequestResetForm(FlaskForm):
    email = StringField('Enter your email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UserEditForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password')
    submit = SubmitField('Update User')

    def __init__(self, obj=None, **kwargs):
        super(UserEditForm, self).__init__(**kwargs)
        self.obj = obj

    def populate_obj(self, obj):
        obj.email = self.email.data
