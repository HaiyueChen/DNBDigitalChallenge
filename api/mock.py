import numpy as np
import json
import urllib
import itertools


# Use mock_singl_month

categ = ["Mat og drikke", "Bil og transport","Bolig og fritidsbolig","Ferige og fritid", "Sparing","Faste utgifter","Ikke kategorisert"]
amounts = [800.00, 3200.00, 15000.00, 2000.00, 0.00, 2000.00, 100.00]



def mock_transport(total_sum):
    children = []
    ids = ["Billån", "Verksted og vedlikehold", "Bompenger og parkerings", "Offentlig transport", "Diverse bil transport"]
    billan = (total_sum-1000.0-800.0)
    sum = [billan, 0.0, 1000.0, 800.0, 0.0]

    for i in range(len(ids)):
        cat = {}
        cat["name"] = ids[i]
        cat["size"] = sum[i]
        cat["children"] = []
        children.append(cat)
    return np.sum(sum), children

def mock_mat(total_sum=500):
    children = []
    ids = ["Kjøtt", "Frukt", "Grønnsaker", "Melkeprodukt", "Smågodt", "Diverse"]
    summ = [800.0, 200.0, 300.0, 200.0, 400.0, 0.0]

    for i in range(len(ids)):
        cat = {}
        cat["name"] = ids[i]
        cat["size"] = summ[i]
        cat["children"] = []
        children.append(cat)
    return np.sum(summ), children


def mock_single_month(ids=categ, total_sum=amounts):
    data = {}
    categories = []
    for i in range(len(ids)):
        cat = {}
        cat['name'] = ids[i]
        if ids[i] == "Bil og transport":
            cat['size'], cat["children"] = mock_transport(total_sum[i])
        elif ids[i] == "Mat og drikke":
            cat['size'], cat["children"] = mock_mat(total_sum[i])
        else:
            cat['size'] = total_sum[i]
            cat['children'] = []
        categories.append(cat)

    data["name"] = 'categories'
    data['children'] = categories
    return data

def mock_normal_consumption():
    normal_consumption = [2000.0, 800.0, 15000.0, 500.0, 2000.0, 1000.0, 100.0]

    sizes = []
    for i in range(len(normal_consumption)):
        map = {}
        map["name"] = categ[i]
        map["size"] = normal_consumption[i]
        sizes.append(map)
    return np.sum(normal_consumption), sizes




def mock_year():
    months = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun","Jul","Aug", "Sep", "Okt","Nov","Des"]
    pass
