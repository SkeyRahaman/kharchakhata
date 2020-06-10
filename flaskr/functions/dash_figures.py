import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from flask_login import current_user
from flaskr.functions import *
import calendar
from flaskr import db
from sqlalchemy import func
from flaskr.models import Expences, Type, Type_subtype, Sub_type, Frequency, Payment_medium
from datetime import datetime
import dash_html_components as html


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
                name="Per Day Cumulative",
                visible='legendonly'
            ),
            go.Bar(
                x=date_31,
                y=data_date[1:],
                name="Per Day",
                text="pop"
            )
        ]
        layout_fig1 = go.Layout(
            legend_title_text='Click To Disable or Enable..',
            legend=dict(x=0.6, y=1.25),
            title="Per Day for the month of " + month,
            barmode='overlay',
            xaxis_title="Date of the month",
            yaxis_title="Amount",
            margin=dict(l=5, r=10),
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


def first_pie_chat(month="May", year=2020, expence_type="expence", graph_type="pie"):
    if current_user and current_user.is_authenticated:
        if graph_type == "pie":
            hole = 0
        elif graph_type == "donut":
            hole = 0.4
        if expence_type == "expence":
            b = db.session.query(Type.id,
                                 Type.name,
                                 func.sum(Expences.debit).label('total')) \
                .group_by(Type.id) \
                .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                .join(Type, Type_subtype.type_id == Type.id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        else:
            b = db.session.query(Type.id,
                                 Type.name,
                                 func.sum(Expences.credit).label('total')) \
                .group_by(Type.id) \
                .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                .join(Type, Type_subtype.type_id == Type.id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        if graph_type == "spider":
            data = [
                go.Scatterpolar(
                    r=[i[2] for i in b],
                    theta=[i[1] for i in b],
                    fill='toself',
                    name="Type distribution"
                ),
            ]
            layout = go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                    )),
                title="Type Amount Percentage.",
                annotations=[
                    dict(
                        y=-0.25,
                        showarrow=False,
                        text="",
                        # """"Click On the type over the <br> Pie and Donut chat to <br> see the subtype distribution.""",
                        xref="paper",
                        yref="paper"
                    )
                ],
                margin=dict(l=15, r=15),
            )
        else:
            data = [
                go.Pie(
                    labels=[i[1] for i in b],
                    values=[i[2] for i in b],
                    hole=hole
                )
            ]
            layout = go.Layout(
                legend_title_text='Types.',
                legend=dict(x=0.8, y=1.15),
                title="Type Amount Percentage.",
                annotations=[
                    dict(
                        y=-0.15,
                        showarrow=False,
                        text="""Click On the type to <br> see the subtype distribution.""",
                        xref="paper",
                        yref="paper"
                    )
                ],
                margin=dict(l=15, r=15, t=30),

            )
        return go.Figure(data=data, layout=layout)
    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))


def first_pie_chat_subtype(month="May", year=2020, expence_type="expence", etype=None, graph_type="pie"):
    if current_user and current_user.is_authenticated:
        if graph_type == "pie":
            hole = 0
        elif graph_type == "donut":
            hole = 0.4
        if expence_type == "expence":
            if not etype:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.debit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year)) \
                    .filter(Expences.user_id == current_user.id)
            else:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.debit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(Type.name == etype) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year)) \
                    .filter(Expences.user_id == current_user.id)
        else:
            if not etype:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.credit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year)) \
                    .filter(Expences.user_id == current_user.id)
            else:
                b = db.session.query(Sub_type.name,
                                     func.sum(Expences.credit).label('total')) \
                    .group_by(Sub_type.id) \
                    .join(Type_subtype, Type_subtype.id == Expences.type_subtype_id) \
                    .join(Sub_type, Type_subtype.subtype_id == Sub_type.id) \
                    .join(Type, Type_subtype.type_id == Type.id) \
                    .filter(Type.name == etype) \
                    .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                    .filter(func.year(Expences.date_time) == int(year)) \
                    .filter(Expences.user_id == current_user.id)
        if graph_type == "spider":
            data = [
                go.Scatterpolar(
                    r=[i[1] for i in b],
                    theta=[i[0] for i in b],
                    fill='toself',
                ),
            ]
            if etype:
                title = "Subtype Amount Graph for <br> Type =" + etype + "..."
            else:
                title = "Subtype Amount Graph!"
            layout = go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                    )),
                title=title,
                annotations=[
                    dict(
                        y=-0.25,
                        showarrow=False,
                        text="""Click On the type over the <br> Pie and Donut chat to <br> see the subtype distribution.""",
                        xref="paper",
                        yref="paper"
                    )
                ],
                margin=dict(l=15, r=15),
            )

        else:
            data = [
                go.Pie(
                    labels=[i[0] for i in b],
                    values=[i[1] for i in b],
                    hole=hole,
                )
            ]
            if etype:
                title = "Subtype Amount Graph for <br> Type =" + etype + "..."
            else:
                title = "Subtype Amount Graph!"
            layout = go.Layout(
                title=title,
                legend_title_text='Sub Types.',
                margin=dict(l=15, r=25),
            )
        return go.Figure(data=data, layout=layout)
    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))


