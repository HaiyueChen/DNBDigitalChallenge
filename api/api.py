from flask import Flask
from flask import request
from flask_cors import CORS
from dnb_res_handler import Dnb_res_handler
from dnb_res_handler import Customer
import json

app = Flask(__name__)
CORS(app)

def main():
    dnb = Dnb_res_handler("AKIAJW7CVZK4CSPEQDCQ", "95/vyM0ZmymXKJZ27D/Yi1j0GtS5VVMfgxuqhqv9", "dd1f980813db45518d97b00cb551f2c7", "https://developer-api-sandbox.dnb.no")
    all_customers = dnb.get_customers()

    all_info = all_customers
    customer = Customer(all_info[2]["customerName"], all_info[2]["ssn"])

    jwt_res = dnb.get_customer_token(customer.ssn)
    customer.token = jwt_res["jwtToken"]
    customer.public_id = jwt_res["customerPublicId"]
    customer.sett_konto(dnb.get_accounts(customer.token))
    print(customer)

    trans_bruks = dnb.get_transactions(customer.brukskonto, customer.token, "2018-08-01", "2018-08-02")
    print(trans_bruks)



@app.route('/', methods=['GET'])
def index():
    dnb = Dnb_res_handler("AKIAJW7CVZK4CSPEQDCQ", "95/vyM0ZmymXKJZ27D/Yi1j0GtS5VVMfgxuqhqv9", "dd1f980813db45518d97b00cb551f2c7", "https://developer-api-sandbox.dnb.no")
    all_customers = dnb.get_customers()
    customer = Customer(all_customers[2]["customerName"], all_customers[2]["ssn"])
    jwt_res = dnb.get_customer_token(customer.ssn)
    customer.token = jwt_res["jwtToken"]
    customer.public_id = jwt_res["customerPublicId"]
    customer.sett_konto(dnb.get_accounts(customer.token))
    trans_bruks = dnb.get_transactions(customer.brukskonto, customer.token, "2018-03-09", "2019-03-08")
    for trans in trans_bruks:
        print(trans)
    
    json_object = {}
    json_object["customerName"] = customer.name
    json_object["konto"] = customer.brukskonto
    json_object["token"] = customer.token

    return json.dumps(json_object)

def func():
    pass




if __name__ == "__main__":
    # main()
    app.run(host="localhost", debug=True)