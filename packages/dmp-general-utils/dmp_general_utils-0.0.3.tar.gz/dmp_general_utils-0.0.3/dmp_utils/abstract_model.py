from datetime import datetime

import pytz
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModal:
    created_at = db.Column(db.Integer, server_default=str(datetime.now().astimezone(pytz.utc).timestamp()))
    updated_at = db.Column(db.Integer, server_default=str(datetime.now().astimezone(pytz.utc).timestamp()))
