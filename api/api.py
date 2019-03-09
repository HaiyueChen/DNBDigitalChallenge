from flask import Flask
from flask import request
from flask_cors import CORS
from dnb_res_handler import Dnb_res_handler
from dnb_res_handler import Customer
from mock import mock_single_month
import json

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
    trans_bruks = dnb.get_transactions(customer.brukskonto, customer.token, "2018-09-01", "2018-11-20")
    
    for trans in trans_bruks:
        print(trans)
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
        
        
        # "Mat og drikke", "Bil og transport","Bolig og fritidsbolig","Ferige og fritid", "Sparing","Øvrige utgifter","Ikke kategorisert"
    
    
    
    json_object = {}
    json_object["customerName"] = customer.name
    json_object["konto"] = customer.brukskonto
    json_object["token"] = customer.token
    return json.dumps(mock_data)

def func():
    pass


@app.route('/parseImg', methods=['POST'])
def parseImg():
    if request.method == 'POST':
        print(request.body)

    return "Success"




if __name__ == "__main__":
    # main()
    app.run(host="localhost", debug=True)