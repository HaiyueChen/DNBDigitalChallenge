import requests
import json
import ast
import sys

url = 'https://api.taggun.io/api/receipt/v1/verbose/file'

headers = {'apikey': '17ef0120425a11e9bba4c5572eb43161'}

def log_e(errormsg):
    sys.stderr.write(str(errormsg))



def get_image_data(filename, item_count):
    """
    Takes filepath and amount of items bought on receipt as argument
    Returns dictionary with content:
    {
        'success': True/False,
        'description : 'status-message',
        
        'data' : [
            {
                'item' : 'item description',
                'price' : price of item
            },
            {
                'item' : 'item description',
                'price' : price of item
            }, 
            ...
        ]
    }
    """
    for tries in range(10):
        res = parse_receipt(filename, item_count)
        if res['success']:
            return res
        log_e(res['description'])
    raise Exception('Taggun API error')

def parse_receipt(filename, item_count):
    files = {
        'file': (
            filename, # set a filename for the file
            open(filename, 'rb'), # the actual file
            'image/jpg'
        ), # content-type for the file

    # other optional parameters for Taggun API (eg: incognito, refresh, ipAddress, language)
        'incognito': (
            None, #set filename to none for optional parameters
            'false'
        ) #value for the parameters
    }

    try:
        response = requests.post(url, files=files, headers=headers)
        new_str = response.content.decode('utf-8') # Decode using the utf-8 encoding
        data = ast.literal_eval(new_str)

        res = {'success' : True, 'description' : 'Data successfully parsed', 'data': []}
        for data in data['lineAmounts']:
            if item_count <= 0:
                break
            res['data'].append({'item' : data['description'], 'price' : data['data']})
            item_count -= 1
        res['description'] = 'Unable to get given amount of data'
        return res
    except Exception as e:
        return {'success': False, 'description' : str(e)}

if __name__ == "__main__":
    filename = 'kvittering.jpg'
    item_count = 3
    try:
        print(get_image_data(filename, item_count))
    except Exception as e:
        log_e(e)