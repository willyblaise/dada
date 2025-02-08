from flask import current_app
from yourapp.models import User

def send_registration_email(user_id):
    user = User.query.get(user_id)
    receiver_email = user.email

    msg = EmailMessage()
    msg.set_content('Hello, welcome to our site!')

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.sendmail(current_app.config['MAIL_USERNAME'], receiver_email, msg.as_string())
