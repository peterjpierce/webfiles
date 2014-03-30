from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, validators

import webfiles.util.auth as auth


class LoginForm(Form):
    """Fields for a login form."""
    username = StringField('Username', [validators.Required('Username is missing')])
    password = PasswordField('Password', [validators.Required('Password is missing')])
    submit = SubmitField('Sign In')

    def validate(self):
        """Validate the input and authenticate the user."""
        if Form.validate(self):
            if auth.is_valid_login(self.username.data, self.password.data):
                return True
        self.username.errors.insert(0, 'Invalid credentials, try again')
        return False
