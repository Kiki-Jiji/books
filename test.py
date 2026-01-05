import pandas as pd
import plotly.express as px
from functions import calulate_price

books_groups:dict[str,dict[int, str]] = {
    'dreaming_devon': {
        1:  'Sunsets Over Salcombe',
        2:  'Broken-Hearted on Blackpool Sands',
        3:  'Happily Ever After in Hope Cove',
        4: 'Coming Home to Kingsbridge',
    }
}


all_sheets = pd.read_excel('DATA.xlsx', sheet_name=None)

Summary = all_sheets['Summary']


sales = all_sheets['Combined Sales']

books_groups['dreaming_devon'].values()

series = sales[sales['Title'].isin(books_groups['dreaming_devon'].values())]

[['Title', 'Royalty']].groupby('Title').cumsum()

all_data = []
for i in series['Title'].unique():
    book_data = series[series['Title'] == i].sort_values('Royalty Date').reset_index(drop=True)

    book_data['Royalty_cumsum'] = book_data['Royalty'].cumsum()
    all_data.append(book_data)

all_data = pd.concat(all_data)

px.line(all_data, x ='Royalty Date', y = 'Royalty_cumsum', color='Title')

prices = calulate_price(sales)

standard = sales[sales['Transaction Type'] == 'Standard']



cols = ['Royalty Date', 'Title',
       'Net Units Sold',
       'Royalty',]

sales = sales[cols]


b = [ 'Lawyers and Lattes: Happily Ever After in Devon','The Worst Christmas Ever?: Christmas in Devon',]
b = books_groups['dreaming_devon'].values()

books = sales[sales['Title'].isin(b)]


sold = books.groupby('Title')['Net Units Sold'].sum().sort_values().to_dict()
books_groups['dreaming_devon'][1]



first = sold[books_groups['dreaming_devon'][1]]

p = {}
for i in sold:
    p[i] = sold[i] / first


total = 0.0
marginal_gains = {}
for i in p:
    marginal_gain = p[i] * prices[i]
    marginal_gains[i] = marginal_gain
    total += marginal_gain





############
