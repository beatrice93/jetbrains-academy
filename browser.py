"""
Text-based browser.
Reads HTML page, writes it to a file with links highlighted in blue.
Learning objectives:
 - Handling user input;
 - HTTP requests;
 - Reading and writing files in Python;
 - Web scraping basics with BeautifulSoup;
Suggested improvements/bug fixes:
 - Get rid of strings only constituted of whitespace;
 - Fix tab names (there could be some conflicts/bugs);
 - Return error codes 
"""


import os
import sys
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore, init
init()


def format_url(url):
    """
    Check whether url (a string) is a valid url and prepend "https://"
    if needed.
    """
    if "." in url:
        if url.startswith('https://'):
            return url
        else:
            return 'https://' + url
    else:
        return False


def display_page(url, open_tabs, folder):
    """
    Checks whether the page is cached; if it is, print it.
    If not, cache it and print it. In both cases, return the tab name.
    """
    if url in open_tabs:
        with open(folder + '\\' + url, 'r') as tab:
            print(tab.read())
        return url
    elif format_url(url):
        try:
            requests.get(format_url(url))
        except requests.exceptions.ConnectionError:
            return False
        else:
            name = write_tab(url, open_tabs, folder)
            with open(folder + '\\' + name, 'r') as tab:
                print(tab.read())
            return name
    else:
        return False


def write_tab(url, open_tabs, folder):
    """
    Write the page to a file; add its name and url to the list of open tabs.
    Note: I wrote the links in CYAN because BLUE is illegible on my terminal.
    Returns the name of the new tab.
    """
    url = format_url(url)
    r = requests.get(url)
    name = ''.join(url.split('https://')[1].split('.')[:-1])  # remove 'https://' and '.com'
    open_tabs.add(name)
    open_tabs.add(url)

    soup = BeautifulSoup(r.content, 'html.parser')
    links = soup.find_all(name="a")
    for link_ in links:
        link_.replace_with(Fore.CYAN + link_.text + Fore.RESET)  # this mutates the soup object
    with open(folder + '\\' + name, 'w', encoding='utf-8') as tab:
        tab.write(soup.get_text())

    return name


def main():
    arguments = sys.argv
    folder = arguments[1]
    try:
        # Create target Directory
        os.mkdir(folder)
        print("Directory", folder, "created.")
    except FileExistsError:
        print("Directory", folder, "already exists")

    open_tabs = set()
    history = deque()
    current_page = False
    while True:
        input_ = input()
        previous_page = current_page
        current_page = display_page(input_, open_tabs, folder)  # False if not a valid url/open tab
        if not current_page:
            if input_ == 'back':
                if len(history) != 0:
                    display_page(history.pop(), open_tabs, folder)
            elif input_ == 'exit':
                break
            else:
                print("Error: did you enter a valid URL?")
        if previous_page:
            history.append(previous_page)


main()
