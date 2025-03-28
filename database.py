from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import UserModel, db
from flask_login import login_user, logout_user, login_required

# Authentication module
auth = Blueprint('auth', __name__)

class AuthService:
    """Service for handling authentication operations."""
    @staticmethod
    def login_user(email, password):
        user = UserModel.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return True
        return False

    @staticmethod
    def register_user(email, name, password):
        if UserModel.query.filter_by(email=email).first():
            return False
        new_user = UserModel(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return True

    @staticmethod
    def logout_user():
        logout_user()
