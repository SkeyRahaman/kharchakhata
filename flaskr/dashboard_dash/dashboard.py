import dash
import dash_core_components as dcc
import dash_html_components as html
from flaskr.functions import *
from flaskr.functions import *


def create_dashboard(server):
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
        html.Div(className="row", children=[
            html.Div(className="text-left col-6", children=[
                html.H3("GRAPHS!")
            ]),
            html.Div(className="text-right col-6", children=[
                html.H3("Back")
            ]),
        ]),

        # DashBoard
        html.Div(className="row container-fluid", children=[
            html.Div(className="col-md-6 col-sm-12", children=[
                html.Div(className="row", children=[
                    html.Button(id="graph1_btn1", className='btn col-5', children="Histogram"),
                    html.Button(id="graph1_btn2", className='btn col-5', children="Line Graph"),
                    html.Div(id="graph1_1", className='col-11 m-auto', children=[
                        dcc.Graph(
                            id="Heatmap",
                            figure=first_heatmap_graph("March")
                        )
                    ]),
                    html.Div(id="graph1_2", className='col-11 m-auto', children=[
                        dcc.Graph(
                            id="bar_graph",
                            figure=first_bar_graph("March"),
                        )
                    ]),
                ])
            ]),
            html.Div(className="col-md-6 col-sm-12", children=[
                html.Div(className="row", children=[
                    dcc.Graph(
                        id="first_pie_chat",
                        className="col-6",
                        figure=first_pie_chat(),
                    ),
                    html.Div(className="col-6", children=[
                        dcc.Dropdown(options=["Expendature", "Earning"]),
                        dcc.Graph(
                            id="first_pie_chat_subtype",
                            figure=first_pie_chat_subtype(),
                        )
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
            html.Div("A Complete Project By Md Shakib Mondal")
        ]),

    ])
    return dash_app.server
