import os
import requests
import urllib
import json

from aws_signing import AwsSigningV4
from request_handler import RequestHandler


class Customer(object):
    def __init__(self, name, ssn):
        self.name = name
        self.ssn = ssn
        self.token = None
        self.public_id = None
        self.brukskonto = None
        self.sparekonto = None


    def sett_konto(self, kontolist):
        for konto in kontolist:
            if konto["productName"] == "BRUKSKONTO":
                self.brukskonto = konto["accountNumber"]
            elif konto["productName"] == "SPAREKONTO":
                self.sparekonto = konto["accountNumber"]

    def __str__(self):
        return "%s\nssn: %s\ntoken: %s\npubID: %s\nbrukskonto: %s\nsparekonto: %s" % (self.name, self.ssn, self.token, self.public_id, self.brukskonto, self.sparekonto)


class Dnb_res_handler(object):
    def __init__(self, client_id, client_secret, api_key, endpoint):
        self.endpoint = endpoint

        self.aws_signing_v4 = AwsSigningV4(
            aws_access_key_id=client_id,
            aws_secret_access_key=client_secret,
            aws_host="developer-api-sandbox.dnb.no",
            aws_region="eu-west-1",
            aws_service="execute-api",
        )
        self.request_handler = RequestHandler(
            endpoint=self.endpoint,
            aws_signing_v4=self.aws_signing_v4,
            api_key=api_key
        )
        

    def get_customers(self):
        all_customer_path = "/testCustomers"
        all_customer_res = self.request_handler.get_request(
            path=all_customer_path, params={}
        )
        all_customers = all_customer_res.json() 

        return all_customers["customers"]

    def get_customer_token(self, ssn):
        value = "{\"type\":\"SSN\", \"value\":\"%s\"}" % ssn
        token_params = {"customerId": value}    
        token_path = "/token"
        customer_token_res = self.request_handler.get_request(
            path=token_path, params=token_params
        )

        token = customer_token_res.json()
        return token["tokenInfo"][0]
    
    def get_accounts(self, token):
        all_accounts_path = "/accounts"
        all_accounts_res = self.request_handler.get_request(
            path=all_accounts_path, params={}, api_token=token
        )
        all_accounts = all_accounts_res.json() 

        return all_accounts["accounts"]

    def get_transactions(self, accountNumber, token, from_date, to_date):
        transactions_path = "/transactions/%s" % accountNumber
        time_interval = {"fromDate" : from_date, "toDate" : to_date}
        print(time_interval)
        
        all_transactions_res = self.request_handler.get_request(
            path=transactions_path, params=time_interval, api_token=token
        )
        # print(all_transactions_res)
        all_transactions = all_transactions_res.json()["transactions"]
        out_going = []
        for trans in all_transactions:
            trans.pop("externalReference")
            trans.pop("textLines")
            trans.pop("details")  
            trans.pop("bookingDate")
            trans.pop("valueDate")
            trans.pop("accountNumber")
        for trans in all_transactions:
            if(trans["amount"] < 0):
                out_going.append(trans)

        return out_going


if __name__ == "__main__":
    dnb = Dnb_res_handler("AKIAJW7CVZK4CSPEQDCQ", "95/vyM0ZmymXKJZ27D/Yi1j0GtS5VVMfgxuqhqv9", "dd1f980813db45518d97b00cb551f2c7", "https://developer-api-sandbox.dnb.no")
    all_customers = dnb.get_customers()

    all_info = all_customers
    customer = Customer(all_info[2]["customerName"], all_info[2]["ssn"])

    jwt_res = dnb.get_customer_token(customer.ssn)
    customer.token = jwt_res["jwtToken"]
    customer.public_id = jwt_res["customerPublicId"]
    customer.sett_konto(dnb.get_accounts(customer.token))
    trans_bruks = dnb.get_transactions(customer.brukskonto, customer.token, "2018-03-09", "2019-03-08")
    for trans in trans_bruks:
        print(trans)
