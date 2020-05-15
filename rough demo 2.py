from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@127.0.0.1/kharchakhatadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

users = db.Table('users', db.metadata, autoload=True, autoload_with=db.engine)

# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
#
# users = Base.classes.users

@app.route('/')
def index():
    res = db.session.query(users).all()
    for r in res:
        print(r.lname)
    return ""

if __name__=="__main__":
    app.run(debug=True)
