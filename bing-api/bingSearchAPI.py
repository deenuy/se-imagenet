# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os
from pprint import pprint
import requests
import config

'''
This sample makes a call to the Bing Image Search API with a text query and returns relevant images with data.
Documentation: https: // docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/
'''

# Add your Bing Search V7 subscription key and endpoint to your environment variables
subscriptionKey = config.BING_CUSTOM_SEARCH_SUBSCRIPTION_KEY
endpoint = config.BING_CUSTOM_SEARCH_ENDPOINT
customConfig = config.BING_CUSTOM_CONFIG_ID

# Keyword search parameter
query = "java run time error"

# Construct a request
mkt = 'en-US'
params = {'q': query, 'customConfig': customConfig}
headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}

# Call the API
# curl -H "Ocp-Apim-Subscription-Key: <yourkeygoeshere>" https://api.bing.microsoft.com/v7.0/images/search?q=upgrade+program+java
try:
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()

    print("\nHeaders:\n")
    print(response.headers)

    print("\nJSON Response:\n")
    pprint(response.json())
except Exception as ex:
    raise ex