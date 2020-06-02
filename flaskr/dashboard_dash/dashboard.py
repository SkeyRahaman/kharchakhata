import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flaskr.functions import *
from flaskr.models import Expences
from flaskr import app, db
from sqlalchemy import func
from flask_login import current_user
from flask import session

month_name = db.session.query(func.month(Expences.date_time),
                              func.year(Expences.date_time)).distinct()
_ = sorted([[i[0], i[1], calendar.month_name[i[0]]] for i in month_name], key=lambda x: (x[1], x[0]), reverse=True)
month_name = [{'label': i[2] + " " + str(i[1]), 'value': i[2] + "_" + str(i[1])} for i in _]


def create_dashboard(server=app):
    external_stylesheets = [
        {
            'rel': "stylesheet",
            'href': "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
            "integrity": "sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh",
            "crossorigin": "anonymous"
        }
    ]
    external_scripts = [
        {
            'src': "https://code.jquery.com/jquery-3.4.1.slim.min.js",
            'integrity': "sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n",
            'crossorigin': "anonymous"
        }, {
            'src': "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
            'integrity': "sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo",
            'crossorigin': "anonymous"
        }, {
            'src': "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js",
            'integrity': "sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6",
            'crossorigin': "anonymous"
        }
    ]

    dash_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
    )

    dash_app.title = 'KharchaKhata - Dashboard'
    dash_app.layout = html.Div([

        # hedder

        html.Nav(className='navbar heading', children=[
            html.Strong(id='name_app', children=[
                html.A(href="/dashboard/all/all", children='KHARCHAKHATA')
            ]),
            html.Strong(id='my_account', children=[
                html.A(href="/my_account", children='Hi! ')
            ])
        ]),

        # Navbar

        html.Nav(className="navbar navbar-expand-lg navbar-light bg-light", children=[
            html.Button(className="navbar-toggler", type="button", id="navbar-button", children=[
                html.Span(className="navbar-toggler-icon")
            ]),
            html.Div(className="collapse navbar-collapse", id="navbarNav", children=[
                html.Ul(className="navbar-nav", children=[
                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link", href="/", children=[
                            html.Strong("Dashboard")
                        ])
                    ]),
                    html.Li(className="nav-item active", children=[
                        html.A(className="nav-link", href="/dashapp/", children=[
                            html.Strong("Charts")
                        ])
                    ]),

                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link", href="/my_account", children=[
                            html.Strong("My Account")
                        ])
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link", href="/add_expence", children=[
                            html.Strong("Add Transaction")
                        ])
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link", href="/about", children=[
                            html.Strong("About")
                        ])
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link", href="/settings", children=[
                            html.Strong("Settings")
                        ])
                    ]),
                    html.Li(className="nav-item", children=[
                        html.A(className="nav-link", href="/logout", children=[
                            html.Strong("Logout")
                        ])
                    ]),
                    html.Li(className="nav-item", children=[
                        html.Div(id="month_dropdown", children=[
                            dcc.Dropdown(id="month_select",
                                         searchable=False,
                                         clearable=False,
                                         style={
                                             'position': 'relative',
                                             'zIndex': '999',
                                             'width': '150px'
                                         },
                                         options=month_name,
                                         value=month_name[0]['value']),
                        ]),
                    ]),
                    html.Li(className="nav-item", children=[
                        html.Div(id="income_dropdown", children=[
                            dcc.Dropdown(id="expence_type",
                                         searchable=False,
                                         clearable=False,
                                         style={
                                             'position': 'relative',
                                             'zIndex': '998',
                                             'width': '150px'
                                         },
                                         value="expenditure",
                                         options=[
                                             {'label': 'Expenditure', 'value': 'expence'},
                                             {'label': 'Income', 'value': 'income'}
                                         ]),
                        ]),
                    ]),
                ])
            ])
        ]),

        # DashBoard

        html.Div(className="row container-fluid", children=[
            html.Div(className="col-md-6 col-sm-12 p-2 mx-auto", children=[
                html.Div(className="bg-light card row", children=[
                    html.Div(className="col-11 btn-group btn-group-toggle mx-auto mt-2", id="fig1_togel", children=[
                        html.Label(className="btn btn-outline-dark active", children=[
                            "Bar Graph",
                            dcc.Input(type="radio", id='graph1_btn1')
                        ]),
                        html.Label(className="btn btn-outline-dark", children=[
                            "Histogram",
                            dcc.Input(type="radio", id='graph1_btn2')
                        ]),
                    ]),
                    html.Div(id="graph1_1", className='col-11 mx-auto mb-2', children=[
                        dcc.Graph(
                            id="bar_graph",
                            figure=first_bar_graph()
                        )
                    ]),
                    html.Div(id="graph1_2", className='col-11  mx-auto mb-2', children=[
                        dcc.Graph(
                            id="Heatmap",
                            figure=first_heatmap_graph(),
                        )
                    ]),
                ])
            ]),
            html.Div(className="col-md-6 col-sm-12 p-2 mx-auto", children=[
                html.Div(className="bg-light card px-auto", children=[
                    html.Div(className="row", children=[
                        html.Div(className="col-6 m-auto", children=[
                            dcc.Graph(
                                id="first_pie_chat",
                                figure=first_pie_chat("may", 2020, "Expenditure"),
                            ),
                        ]),
                        html.Div(className="col-6", children=[
                            dcc.Graph(
                                id="first_pie_chat_subtype",
                                figure=first_pie_chat_subtype(month="May",
                                                              year=2020,
                                                              expence_type=None,
                                                              etype=None)
                            )
                        ])
                    ])
                ])
            ]),
            html.Div(className="col-md-6 col-sm-12", children=[
                dcc.Dropdown(className="bv", options=["Earning", "Expendature"])
            ]),
            html.Div(className="col-md-6 col-sm-12", children=[
                dcc.Dropdown(className="bv", options=["Earning", "Expendature"])
            ]),
        ]),

        # Footer
        html.Div(className='footer text-center', children=[
            html.A(href="http://shakib-portfolio-app.herokuapp.com/", children=[
                html.Div("A Complete Project By Md Shakib Mondal", className="btn")
            ]),
        ]),
    ])

    @dash_app.callback(Output(component_id='Heatmap', component_property='figure'),
                       [Input(component_id='expence_type', component_property='value'),
                        Input(component_id='month_select', component_property='value')]
                       )
    def update_heat_map(input_value, month_select):
        return first_heatmap_graph(month=month_select.split("_")[0],
                                   year=month_select.split("_")[1],
                                   expence_type=input_value)

    @dash_app.callback(Output(component_id='bar_graph', component_property='figure'),
                       [Input(component_id='expence_type', component_property='value'),
                        Input(component_id='month_select', component_property='value')]
                       )
    def update_heat_map(input_value, month_select):
        return first_bar_graph(month=month_select.split("_")[0],
                               year=month_select.split("_")[1],
                               expence_type=input_value)

    @dash_app.callback(Output(component_id='first_pie_chat', component_property='figure'),
                       [Input(component_id='expence_type', component_property='value'),
                        Input(component_id='month_select', component_property='value')]
                       )
    def update_heat_map(input_value, month_select):
        return first_pie_chat(month=month_select.split("_")[0], year=month_select.split("_")[1],
                              expence_type=input_value)

    @dash_app.callback(Output(component_id='first_pie_chat_subtype', component_property='figure'),
                       [Input(component_id='expence_type', component_property='value'),
                        Input(component_id='month_select', component_property='value'),
                        Input(component_id='first_pie_chat', component_property='clickData')]
                       )
    def update_all(input_value, month_select, graph_data):
        try:
            etype = graph_data['points'][0]['label']
        except:
            etype = None
        return first_pie_chat_subtype(month=month_select.split("_")[0],
                                      year=month_select.split("_")[1],
                                      expence_type=input_value,
                                      etype=etype)

    return dash_app.server
