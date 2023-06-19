import numpy as np
import pandas as pd
from io import BytesIO

from apyori import apriori


class Mlalgo:

    def run(self, file):
        data = pd.read_excel(BytesIO(file), engine='openpyxl')

        data.dropna(inplace=True)
        print("Hello-1")
        data.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
        data['InvoiceDate']=data['InvoiceDate'].astype('int64')
        data['CustomerID'] = data['CustomerID'].astype('int64')
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
        print("Hello-2")
        data['Year'] = data['InvoiceDate'].dt.year
        data['Month-Year'] = data['InvoiceDate'].dt.month
        data['Month-Year'] = data['Month-Year'].apply(
            str)+"-"+data['Year'].apply(str)
        products = data['Description'].unique()
        print("Hello-3")

        dummy = pd.get_dummies(data=data, columns=[
                               'Description'], dummy_na=True)
        dummy = pd.get_dummies(data['Description'])
        data.drop(['Description'], inplace=True, axis=1)
        data = data.join(dummy)
        print("Hello-4")
        data1 = data.groupby(['CustomerID', 'InvoiceDate'])[products[:]].sum()

        data1 = data1.reset_index()[products]
        print("Hello-5")
        data1 = data1.apply(product_names, products=products, axis=1)
        print("Hello-6")
        x = data1.values
        x = [sub[~(sub == 0)].tolist() for sub in x if sub[sub != 0].tolist()]
        transactions = x
        print("Hello-7")
        rules = apriori(transactions, min_support=0.00030,
                        min_confidence=0.05, min_lift=3, max_length=2, target="rules")
        association_results = list(rules)
        datalist = []
        print("Hello-8")

        for item in association_results:
            pair = item[0]
            items = [x for x in pair]
            rule=items[0], " -> " + items[1]
            data = {'rule': rule,
                    'support': str(item[1]),
                    'confidence': str(item[2][0][2]),
                    'lift': str(item[2][0][3])}
            datalist.append(data)

            print("Rule : ", items[0], " -> " + items[1])
            print("Support : ", str(item[1]))
            print("Confidence : ", str(item[2][0][2]))
            print("Lift : ", str(item[2][0][3]))
            print("=============================")
        print("Hello-9")
        return datalist


def product_names(x , products):
    for product in products:
        if x[product] > 0:
            x[product] = product
    return x
