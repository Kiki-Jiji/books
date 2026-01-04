import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from functions import calulate_price, get_book_groups

# --- DATA INITIALIZATION ---
all_sheets = pd.read_excel('DATA.xlsx', sheet_name=None)
sales_raw = all_sheets['Combined Sales']
sales_raw['Royalty Date'] = pd.to_datetime(sales_raw['Royalty Date'])
prices = calulate_price(sales_raw)

books_groups = get_book_groups()
target_titles = list(books_groups['dreaming_devon'].values())
first_book_title = books_groups['dreaming_devon'][1]

# --- APP SETUP ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col(html.H1("Dreaming Devon: Sales Analytics", className="text-center text-primary mb-4"), width=12)
    ], className="mt-4"),

    # Filter Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filter by Date Range", className="card-title"),
                    dcc.DatePickerRange(
                        id='date-picker',
                        min_date_allowed=sales_raw['Royalty Date'].min(),
                        max_date_allowed=sales_raw['Royalty Date'].max(),
                        start_date= pd.to_datetime("2025-01-01"),
                        end_date=sales_raw['Royalty Date'].max(),
                        className="mb-3"
                    ),
                    html.Div(id='summary-stats', className="h3 text-success")
                ])
            ], color="light", outline=True)
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Volume: Net Units Sold"),
                dbc.CardBody([dcc.Graph(id='units-sold-chart')])
            ])
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Value: Marginal Gains per Unit"),
                dbc.CardBody([dcc.Graph(id='marginal-gains-chart')])
            ])
        ], md=6),
    ]),

    html.Footer("Sales Data Analysis Tool © 2024", className="text-center text-muted mt-5")
], fluid=True)

@app.callback(
    [Output('units-sold-chart', 'figure'),
     Output('marginal-gains-chart', 'figure'),
     Output('summary-stats', 'children')],
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_dashboard(start_date, end_date):
    mask = (sales_raw['Royalty Date'] >= start_date) & (sales_raw['Royalty Date'] <= end_date)
    filtered_sales = sales_raw.loc[mask].copy()
    
    books = filtered_sales[filtered_sales['Title'].isin(target_titles)]
    sold = books.groupby('Title')['Net Units Sold'].sum().to_dict()
    first_units = sold.get(first_book_title, 0)
    
    data_list = []
    total_gain = 0.0

    for title in target_titles:
        units = sold.get(title, 0)
        ratio = units / first_units if first_units > 0 else 0
        price = prices.get(title, 0)
        gain = ratio * price
        
        total_gain += gain
        data_list.append({
            'Title': title, 
            'Units': units, 
            'Marginal Gain': round(gain, 2)
        })

    df_plot = pd.DataFrame(data_list)

    # Styling for Charts
    template = "plotly_dark"

    fig_units = px.bar(df_plot, x='Title', y='Units', 
                       color='Units', template=template,
                       color_continuous_scale='Blues')
    fig_units.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20))

    # Figure 2: Marginal Gains
    fig_gains = px.bar(df_plot, x='Title', y='Marginal Gain', 
                       color='Marginal Gain', template=template,
                       color_continuous_scale='Greens', text_auto=True)
    fig_gains.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20))

    summary_text = f"Total Marginal Gain: £{total_gain:.2f}"
    
    return fig_units, fig_gains, summary_text

if __name__ == '__main__':
    app.run(debug=True)