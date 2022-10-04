import sys
import requests


test_endpoints = ["personal_access_tokens",
                  "users",
                  # using random file and main
                  "projects/1/repository/files/placeholder?ref=main",
                  # using a random username
                  "projects?sudo=random_user"]

api_levels=[
    "api/read_api",
    "read_user",
    "read_repository",
    "sudo"
            ]


if len(sys.argv) < 3:
    print("Missing Arguments: python3 api_access_check.py [base_url] [api_key]")
    exit()

base_url = sys.argv[1]
token = sys.argv[2]


for i, endpoint in enumerate(test_endpoints):
    url = f'http://{base_url}/api/v4/{endpoint}?private_token={token}'
    ret = requests.get(url, params={'private_token': token})
    try:
        if 'error' in ret.json().keys():
            if 'revoked' in ret.json()['error_description']:
                print('[!] Token was revoked')
                exit()
            continue
    except AttributeError:
        # we might get a list as a result
        pass
    print("[!] API key has permission level:", api_levels[i])
    if i==0:
        print(f"    -> Check the detailed permissions of all keys on: http://{base_url}/api/v4/personal_access_tokens?private_token={token}")



