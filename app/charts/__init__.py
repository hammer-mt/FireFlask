from flask import Blueprint

bp = Blueprint('charts', __name__)

from app.charts import routes