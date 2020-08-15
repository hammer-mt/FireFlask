from flask import Blueprint

bp = Blueprint('connectors', __name__)

from app.connectors import routes