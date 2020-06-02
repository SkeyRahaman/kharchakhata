import plotly.graph_objects as go
import plotly.figure_factory as ff
from flask_login import current_user
from flaskr.functions import *
import calendar
from flaskr import db
from sqlalchemy import func
from flaskr.models import Expences, Type, Type_subtype, Sub_type
from datetime import datetime


def first_bar_graph(month="May", year=2020, expence_type="expence"):
    if current_user and current_user.is_authenticated:
        if expence_type == "expence":
            b = db.session.query(func.day(Expences.date_time),
                                 func.sum(Expences.debit).label('total'),
                                 ).group_by(func.date(Expences.date_time)) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        else:
            b = db.session.query(func.day(Expences.date_time),
                                 func.sum(Expences.credit).label('total'),
                                 ).group_by(func.date(Expences.date_time)) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        data_date = [0 for _ in range(32)]
        date_31 = [i for i in range(1, 32)]
        for i in b:
            data_date[i[0]] = i[1]
        data_date_1 = [0, ]
        for i in data_date:
            data_date_1.append(data_date_1[-1] + i)
        data_fig1 = [
            go.Bar(
                x=date_31,
                y=data_date_1[2:],
                name="Per Day Cumulative"
            ),
            go.Bar(
                x=date_31,
                y=data_date[1:],
                name="Per Day"
            )
        ]
        layout_fig1 = go.Layout(
            title="Per Day for the month of " + month,
            barmode='overlay',
            xaxis_title="Date of the month",
            yaxis_title="Amount",
        )
        return go.Figure(data=data_fig1, layout=layout_fig1)
    else:
        return go.Figure(data=[go.Bar(x=[1, 2], y=[1, 2])],
                         layout=go.Layout(title="Please login To view Your Data"))


def first_heatmap_graph(month="May", year=2020, expence_type="expence"):
    if current_user and current_user.is_authenticated:
        if expence_type == "expence":
            b = db.session.query(func.day(Expences.date_time),
                                 func.sum(Expences.debit).label('total'),
                                 ).group_by(func.date(Expences.date_time)) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        else:
            b = db.session.query(func.day(Expences.date_time),
                                 func.sum(Expences.credit).label('total'),
                                 ).group_by(func.date(Expences.date_time)) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        data_date = [0 for _ in range(1, 33)]
        for i in b:
            data_date[i[0]] = i[1]
        act_data = []
        for i in calendar.Calendar().monthdayscalendar(month=datetime.strptime(month, '%B').month, year=2020):
            a = []
            for j in i:
                a.append(data_date[j])
            act_data.append(a)
        calendar_dates = calendar.Calendar().monthdayscalendar(month=datetime.strptime(month, '%B').month, year=2020)
        for i in range(len(calendar_dates)):
            for j in range(len(calendar_dates[i])):
                if calendar_dates[i][j] == 0:
                    calendar_dates[i][j] = ""
        fig = ff.create_annotated_heatmap([act_data[i] for i in range(len(act_data) - 1, -1, -1)],
                                          x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
                                             'Sunday'],
                                          annotation_text=[calendar_dates[i] for i in
                                                           range(len(calendar_dates) - 1, -1, -1)],
                                          colorscale='Reds',
                                          )
        fig.update_layout(
            title="Per Day for the month of " + month,
            xaxis_title="Day of the week",
            yaxis_title="Week",
        )
        return fig
    else:
        return go.Figure(data=[go.Bar(x=[1, 2], y=[1, 2])],
                         layout=go.Layout(title="Please login To view Your Data"))


def first_pie_chat(month="May", year=2020, expence_type="expence"):
    if current_user and current_user.is_authenticated:
        if expence_type == "expence":
            b = db.session.query(Type.id,
                                 Type.name,
                                 func.sum(Expences.debit).label('total')) \
                .group_by(Type.id) \
                .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                .join(Type, Type_subtype.type_id == Type.id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year))
        else:
            b = db.session.query(Type.id,
                                 Type.name,
                                 func.sum(Expences.credit).label('total')) \
                .group_by(Type.id) \
                .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                .join(Type, Type_subtype.type_id == Type.id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year))
        data = [
            go.Pie(
                labels=[i[1] for i in b],
                values=[i[2] for i in b]
            )
        ]
        layout = go.Layout(
            title="Total " + expence_type + " with Type.!"
        )
        return go.Figure(data=data, layout=layout)
    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))


def first_pie_chat_subtype(month="May", year=2020, expence_type="expence", etype=None):
    if current_user and current_user.is_authenticated:
        if expence_type == "expence":
            if not etype:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.debit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year))
            else:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.debit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(Type.name == etype) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year))
        else:
            if not etype:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.credit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year))
            else:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.credit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(Type.name == etype) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year))
        data = [
            go.Pie(
                labels=[i[0] for i in b],
                values=[i[1] for i in b],
            )
        ]
        if etype:
            title = "Total " + expence_type + " with Type " + etype + "..."
        else:
            title = "Subtype Graph!"
        layout = go.Layout(
            title=title
        )
        return go.Figure(data=data, layout=layout)
    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))
