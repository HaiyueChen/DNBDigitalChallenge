from mock import mock_normal_consumption
import numpy as np

def calculate_saving(data):
    normal_consumption = mock_normal_consumption()
    categories = data["children"]

    normal_spending_categories = normal_consumption["children"]

    spending = total_consumption(data)

    possible_saving = []

    for i in range(len(categories)):
        name = categories[i]["name"]

        for j in range(len(normal_spending_categories)):
            normal = normal_spending_categories[j]
            if name == normal["name"]:
                habbits = compare_spending_habits(name, normal["children"], categories[i]["children"])
                possible_saving.append(habbits)
                break
    print("\n\nPossible saving",possible_saving)
    return possible_saving

def compare_spending_habits(category_name, normal_spending, customer_spending):
    possible_saving = {}
    children = []
    for i in range(len(customer_spending)):
        cat = {}

        for j in range(len(normal_spending)):
            if customer_spending[i]["name"] == normal_spending[j]["name"]:
                cat["name"] = customer_spending[i]["name"]
                if customer_spending[i]["size"] > normal_spending[j]["size"]:
                    print("PRINT DIF",customer_spending[i]["size"], normal_spending[j]["size"])
                    cat["size"] = abs(round(customer_spending[i]["size"]-normal_spending[j]["size"], 2))
                else:
                    cat["size"] = 0.0
                children.append(cat)
                break

    possible_saving["name"] = category_name
    possible_saving["children"] = children
    return possible_saving

def total_consumption(data):
    spendings = 0.0
    categories = data["children"]

    for i in range(len(categories)):
        category = categories[i]

        if not category["children"]:
            print(category["size"])
            spendings += category["size"]
        else:
            pass



    print(category["name"])
    spendings += category["size"]
    print("total spending:",spendings)
    return spendings