def frequency_pie_chat(month="May", year=2020, expence_type="expence", graph_type="pie"):
    if current_user and current_user.is_authenticated:
        if graph_type == "pie":
            hole = 0
        elif graph_type == "donut":
            hole = 0.4
        if expence_type == "expence":
            b = db.session.query(Frequency.id,
                                 Frequency.name,
                                 func.sum(Expences.debit).label('total')) \
                .group_by(Frequency.id) \
                .join(Frequency, Frequency.id == Expences.frequency_id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        else:
            b = db.session.query(Frequency.id,
                                 Frequency.name,
                                 func.sum(Expences.credit).label('total')) \
                .group_by(Frequency.id) \
                .join(Frequency, Frequency.id == Expences.frequency_id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        if graph_type == "spider":
            data = [
                go.Scatterpolar(
                    r=[i[2] for i in b],
                    theta=[i[1] for i in b],
                    fill='toself',
                    name="Type distribution"
                ),
            ]
            layout = go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                    )),
                title="Frequency Amount Graph.",
                annotations=[
                    dict(
                        y=-0.25,
                        showarrow=False,
                        text="",
                        # """Click On the type over the <br> Pie and Donut chat to <br> see the subtype distribution.""",
                        xref="paper",
                        yref="paper"
                    )
                ],
                margin=dict(l=15, r=15),
            )
        else:
            data = [
                go.Pie(
                    labels=[i[1] for i in b],
                    values=[i[2] for i in b],
                    hole=hole
                )
            ]
            layout = go.Layout(
                title="Frequency Amount Graph.",
                margin=dict(l=15, r=25),
            )
        return go.Figure(data=data, layout=layout)
    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))


def payment_type_pie_chat(month="May", year=2020, expence_type="expence", graph_type="pie"):
    if current_user and current_user.is_authenticated:
        if graph_type == "pie":
            hole = 0
        elif graph_type == "donut":
            hole = 0.4
        if expence_type == "expence":
            b = db.session.query(Payment_medium.id,
                                 Payment_medium.name,
                                 func.sum(Expences.debit).label('total')) \
                .group_by(Payment_medium.id) \
                .join(Payment_medium, Payment_medium.id == Expences.payment_id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        else:
            b = db.session.query(Payment_medium.id,
                                 Payment_medium.name,
                                 func.sum(Expences.credit).label('total')) \
                .group_by(Payment_medium.id) \
                .join(Payment_medium, Payment_medium.id == Expences.payment_id) \
                .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
                .filter(func.year(Expences.date_time) == int(year)) \
                .filter(Expences.user_id == current_user.id)
        if graph_type == "spider":
            data = [
                go.Scatterpolar(
                    r=[i[2] for i in b],
                    theta=[i[1] for i in b],
                    fill='toself',
                    name="Type distribution"
                ),
            ]
            layout = go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                    )),
                title="Payment Method And Amount Graph",
                annotations=[
                    dict(
                        y=-0.25,
                        showarrow=False,
                        text="",
                        # """"Click On the type over the <br> Pie and Donut chat to <br> see the subtype distribution.""",
                        xref="paper",
                        yref="paper"
                    )
                ],
                margin=dict(l=15, r=15),
            )
        else:
            data = [
                go.Pie(
                    labels=[i[1] for i in b],
                    values=[i[2] for i in b],
                    hole=hole
                ),
            ]
            layout = go.Layout(
                title="Payment Method And Amount Graph",
                margin=dict(l=15, r=25),
            )
        return go.Figure(data=data, layout=layout)
    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))


