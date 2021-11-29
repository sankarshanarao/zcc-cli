import json
from json.decoder import JSONDecodeError
import requests
from requests import status_codes
from requests.auth import HTTPBasicAuth

url_template = {
    "fetch_all": "https://{}.zendesk.com/api/v2/tickets?page[size]=25",
    "fetch_one": "https://{}.zendesk.com/api/v2/tickets/{}.json"
}

# Get credentials from config.json
def getCredentials():    
    try:
        credFile = open('config.json')
    except FileNotFoundError:
        print('Create \'config.json\' in current working directory in the below format.')
        print(
            '{\n \
                    \"subdomain\": \"[zccsubdomain]\", \n \
                    \"username\": \"[username or username+\'/token\' for token]\", \n \
                    \"password\": \"[password or token]\" \n \
                    } \
        ')
        exit()

    try:
        credJson = json.load(credFile)   
    except json.JSONDecodeError:
        print('Ensure config.json follows the given json schema')
        print(
            '{\n \
                    \"subdomain\": \"[zccsubdomain]\", \n \
                    \"username\": \"[username or username+\'/token\' for token]\", \n \
                    \"password\": \"[password or token]\" \n \
                    } \
        ')
        exit()
    
    try:
        subdomain, username, password = credJson['subdomain'], credJson['username'], credJson['password']
    except KeyError:
        print('Ensure config.json follows the given json schema')
        print(
            '{\n \
                    \"subdomain\": \"[zccsubdomain]\", \n \
                    \"username\": \"[username or username+\'/token\' for token]\", \n \
                    \"password\": \"[password or token]\" \n \
                    } \
        ')
        exit()

    return subdomain, username, password

def reportErrorsAndExit(response):
    if (response.status_code == 401 or response.status_code == 403):
        print('\nCould not authenticate. Check credentials in config.json and try again')
        exit()
    elif (response.status_code == 429):
        print('Too many requests. Try again later.')
        exit()
    elif (response.status_code == 500):
        print('Currently unavailable. Try again later.')
        exit()


def fetchAll():
    subdomain, username, password = getCredentials()

    url = url_template['fetch_all'].format(subdomain)

    response = requests.get(url, auth=(username, password))

    reportErrorsAndExit(response)

    return response.json()


def fetchPage(url):
    subdomain, username, password = getCredentials()

    response = requests.get(url, auth=(username, password))

    reportErrorsAndExit(response)

    return response.json()


def fetchTicket(id):
    subdomain, username, password = getCredentials()

    url = url_template['fetch_one'].format(subdomain, id)

    response = requests.get(url, auth=(username, password))

    reportErrorsAndExit(response)

    return response.json()