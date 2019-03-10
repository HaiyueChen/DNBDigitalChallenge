from mock import mock_normal_consumption
import numpy as np

def calculate_saving(data, totalAmount=1000.0, date="2019-03-10"):

    print("\n\n",totalAmount, date, "\n\n")

    normal_consumption = mock_normal_consumption()
    categories = data["children"]

    normal_spending_categories = normal_consumption["children"]
    spending = total_consumption(data)

    possible_saving = []

    for i in range(len(categories)):
        category = categories[i]
        for j in range(len(normal_spending_categories)):
            normal = normal_spending_categories[j]
            if category["name"] == normal["name"]:
                habbits = compare_spending_habits(category["name"], normal, category)
                possible_saving.append(habbits)
    return possible_saving

def compare_spending_habits(category_name, normal_spending, customer_spending):
    possible_saving = {}
    children = []
    normal_children = normal_spending["children"]
    customer_children = customer_spending["children"]

    print(customer_children)

    # send in more data so it is possible to check if it has children
    # if it has children just compare the size
    if customer_children:
        for i in range(len(customer_children)):
            cat = {}

            for j in range(len(normal_children)):
                if customer_children[i]["name"] == normal_children[j]["name"]:
                    cat["name"] = customer_children[i]["name"]
                    if customer_children[i]["size"] > normal_children[j]["size"]:
                        cat["size"] = abs(round(customer_children[i]["size"]-normal_children[j]["size"], 2))
                    else:
                        cat["size"] = 0.0
                    children.append(cat)
                    break
    else:
        if normal_spending["size"] < customer_spending["size"]:
            possible_saving["size"] =  abs(round(customer_spending["size"]-normal_spending["size"], 2))
        else:
            possible_saving["size"] = 0.0


    possible_saving["name"] = category_name
    possible_saving["children"] = children
    return possible_saving

def compare_children():
    pass

def total_consumption(data):
    spendings = 0.0
    categories = data["children"]

    for i in range(len(categories)):
        category = categories[i]
        if not category["children"]:
            spendings += category["size"]
        else:
            sub_category = category["children"]
            for j in range(len(sub_category)):
                spendings += sub_category[j]["size"]


    return round(spendings, 2)
