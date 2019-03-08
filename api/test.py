import os
import requests
import urllib
import json
# from dotenv import load_dotenv

from aws_signing import AwsSigningV4
from request_handler import RequestHandler

client_id = "AKIAJW7CVZK4CSPEQDCQ"
client_secret = "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"
api_key = "dd1f980813db45518d97b00cb551f2c7"

def main():
    openbanking_endpoint = "https://developer-api-sandbox.dnb.no"

    aws_signing_v4 = AwsSigningV4(
        aws_access_key_id=client_id,
        aws_secret_access_key=client_secret,
        aws_host="developer-api-sandbox.dnb.no",
        aws_region="eu-west-1",
        aws_service="execute-api",
    )
    request_handler = RequestHandler(
        endpoint=openbanking_endpoint,
        aws_signing_v4=aws_signing_v4,
        api_key=api_key
    )

    api_token_params = {"customerId": '{"type":"SSN", "value":"29105573083"}'}
    api_token_path = "/token"
    api_token_response = request_handler.get_request(
        path=api_token_path, params=api_token_params
    )
    api_token = api_token_response.json()["tokenInfo"][0]["jwtToken"]
    print("api_token: " + api_token)





if __name__ == "__main__" :
    main()