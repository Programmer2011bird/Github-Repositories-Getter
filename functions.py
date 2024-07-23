from colorama import Fore
from typing import Any
import requests
import base64
import os

USERS_ENDPOINT: str = "https://api.github.com/users"
REPOS_ENDPOINT: str = "https://api.github.com/repos"


def make_directory(directory_name: str) -> None | str:
    try:
        os.mkdir(f"{directory_name}")

    except FileExistsError:
        return Fore.RED + "File or folder already exists ❌"


def decode_and_write(content: bytes, file_path: str, file_name: str, repository_name: str):
    RAW_CONTENT: bytes = base64.b64decode(content)
    CONTENT: str = RAW_CONTENT.decode('utf-8')

    with open(f'{file_path}', "w+") as file:
        file.write(CONTENT)

        print(Fore.LIGHTBLUE_EX + f"DOWNLOADED THE FILE : {file_name} FROM REPOSITORY {repository_name} ✅")


def get_json(user_name: str) -> Any:
    USER_REPOS_ENDPOINT: str = f"{USERS_ENDPOINT}/{user_name}/repos"

    RESPONSE: requests.Response = requests.request("get", f"{USER_REPOS_ENDPOINT}")
    RESPONSE_JSON: Any = RESPONSE.json()

    return RESPONSE_JSON


def get_info(json_data) -> dict[str, str]:
    INFO: dict[str, str] = {}

    for i in range(len(json_data)):
        OWNER_URL: str = str(json_data[i]['owner']['url'])
        REPO_NAME: str = str(json_data[i]['name'])
        HTML_URL: str = str(json_data[i]['html_url'])
        DESCRIPTION: str = str(json_data[i]['description'])
        CREATED_AT: str = str(json_data[i]['created_at'])
        UPDATED_AT: str = str(json_data[i]['updated_at'])
        LANGUAGE: str = str(json_data[i]['language'])

        INFO.update({
            f"{REPO_NAME}": {
                'Description': DESCRIPTION,
                "Created At": CREATED_AT,
                "Updated At": UPDATED_AT,
                "Language(s)": LANGUAGE,
                "Html link": HTML_URL,
                "Owner url": OWNER_URL
            }
        })

    return INFO


def download(username: str, repository: str) -> str:
    USER_REPOS_ENDPOINT: str = f"{REPOS_ENDPOINT}/{username}/{repository}/contents"

    RESPONSE: requests.Response = requests.request("get", f"{USER_REPOS_ENDPOINT}")
    RESPONSE_JSON: Any = RESPONSE.json()

    make_directory(f"{repository}")

    FILES: list[str] = []
    for i in range(len(RESPONSE_JSON)):
        FILES.append(RESPONSE_JSON[i]['name'])

    for i in FILES:
        FILE_CONTENT_ENDPOINT: str = f"{USER_REPOS_ENDPOINT}/{i}"
        RESPONSE: requests.Response = requests.request("get", f"{FILE_CONTENT_ENDPOINT}")
        RESPONSE_JSON: Any = RESPONSE.json()

        decode_and_write(RESPONSE_JSON["content"], f'{repository}/{i}', i, repository)

    return Fore.GREEN + "FILE(S) DOWNLOADED ✅"
