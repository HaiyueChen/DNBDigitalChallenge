import urllib
import requests
import json



class RequestHandler(object):
    def __init__(self, endpoint, aws_signing_v4, api_key):
        self.__endpoint = endpoint
        self.__aws_signing_v4 = aws_signing_v4
        self.api_key = api_key

    def __to_canonical_querystring(self, params):
        canonical_querystring = ""
        # parameters have to be sorted alphabetically for the signing part
        for param_key, param_value in sorted(params.items()):
            
            if canonical_querystring != "":
                canonical_querystring += "&"
            canonical_querystring += param_key + "=" + urllib.parse.quote(param_value)
        return canonical_querystring

    def get_request(self, path, params, api_token=None):
        canonical_querystring = self.__to_canonical_querystring(params)
        headers = self.__aws_signing_v4.headers_for_get_method(
            path, canonical_querystring
        )

        # 'host' header is added automatically by the Python 'requests' library.
        headers["Accept"] = "application/json"
        headers["Content-type"] = "application/json"
        headers["x-api-key"] = self.api_key

        # All endpoints require the API token, except the API token endpoint.
        if api_token:
            headers["x-dnbapi-jwt"] = api_token

        request_url = self.__endpoint + path + "?" + canonical_querystring
        return requests.get(request_url, headers=headers)