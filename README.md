# zccli
A CLI App to fetch tickets from Zendesk API

## Instructions
Run `pip` to install dependencies
```
$ pip3 install -r requirements.txt
```
Create `config.json` file in the project root. Add `/token` to use API token instead of passwords.
```
{
    "subdomain": "{zcc-subdomain-name}",
    "username": "{username}[/token]",
    "password": "{password|api-token}"
}
```
Run the CLI App by running and follow the prompts
```
$ python3 zccli.py
```