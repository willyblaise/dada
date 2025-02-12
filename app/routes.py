from flask import render_template, url_for, redirect, flash, Blueprint, request
from . import db  # Import app and db from the app package
from app.models import User, Measurement
from app.forms import RegistrationForm, MeasurementForm, LoginForm, UserEditForm
from flask_login import login_user, current_user, logout_user, login_required, fresh_login_required
from flask_mail import Message
from app import mail
#from flask_bcrypt import Bcrypt
from flask import Blueprint
from app import db, bcrypt


# Create a Blueprint for the routes
app_routes = Blueprint('app_routes', __name__)

#bcrypt = Bcrypt(app)


# Home route
#@app_routes.route('/')
#def home():
#    return render_template('home.html')

@app_routes.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('app_routes.profile'))
    return render_template("home.html")

# Measurement form route
@app_routes.route('/measurement', methods=['GET', 'POST'])
def measurement_form():
    form = MeasurementForm()
    if form.validate_on_submit():
        flash("Measurements submitted successfully!", "success")
        return redirect(url_for('app_routes.home'))  # Redirect to home route
    return render_template('measurement_form.html', form=form)

# Login route
#@app_routes.route("/login", methods=['GET', 'POST'])
#def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('app_routes.profile'))  # Redirect to profile if already logged in
#    form = LoginForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(email=form.email.data).first()
#        if user and user.password == form.password.data:  # Hash passwords properly in production
#            login_user(user)
#            return redirect(url_for('app_routes.profile'))  # Redirect to profile after login
#        else:
#            flash('Login Unsuccessful. Please check email and password', 'danger')
#    return render_template('login.html', title='Login', form=form)

# Login route
@app_routes.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('app_routes.profile'))  # Redirect to profile if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('app_routes.profile'))  # Redirect to profile after login
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout route
@app_routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('app_routes.home'))  # Redirect to home route after logout


# Confirm email route
@app_routes.route("/confirm_email/<token>")
def confirm_email(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('The confirmation link is invalid or has expired.', 'warning')
        return redirect(url_for('app_routes.register'))  # Redirect to register page if token is invalid
    flash('Your email has been confirmed!', 'success')
    return redirect(url_for('app_routes.profile'))  # Redirect to profile after confirmation


# Registration route
#@app_routes.route("/register", methods=['GET', 'POST'])
#def register():
#    form = RegistrationForm()
#    if form.validate_on_submit():
#        user = User(email=form.email.data, password=form.password.data)
#        db.session.add(user)
#        db.session.commit()
#        token = user.get_reset_token()  # You'll create this function for generating tokens
#        send_confirmation_email(user, token)
#        flash('An email has been sent with instructions to confirm your account!', 'info')
#        return redirect(url_for('app_routes.login'))  # Redirect to login after registration
#    return render_template('register.html', title='Register', form=form)

# Registration route
@app_routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        token = user.get_reset_token()  # You'll create this function for generating tokens
        send_confirmation_email(user, token)
        flash('An email has been sent with instructions to confirm your account!', 'info')
        return redirect(url_for('app_routes.login'))  # Redirect to login after registration
    return render_template('register.html', title='Register', form=form)

# Send confirmation email
def send_confirmation_email(user, token):
    confirm_url = url_for('app_routes.confirm_email', token=token, _external=True)
    msg = Message('Please Confirm Your Email', recipients=[user.email])
    msg.body = f'Your confirmation link is: {confirm_url}'
    mail.send(msg)


#@app_routes.route("/profile", methods=['GET', 'POST'])
#@login_required
#def profile():
#    form = MeasurementForm()  # Ensure form is instantiated
#
#    if form.validate_on_submit():
#        measurement = Measurement(
#            chest=form.chest.data,
#            waist=form.waist.data,
#            inseam=form.inseam.data,
#            head=form.head.data,  # Ensure this field exists in your model
#            neck_circumference=form.neck_circumference.data,
#            shoulder_width=form.shoulder_width.data,
#            sleeve_length=form.sleeve_length.data,
#            buba_length=form.buba_length.data,
#            user_id=current_user.id
#        )
#        db.session.add(measurement)
#        db.session.commit()
#        flash("Your measurements have been saved!", "success")
#        return redirect(url_for("app_routes.profile"))  # Redirect to avoid re-submission
#
#    return render_template("profile.html", title="Profile", form=form)  # Ensure form is passed

@app_routes.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = MeasurementForm()

    if form.validate_on_submit():
        measurement = Measurement(
            chest=form.chest.data,
            waist=form.waist.data,
            inseam=form.inseam.data,
            head=form.head.data,
            neck_circumference=form.neck_circumference.data,
            shoulder_width=form.shoulder_width.data,
            sleeve_length=form.sleeve_length.data,
            buba_length=form.buba_length.data,
            user_id=current_user.id
        )
        db.session.add(measurement)
        db.session.commit()
        flash("Your measurements have been saved!", "success")
        return redirect(url_for("app_routes.profile"))

    elif request.method == "POST":  # Form was submitted but validation failed
        flash("There was an error with your submission. Please check your inputs.", "danger")

    return render_template("profile.html", title="Profile", form=form)



@app_routes.route("/admin", methods=['GET', 'POST'])
@fresh_login_required
def admin():
    if not getattr(current_user, "is_admin", False):  # Safely check is_admin
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('app_routes.profile'))

    users = User.query.all()
    return render_template('admin_dashboard.html', title='Admin Dashboard', users=users)


@app_routes.route("/edit_user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('app_routes.profile'))

    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        print("Form validated successfully")
        user.email = form.email.data
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print("User object updated")
        try:
            db.session.commit()
            print("Database changes committed")
            flash('User details updated successfully', 'success')
            return redirect(url_for('app_routes.admin'))
        except Exception as e:
            db.session.rollback()
            print("Error committing database changes:", str(e))
            flash('Error updating user details', 'error')

    return render_template('edit_user.html', title='Edit User', form=form, user=user)

@app_routes.route("/delete_user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':  # Ensure the user is an admin
        return redirect(url_for('app_routes.profile'))

    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error occurred while deleting the user.', 'danger')

    return redirect(url_for('app_routes.admin'))  # Redirect to the admin dashboard



@app_routes.route("/admin/view_user/<int:user_id>", methods=['GET'])
@login_required
def admin_view_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('app_routes.profile'))

    user = User.query.get_or_404(user_id)

    return render_template('admin_view_user.html', title=f"{user.email} Profile", user=user)



@app_routes.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('app_routes.profile'))
    return render_template('admin_dashboard.html')
