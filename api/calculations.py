from mock import mock_normal_consumption
import numpy as np

def calculate_saving(data, totalAmount=1000.0, date="2019-03-10"):
    print("\n\n",totalAmount, date, "\n\n")

    possible_saving, spending, acumulated_saving = calculate_possible_savings(data, totalAmount, date)
    print(possible_saving, "\n\n", spending , "\n\n", acumulated_saving)

    return possible_saving


def calculate_possible_savings(data, totalAmount, date):
    normal_consumption = mock_normal_consumption()
    categories = data["children"]

    normal_spending_categories = normal_consumption["children"]
    spending = total_consumption(data)
    acumulated_saving = 0.0
    savingGoal = totalAmount

    possible_saving = []

    for i in range(len(categories)):
        category = categories[i]
        for j in range(len(normal_spending_categories)):
            normal = normal_spending_categories[j]
            if category["name"] == normal["name"]:
                saved, habbits = compare_spending_habits(category["name"], normal, category, savingGoal)
                acumulated_saving += saved
                savingGoal -= saved
                possible_saving.append(habbits)

    return possible_saving, spending, acumulated_saving

def compare_spending_habits(category_name, normal_spending, customer_spending, savingGoal):
    possible_saving = {}
    children = []
    normal_children = normal_spending["children"]
    customer_children = customer_spending["children"]

    acumulated_saving = 0.0

    # send in more data so it is possible to check if it has children
    # if it has children just compare the size

    if savingGoal <= acumulated_saving:
        possible_saving["size"] = 0.0
    elif customer_children:
        for i in range(len(customer_children)):
            cat = {}
            value = 0.0
            for j in range(len(normal_children)):

                if "COLA" in customer_children[i]["name"].upper() :
                    cat["name"] = customer_children[i]["name"]
                    value = round(customer_children[i]["size"]-normal_children[j]["size"], 2)
                    cat["size"] = value
                    acumulated_saving += value
                    children.append(cat)
                    break
                elif customer_children[i]["name"] == "Kjøtt":
                    cat["name"] = customer_children[i]["name"]

                    if customer_children[i]["size"] > normal_children[j]["size"]:
                        value = round(customer_children[i]["size"]-normal_children[j]["size"], 2)
                    if customer_children[i]["size"] < 500.0:
                        pass
                    elif customer_children[i]["size"] > normal_children[j]["size"]:
                        if value >= savingGoal-acumulated_saving:
                            value = savingGoal-acumulated_saving
                        cat["size"] = value
                        acumulated_saving += value
                    cat["size"] = value
                    acumulated_saving += value
                    children.append(cat)
                    break
                elif customer_children[i]["name"] == "Smågodt":
                    cat["name"] = customer_children[i]["name"]
                    value = round(customer_children[i]["size"]-normal_children[j]["size"], 2)

                    if customer_children[i]["size"] > normal_children[j]["size"]:
                        if value < savingGoal and value >= 100.0:
                            pass
                    cat["size"] = value
                    acumulated_saving += value
                    children.append(cat)
                    break
                elif customer_children[i]["name"] == normal_children[j]["name"]:
                    cat["name"] = customer_children[i]["name"]
                    value = round(customer_children[i]["size"]-normal_children[j]["size"], 2)
                    if acumulated_saving >= savingGoal:
                        cat["size"] = 0.0
                    elif customer_children[i]["size"] > normal_children[j]["size"]:
                        if value < savingGoal and value < 500.0:
                            pass
                        if value >= savingGoal-acumulated_saving:
                            value = savingGoal-acumulated_saving
                        cat["size"] = value
                        acumulated_saving += value
                    else:
                        cat["size"] = 0.0
                    children.append(cat)
                    break
    else:
        if normal_spending["size"] < customer_spending["size"]:
            value = round(customer_spending["size"]-normal_spending["size"], 2)
            if value >= savingGoal-acumulated_saving:
                value = savingGoal-acumulated_saving
            possible_saving["size"] = value
            acumulated_saving += value
        else:
            possible_saving["size"] = 0.0

    possible_saving["name"] = category_name
    possible_saving["children"] = children
    return acumulated_saving, possible_saving

def compare_children():
    pass

def total_consumption(data):
    spendings = 0.0
    categories = data["children"]

    for i in range(len(categories)):
        category = categories[i]
        if category["children"]:
            sub_category = category["children"]
            for j in range(len(sub_category)):
                spendings += sub_category[j]["size"]
        else:
            spendings += category["size"]

    spendings = round(spendings, 2)
    return spendings
