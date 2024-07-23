from functions import download, get_info, get_json
from colorama import Fore
from typing import Any
import sys


def _download(user_name: str, repo_name: str):
    try:
        FILE: str = download(f"{user_name}", f"{repo_name}")
        print(FILE)

    # If The API returns 404 or not the wanted information we can not access the information we want like `user_name`
    # Therefore python throes a KeyError which indicates that there is a typo
    except KeyError:
        print(Fore.RED + "Oops, There is a problem maybe try later or correct your typo !" + Fore.RESET)


def _get_info(user_name: str) -> None:
    JSON: Any = get_json(user_name)
    INFO: dict[str, str] = get_info(JSON)

    for i in INFO:
        formatted_i: str = str(i)
        print(Fore.MAGENTA + ("-" * 25) + formatted_i + ("-" * 25))
        print(Fore.YELLOW + 'Description : ' + Fore.CYAN + INFO[i]["Description"])
        print(Fore.YELLOW + 'Created At : ' + Fore.CYAN + INFO[i]["Created At"])
        print(Fore.YELLOW + 'Updated At : ' + Fore.CYAN + INFO[i]["Updated At"])
        print(Fore.YELLOW + 'Language(s) : ' + Fore.CYAN + INFO[i]["Language(s)"])
        print(Fore.YELLOW + 'Html link : ' + Fore.CYAN + INFO[i]["Html link"])
        print(Fore.YELLOW + 'Owner url : ' + Fore.CYAN + INFO[i]["Owner url"])


def main():
    # Getting the arguments after `python __init__.py` in the terminal
    ARGUMENTS: list[str] = sys.argv

    print(Fore.LIGHTCYAN_EX + " -- COMMAND LINE GITHUB REPOSITORY TOOL -- ")
    print(" -- Switch to the application's folder to get started")
    print(
        ' -- Type ' + Fore.YELLOW + 'python main.py -download "<USER NAME>" "<REPO NAME>" ' + Fore.LIGHTCYAN_EX + 'to clone or download a repository')
    print(
        f' -- Type ' + Fore.YELLOW + 'python main.py -getInfo "<USER NAME>" ' + Fore.LIGHTCYAN_EX + 'to get information about a all repositories for a user')

    for i in range(len(ARGUMENTS)):
        match ARGUMENTS[i]:

            case "-download":
                USER_NAME: str = str(ARGUMENTS[i + 1])
                REPO_NAME: str = str(ARGUMENTS[i + 2])

                _download(USER_NAME, REPO_NAME)

            case "-getInfo":
                USER_NAME: str = str(ARGUMENTS[i + 1])

                _get_info(USER_NAME)


if __name__ == "__main__":
    main()
