from flask import Flask
from flask import request
from flask_cors import CORS
from dnb_res_handler import Dnb_res_handler
from dnb_res_handler import Customer
from mock import mock_single_month
import ast
import json
import os
from taggun.taggun import *

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
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
    print(customer)
    mock_data = mock_single_month()
    trans_bruks = dnb.get_transactions(customer.brukskonto, customer.token, "2018-03-09", "2019-03-08")
    # for trans in trans_bruks:
        # print(trans)
    
    
    
    json_object = {}
    json_object["customerName"] = customer.name
    json_object["konto"] = customer.brukskonto
    json_object["token"] = customer.token
    return json.dumps(mock_single_month())

def func():
    pass


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
        res['data'].append({'item' : d['item'], 'price' : d['price']})
        item_count -= 1
    
    return json.dumps(res)


# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s', request.headers)
#     app.logger.debug('Body: %s', request.get_data(as_text=True))



if __name__ == "__main__":
    # main()
    app.run(host="localhost", debug=True)