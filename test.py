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
