from flask import Flask
from flask import request
from flask_cors import CORS
from dnb_res_handler import Dnb_res_handler
from dnb_res_handler import Customer
from mock import mock_single_month

from calculations import calculate_saving

import json
import os
from taggun.taggun import *

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    if not os.path.isfile("./temp.json"):
        dnb = Dnb_res_handler("AKIAJW7CVZK4CSPEQDCQ", "95/vyM0ZmymXKJZ27D/Yi1j0GtS5VVMfgxuqhqv9", "dd1f980813db45518d97b00cb551f2c7", "https://developer-api-sandbox.dnb.no")
        all_customers = dnb.get_customers()
        customer = Customer(all_customers[2]["customerName"], all_customers[2]["ssn"])
        jwt_res = dnb.get_customer_token(customer.ssn)
        customer.token = jwt_res["jwtToken"]
        customer.public_id = jwt_res["customerPublicId"]
        #############################################
        # customer.set_account(dnb.get_accounts(customer.token))
        ## hard code due to performance issues
        customer.brukskonto = "12060035404"
        customer.sparekonto = "12038763721"
        #######################################3######
        #print(customer)
        mock_data = mock_single_month()
        trans_bruks = dnb.get_transactions(customer.brukskonto, customer.token, "2018-09-01", "2018-11-20")

        for trans in trans_bruks:
            # print(trans)
            if ("Spar" in trans["description"]
                or "Coop" in trans["description"]
                or "Kiwi" in trans["description"]
                or "Rema" in trans["description"]
                or "Bunnpris" in trans["description"]
                or "Meny" in trans["description"]):
                for cat in mock_data["children"]:
                    if cat["name"] == "Mat og drikke":
                        for under_cat in cat["children"]:
                            if under_cat["name"] == "Diverse":
                                under_cat["size"] += abs(float(trans["amount"])) / 3
                                break
            elif ("HBO" in trans["description"]
                    or "Olivia" in trans["description"]
                    or "Kondomeriet" in trans["description"]):
                for cat in mock_data["children"]:
                    if cat["name"] == "Ferige og fritid":
                        cat["size"] = abs(float(trans["amount"]))
                        break
            elif ("Bohus" in trans["description"]):
                for cat in mock_data["children"]:
                    if cat["name"] == "Ikke kategorisert":
                        #print(cat["size"])
                        if("size" not in cat):
                            cat["size"] = 0
                        cat["size"] = abs(float(trans["amount"]))
                        break
            elif ("Rentebetalinger" in trans["description"]
                    or "Avtalegiro" in trans["description"]):
                for cat in mock_data["children"]:
                    if cat["name"] == "Faste utgifter":
                        if "size" not in cat:
                            cat["size"] = 0.0
                        cat["size"] += abs(float(trans["amount"])) / 3

        json_object = {}
        json_object["customerName"] = customer.name
        json_object["konto"] = customer.brukskonto
        json_object["token"] = customer.token
        json_string = json.dumps(mock_data)
        # write to file
        f = open("temp.json", "w")
        f.write(json_string)
        f.close()
        return json_string

    else:
        f = open("temp.json")
        data = json.load(f)
        f.close()
        return json.dumps(data)

@app.route('/saving', methods=['GET'])
def calc_savings():
    if os.path.isfile("./temp.json"):
        f = open("temp.json")
        data = json.load(f)
        return str(calculate_saving(data))
    else:
        return "Error"


@app.route('/parseImg', methods=['POST'])
def parseImg():
    data = request.get_data()


    filepath = 'taggun/kvittering.jpg'
    item_count = 3

    if os.path.exists(filepath):
        os.remove(filepath)
    f = open(filepath, 'wb')
    f.write(data)
    f.close()


    try:
        data = get_image_data(filepath, item_count+1)
    except Exception as e:
        return {'success' : False, 'description' : str(e)}


    res = {'success' : True, 'data' : []}

    for d in data['data']:
        if item_count <= 0:
            break
        res['data'].append({'item' : d['item'], 'size' : d['price']})
        item_count -= 1

    return json.dumps(res)


def add_mat_og_drikke(d, json_data):
    for children in json_data['children']:
        if 'name' in children and children['name'].lower() == 'mat og drikke':
            for child in children['children']:
                if 'name' in child and child['name'].lower() == 'diverse':
                    d["size"] = d["size"] * 10
                    child['size'] -= d['size']
                    children['children'].append({'name' : d['item'], 'size' : d['size']})

@app.route('/saveJson', methods=['POST'])
def saveJson():
    data = request.get_data()
    data = json.loads(data)
    print(data)

    if not os.path.isfile("./temp.json"):
        return json.dumps({'success' : False, 'description' : 'Unable to find temp.json'})    

    f = open("temp.json")
    json_data = json.load(f)
    

    for d in data:
        print("sdfsdfdsf", d)
        if('item' in d and 'cola' in d['item'].lower()):
            add_mat_og_drikke(d, json_data)
                            
        if('item' in d and 'plommer' in d['item'].lower()):
            add_mat_og_drikke(d, json_data)

        if('item' in d and 'mellombar' in d['item'].lower()):
            add_mat_og_drikke(d, json_data)

    os.remove("./temp.json")
    f = open("temp.json", "w")
    f.write(json.dumps(json_data))
    f.close()

    return json.dumps({'success' : True})

# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s', request.headers)
#     app.logger.debug('Body: %s', request.get_data(as_text=True))



if __name__ == "__main__":
    if os.path.isfile("./temp.json"):

        os.remove("./temp.json")
    app.run(host="localhost", debug=True)
