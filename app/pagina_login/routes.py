from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import User



login_route = Blueprint('login_route', __name__)




@login_route.route('/login', methods=["POST","GET"])
def login():
    return render_template('login.html')