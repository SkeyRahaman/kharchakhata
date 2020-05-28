from flaskr.models import Expences
from flaskr import db
from datetime import datetime
from sqlalchemy import func

a = db.session.query(func.sum(Expences.credit).label("credit"),
                     func.sum(Expences.debit).label("debit"),
                     (func.sum(Expences.credit) - func.sum(Expences.debit)).label("profit")) \
    .filter(Expences.user_id == 2).filter((func.month(Expences.date_time) == 5)).filter(func.year(Expences.date_time) == 2019).first()
b = db.session.query((func.sum(Expences.credit) - func.sum(Expences.debit)).label("profit")) \
    .filter(Expences.user_id == 2).filter(func.month(Expences.date_time) == (datetime.now().month - 1))\
    .first()

c = db.session.query(func.month(Expences.date_time),
                     func.year(Expences.date_time)).distinct()
print(sorted([[i[0], i[1]] for i in c], key=lambda x: (x[1], x[0]), reverse=True))


# print(a[-1].date_time)
# b = db.session.query(Expences).filter_by(user_id=2)\
#     .filter(Expences.date_time >= a[0].date_time)


for i in range(10):
    print("*****************")
print(a.credit, a.debit, a.profit, b.profit)
print((datetime.now().month - 1))
