from flaskr.models import Expences
from flaskr import db
from datetime import datetime
from sqlalchemy import func

print(Expences.query.filter_by(id=2).first().date_time)
