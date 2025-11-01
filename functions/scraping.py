import requests
import json
import pandas as pd
import re

# Algolia credentials
algolia_app_id = "NGFIBXY77H"
algolia_api_key = "c98fc1c21abf20589ad1a6417343f3e2"

# API endpoint
url = f"https://{algolia_app_id.lower()}-dsn.algolia.net/1/indexes/*/queries"

# Headers
headers = {
    "X-Algolia-API-Key": algolia_api_key,
    "X-Algolia-Application-Id": algolia_app_id,
    "Content-Type": "application/json"
}
# 
# Request body - this is what defines your search
payload = {
    "requests": [
        {
            "indexName": "prod_marketItem_nl_relevance", 
            "params": "query=&hitsPerPage=100&page=0"  # Adjust search parameters
        }
    ]
}

# Make the POST request
response = requests.post(url, headers=headers, json=payload)
response_dict = response.json()
items_dict = response_dict['results'][0]['hits']

print(f"Status Code: {response.status_code}")
print(type(items_dict))

items = pd.json_normalize(items_dict, sep='_')

# keep only some columns

items = items[['createdAt', 'updatedAt', 'metadata_size', 'metadata_color', 'metadata_brand', 'metadata_type', 'metadata_condition', 'favouriteCount', 'price_NL_amount', 'firstOfferedAt_NL']]

items['firstOfferedAt_NL'] = pd.to_datetime(items['firstOfferedAt_NL'], unit='ms')
#manually rename some edge case columns
items = items.rename(columns={'price_NL_amount': 'price_nl_amount', 'firstOfferedAt_NL': 'first_offered_at_nl'})

def to_snake_case(name):
    # Remove metadata_ prefix
    name = name.replace('metadata_', '')
    # Replace spaces and hyphens with underscores
    name = re.sub(r'[-\s]+', '_', name)
    # Insert underscore before capital letters (for camelCase), but not if already has underscore
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    # Remove multiple consecutive underscores
    name = re.sub(r'_+', '_', name)
    return name

items.columns = [to_snake_case(col) for col in items.columns]
print(items)