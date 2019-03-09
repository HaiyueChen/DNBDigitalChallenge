import numpy as np
import json
import urllib

categ = ["Mat og drikke", "Bil og transport","Bolig og fritidsbolig","Ferige og fritid",  "Sparing","Øvrige utgifter","Ikke kategorisert"]
amounts = [6000.00, 3200.00, 15000.00, 2000.00, 0.00, 2000.00, 100.00]

def mock_transport(total_sum):
    children = []
    ids = ["Billån", "Verksted og vedlikehold", "Bompenger og perkerings avgifter", "Offentlig transport", "Diverse bil transport"]
    billan = (total_sum-1000.0-800.0)
    sum = [billan, 0.0, 1000.0, 800.0, 0.0]

    for i in range(len(ids)):
        cat = {}
        cat["id"] = ids[i]
        cat["sum"] = sum[i]
        cat["children"] = []
        children.append(cat)
    return children


def mock_data(ids, total_sum):
    months = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun","Jul","Aug", "Sep", "Okt","Nov","Des"]
    data = {}

    v = 0
    for month in months:
        categories = []
        for i in range(len(ids)):
            cat = {}
            cat['id'] = ids[i]
            cat['sum'] = total_sum[i]
            if ids[i] == "Bil og transport":
                print("Bil")
                cat["children"] = mock_transport(total_sum[i])
            else:
                cat['children'] = []
                categories.append(cat)
                data[month] = {"categories": categories}

    return data

mock_data(categ, amounts)
# print(mock_data(categ, amounts))

# data = {
#     "categories": [{
#         "id": "Mat og drikke",
#         "sum": 0.00,
#         "children": {}},
#         {"id": "Bil og transport",
#         "sum": 0.00,
#         "children": [{
#                 "id": "Bil lan",
#                 "sum": 0.00
#             },
#             {
#                 "id": "Verksted og vedlikehold",
#                 "sum": 0.00
#             },
#             {
#                 "id": "bompenger og parkerings avgifter",
#                 "sum": 0.00
#             },
#             {
#                 "id": "Offentlig transport",
#                 "sum": 0.00
#             },
#             {
#                 "id": "Diverse bil transport",
#                 "sum": 0.00
#             },
#         ],
#         {"id": "Bolig og fritidsbolig",
#         "sum": 0.00,
#         "children": {}},
#         {"id": "Ferige og fritid",
#         "sum": 0.00,
#         "children": {}},
#         {"id": "Sparing",
#         "sum": 0.00,
#         "children": {}},
#         {"id": "Øvrige utgifter",
#         "sum": 0.00,
#         "children": {}},
#         {"id": "Ikke kategorisert",
#         "sum": 0.00,
#         "children": {}},
#     ],
#
# }
#
# with open('consumption.json') as json_file:
#     data json.load(json_file)
