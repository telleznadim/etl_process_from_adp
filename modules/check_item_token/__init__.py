import json
import time
from dotenv import dotenv_values
import requests
from datetime import datetime
import os

# Get the absolute path of the current script
script_path = os.path.abspath(__file__)
# Get the directory containing the current script
base_path = os.path.dirname(script_path)

main_script_path_location = os.path.dirname(os.path.dirname(base_path))

config = dotenv_values(
    f"{main_script_path_location}/.env")

current_script_directory = os.path.dirname(os.path.abspath(__file__))
print(current_script_directory)


def oauth_post_requests_client_credentials(region):
    CLIENT_ID = config[f'{region}_adp_api_client_id']
    CLIENT_SECRET = config[f'{region}_adp_api_client_secret']
    TOKEN_URL = config[f'{region}_adp_api_access_token_url']
    SCOPE = config[f'{region}_adp_api_scope']
    print(
        f"Retreiving Token from API")
    response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            "scope": SCOPE
        }
    )
    response_dict = response.json()
    print(response_dict)
    # logger.debug((response_dict["access_token"])
    # print((response_dict["access_token"]))

    return (response_dict)


def oauth_post_requests_client_credentials_ssl(region):
    CLIENT_ID = config[f'{region}_adp_api_client_id']
    CLIENT_SECRET = config[f'{region}_adp_api_client_secret']
    TOKEN_URL = config[f'{region}_adp_api_access_token_url']
    SCOPE = config[f'{region}_adp_api_scope']

    # Your certificate + key
    # '/path/to/client_cert.pem'
    CLIENT_CERT = config[f'{region}_adp_client_cert']
    # '/path/to/client_key.key'
    CLIENT_KEY = config[f'{region}_adp_client_key']

    print("Retrieving Token from API")

    response = requests.post(
        TOKEN_URL,
        data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': SCOPE
        },
        cert=(CLIENT_CERT, CLIENT_KEY),  # 🔑 provide cert + key
        verify=True  # or path to ADP’s CA if they gave you one
    )

    response.raise_for_status()
    response_dict = response.json()

    print(response_dict)

    return response_dict


def load_tokens():
    try:
        with open(os.path.join(current_script_directory, 'files', 'tokens.json'), 'r') as file:
            tokens = json.load(file)
        return tokens
    except Exception as e:
        print(str(e))
        return {}


def load_active_token(region):
    try:
        with open(os.path.join(current_script_directory, 'files', 'tokens.json'), 'r') as file:
            tokens = json.load(file)
        return tokens[f"{region}_active_token"]
    except Exception as e:
        print(str(e))
        return {}


def save_tokens(tokens):
    with open(os.path.join(current_script_directory, 'files', 'tokens.json'), 'w') as file:
        json.dump(tokens, file, indent=2)


def add_token(region, token_info):
    print("Adding new token to the JSON db")
    tokens = load_tokens()

    # Extract the expiration time from the token_info
    expires_in_seconds = token_info.get('expires_in', 0)
    # Stablishing a long expiring date since the token does not change
    # expires_in_seconds = token_info.get('expires_in', (3 * 31536000))
    print(token_info)

    # Get the current time in seconds since the epoch
    current_time = int(time.time())

    # Calculate the expiration time by adding expires_in to the current time
    expiration_time = current_time + expires_in_seconds

    # Add the token information to the tokens dictionary
    tokens[f"{region}_active_token"] = {
        'token_type': token_info.get('token_type', ''),
        'expires_in': expires_in_seconds,
        'expiration_time': expiration_time,
        'access_token': token_info['access_token']
    }

    # Save the updated tokens to the file
    save_tokens(tokens)


def check_token_status(region):
    print("Checking token status from JSON db")
    active_token = load_active_token(region)

    # Check if the token already exists
    if active_token:
        print("Active token present")
        print("Checking if token expired")
        if active_token['expiration_time'] < int(time.time()):
            print("Token Expired")
            # new_token = request_new_token()
            new_token = oauth_post_requests_client_credentials_ssl(region)
            add_token(region, new_token)
        else:
            print("Token has not expired yet")
            formatted_datetime = datetime.fromtimestamp(
                active_token["expiration_time"]).strftime('%Y-%m-%d %H:%M:%S')
            print(f'Expiration time: {formatted_datetime}')
    else:
        print("No active token")
        # new_token = request_new_token()
        new_token = oauth_post_requests_client_credentials(region)
        add_token(region, new_token)

    print("Loading active token from JSON db")
    active_token = load_active_token(region)
    return (active_token)
