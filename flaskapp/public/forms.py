# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired

from flaskapp.user.models import User


class LoginForm(Form):
    """Login form."""
    LANGUAGES = ['zh']

    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append('用户名不存在！')
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append('密码不正确！')
            return False

        if not self.user.active:
            self.username.errors.append('用户未激活！')
            return False
        return True
