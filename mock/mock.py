import numpy as np
import json
import urllib


# Use mock_singl_month

categ = ["Mat og drikke", "Bil og transport","Bolig og fritidsbolig","Ferige og fritid", "Sparing","Øvrige utgifter","Ikke kategorisert"]
amounts = [6000.00, 3200.00, 15000.00, 2000.00, 0.00, 2000.00, 100.00]

def mock_transport(total_sum):
    children = []
    ids = ["Billån", "Verksted og vedlikehold", "Bompenger og perkerings avgifter", "Offentlig transport", "Diverse bil transport"]
    billan = (total_sum-1000.0-800.0)
    sum = [billan, 0.0, 1000.0, 800.0, 0.0]

    for i in range(len(ids)):
        cat = {}
        cat["name"] = ids[i]
        cat["size"] = sum[i]
        cat["children"] = []
        children.append(cat)
    return np.sum(sum), children

def mock_mat(total_sum=3000):
    children = []
    ids = ["Kjøtt", "Frukt", "Grønnsaker", "Melkeprodukt", "Smågodt", "Diverse"]
    sum = [total_sum, total_sum-100, total_sum-500.0, total_sum-200.0, total_sum-600.0, total_sum-200.0]

    for i in range(len(ids)):
        cat = {}
        cat["name"] = ids[i]
        cat["size"] = sum[i]
        cat["children"] = []
        children.append(cat)
    return np.sum(sum), children


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
            cat['children'] = []
        categories.append(cat)

    data["name"] = 'categories'
    data['children'] = categories
    return data


def mock_year():
    months = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun","Jul","Aug", "Sep", "Okt","Nov","Des"]
    pass
