from flask import Blueprint

dashboard_route = Blueprint('dashboard', __name__)

from . import routes