def expenditure_income_line_graph(month="May", year=2020):
    if current_user and current_user.is_authenticated:
        b = db.session.query(func.day(Expences.date_time),
                             func.sum(Expences.debit).label('total'),
                             func.sum(Expences.credit).label('total')
                             ).group_by(func.date(Expences.date_time)) \
            .filter(func.month(Expences.date_time) == datetime.strptime(month, '%B').month) \
            .filter(func.year(Expences.date_time) == int(year)) \
            .filter(Expences.user_id == current_user.id)
        data_vs_income = [0 for _ in range(32)]
        data_vs_expence = [0 for _ in range(32)]
        date_31 = [i for i in range(1, 32)]
        for i in b:
            data_vs_income[i[0]] = i[1]
            data_vs_expence[i[0]] = i[2]
        data_vs_income_commutative = [0, ]
        data_vs_expence_commutative = [0, ]
        for i in data_vs_income:
            data_vs_income_commutative.append(data_vs_income_commutative[-1] + i)
        for i in data_vs_expence:
            data_vs_expence_commutative.append(data_vs_expence_commutative[-1] + i)

        data_fig1 = [
            go.Scatter(
                x=date_31,
                y=data_vs_income_commutative[2:],
                name="Data vs Income Commutative",
                mode="markers+lines"
            ),
            go.Scatter(
                x=date_31,
                y=data_vs_expence_commutative[2:],
                name="Data vs Expense Commutative",
                mode="markers+lines"
            ),
        ]
        layout_fig1 = go.Layout(
            title="Income Expense Comparison <br> For the month of " + month,
            barmode='overlay',
            xaxis_title="Date of the month",
            yaxis_title="Commutative Amount",
            legend=dict(x=0.6, y=1.15),
            margin=dict(l=20, r=25),
        )
        return go.Figure(data=data_fig1, layout=layout_fig1)
    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))


def savings_month_wise_bar_graph():
    if current_user and current_user.is_authenticated:
        b = db.session.query(func.month(Expences.date_time),
                             func.year(Expences.date_time),
                             func.sum(Expences.debit).label('total'),
                             func.sum(Expences.credit).label('total')
                             ).group_by(func.month(Expences.date_time),
                                        func.year(Expences.date_time)) \
            .filter(Expences.user_id == current_user.id)

        _ = sorted([[calendar.month_name[i[0]], i[1], i[0], i[2], i[3]] for i in b], key=lambda x: (x[1], x[2]))
        data_fig1 = [
            go.Bar(
                x=[str(i[0]) + " " + str(i[1]) for i in _],
                y=[i[4] - i[3] for i in _],
                name="Savings",
                marker={'color': [i[4] - i[3] for i in _],
                        'colorscale': 'RdYlGn'}
            ),
        ]
        layout_fig1 = go.Layout(
            title="Savings Per month",
            xaxis_title="Month And Year",
            yaxis_title="Amount saved",
        )
        return go.Figure(data=data_fig1, layout=layout_fig1)

    else:
        return go.Figure(data=[go.Pie(labels=[1], values=["None"])],
                         layout=go.Layout(title="Please Login To View Your Data!"))


def get_user_name():
    if current_user and current_user.is_authenticated:
        return [
            html.A(href="/my_account",
                   children='Hi! ' + str(current_user.fname))
        ]
    else:
        return [
            html.Div(className="row", children=[
                    html.Strong("Login")
                ]),
                html.A(className="text-danger", href="/registration_form", children=[
                    html.Strong("Sign Up")
                ]),
                html.A(className="text-danger", href="/about", children=[
                    html.Strong("About")
                ]),
            ]


def get_months():
    if current_user and current_user.is_authenticated:
        month_name = db.session.query(func.month(Expences.date_time),
                                      func.year(Expences.date_time)) \
            .filter(Expences.user_id == current_user.id).distinct()
        _ = sorted([[i[0], i[1], calendar.month_name[i[0]]] for i in month_name], key=lambda x: (x[1], x[0]),
                   reverse=True)
        if _:
            return [{'label': i[2] + " " + str(i[1]), 'value': i[2] + "_" + str(i[1])} for i in _]
        else:
            return [{'label': datetime.now().strftime('%b %Y'), 'value': datetime.now().strftime('%b_%Y')}]
    else:
        return [{'label': "Login First", 'value': datetime.now().strftime('%b_%Y')}]


def get_months_first_value():
    if current_user and current_user.is_authenticated:
        month_name = db.session.query(func.month(Expences.date_time),
                                      func.year(Expences.date_time)) \
            .filter(Expences.user_id == current_user.id).distinct()
        _ = sorted([[i[0], i[1], calendar.month_name[i[0]]] for i in month_name], key=lambda x: (x[1], x[0]),
                   reverse=True)
        if _:
            i = _[0]
            return i[2] + "_" + str(i[1])

    return datetime.now().strftime('%B_%Y')
