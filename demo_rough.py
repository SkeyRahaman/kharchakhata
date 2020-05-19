from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)

bcr = Bcrypt(app)
pas = bcr.generate_password_hash("9038383080").decode('utf-8')
a = True
while a:
    a = input("Password:-")
    print(bcr.generate_password_hash(a).decode('utf-8'))

