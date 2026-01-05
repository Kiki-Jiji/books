import dash
from dash import html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html, Input, Output, callback
from functions import get_book_groups
import plotly.express as px

dash.register_page(__name__, path='/')


# Load data specifically for the table view
all_sheets = pd.read_excel('DATA.xlsx', sheet_name=None)
sales = all_sheets['Combined Sales']
books_groups = get_book_groups()


series = sales[sales['Title'].isin(books_groups['dreaming_devon'].values())]

all_data = []
for i in series['Title'].unique():
    book_data = series[series['Title'] == i].sort_values('Royalty Date').reset_index(drop=True)

    book_data['Royalty_cumsum'] = book_data['Royalty'].cumsum()
    all_data.append(book_data)

all_data = pd.concat(all_data)

fig = px.line(all_data, x ='Royalty Date', y = 'Royalty_cumsum', color='Title', template="plotly_dark")



layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("Dreaming Devon: Sales Analytics", className="text-center text-primary mb-4"), width=12)
    ], className="mt-4"),

    dbc.Row([
        dbc.Col([
            dbc.CardBody([dcc.Graph(figure=fig)]),
        ])
    ])
], fluid=True)


