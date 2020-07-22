from flask import Blueprint

bp = Blueprint('teams', __name__)

from app.teams import routes