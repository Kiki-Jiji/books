
import pandas as pd

def calulate_price(sales:pd.DataFrame) -> dict[str, float]:
        
    prices = {}
    for t in sales['Title'].unique():

        f = (sales['Transaction Type'] == 'Standard') & (sales['Title'] == t)

        book_sales = sales[f]

        latest = book_sales[book_sales['Royalty Date'] == book_sales['Royalty Date'].max()]

        gbp = latest[latest['Currency'] == 'GBP']

        if len(gbp) == 0:
            continue

        unit_royalty = gbp['Royalty'] / gbp['Net Units Sold']

        prices[t] = float(unit_royalty.iloc[0])

    return prices


def get_book_groups() -> dict[str,dict[int, str]]:

    books_groups = {
    'dreaming_devon': {
        1:  'Sunsets Over Salcombe',
        2:  'Broken-Hearted on Blackpool Sands',
        3:  'Happily Ever After in Hope Cove',
        4: 'Coming Home to Kingsbridge',
    }
    }

    return books_groups
