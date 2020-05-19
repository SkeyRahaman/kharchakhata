import plotly.graph_objects as go
from flask_login import current_user
from flask import session
from flaskr.functions import *
import calendar
import numpy as np


def first_bar_graph(month, user_id=5):
    first_graph_data = dashboard_bargraph_data(user_id, month=month)
    data_fig1 = [
        go.Bar(
            x=first_graph_data["Date_n"],
            y=first_graph_data["Amount_comm"],
            name="Per Day Cumulative"
        ),
        go.Bar(
            x=first_graph_data["Date_n"],
            y=first_graph_data["Amount"],
            name="Per Day"
        )
    ]
    layout_fig1 = go.Layout(
        title="Per Day",
        barmode='overlay',
        xaxis_title="Date of the month",
        yaxis_title="Amount",
    )
    return go.Figure(data=data_fig1, layout=layout_fig1)


def first_heatmap_graph(month, year=2020, user_id=5):
    data = dashboard_bargraph_data(user_id=user_id, month=month)
    # print(data)
    arr = np.array(
        calendar.Calendar().monthdayscalendar(year=datetime.now().year, month=datetime.strptime(month, '%B').month))
    total_number_of_weeks = len(arr) * 7
    heat_data = pd.DataFrame(arr.reshape(total_number_of_weeks, 1))
    heat_data.columns = ["Date_n"]
    # print(heat_data.reset_index().merge(data[["Date_n", "Amount"]], left_on="Date_n", right_on="Date_n", how='outer').sort_values(by=['index']))
    data_for_heatmap = np.array(
        heat_data.reset_index().merge(data[["Date_n", "Amount"]], left_on="Date_n", right_on="Date_n",
                                      how='outer').sort_values(by=['index'])["Amount"]).reshape(len(arr), 7)

    data = [
        go.Heatmap(
            z=data_for_heatmap,
            x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            colorscale="Reds",
            text=arr
        )
    ]
    layout = go.Layout(
        title="Per Day for the month of " + month,
        xaxis_title="Day of the week",
        yaxis_title="Week"
    )
    return go.Figure(data=data, layout=layout)


# first_heatmap_graph("March")

def first_pie_chat():
    data = get_pie_chat_data()
    data = [
        go.Pie(
            labels=data["type"],
            values=data["Amount"]
        )
    ]
    return go.Figure(data=data)


def first_pie_chat_subtype():
    data = get_pie_chat_data_subtype()
    data = [
        go.Pie(
            labels=data["type"],
            values=data["Amount"]
        )
    ]
    return go.Figure(data=data)
