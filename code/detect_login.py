import time
import requests
import socket
import webbrowser

from bs4 import BeautifulSoup
from bs4.element import Comment
from termcolor import colored

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'a']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(soup):
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def match_print(url, title, certainty):
    print(f'\n{url}' + title)
    print(colored(
        f'     [*] Detection: {certainty}', 'green'))
    print(colored(
        f'     [*] IP Address of Site: {socket.gethostbyname(url)}', 'green'))
    print(colored(
        f"     [*] Login detected", 'green'))


def detect_login(urls, uTimeout, screenshot, open):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    driver = uc.Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(uTimeout)

    matches = {"results": []}

    for url in urls:
        try:
            driver.get("https://" + url)
            time.sleep(1)
            page_source = driver.page_source
        except Exception as e:
            print(e)
            continue
        soup = BeautifulSoup(page_source, "html.parser")

        match = soup.find_all("input", type="password")
        webpage_text = text_from_html(soup).lower()
        try:
            title = ' | ' + soup.find('title').get_text().replace('\n', ' ')
        except AttributeError:
            title = ''

        if len(match) > 0:
            # If the match was detected via a literal password attribute HTML field
            match_print(
                url, title, 'Password field detected (Higher accuracy)')
            matches["results"].append({"subdomain": url, "pub_login": True})
            if screenshot == True:
                driver.get_screenshot_as_file('screenshots/'+url+'.png')
            if open == True:
                webbrowser.open('https://'+url)

        elif len(match) == 0:
            # If the match was detected via one of the below keywords in the HTML (less accurate)
            if 'sign in' in webpage_text or 'login' in webpage_text or 'log in' in webpage_text:
                match_print(url, title, 'Matched keyword (Lower accuracy)')
                matches["results"].append(
                    {"subdomain": url, "pub_login": True})
                if screenshot == True:
                    driver.get_screenshot_as_file('screenshots/'+url+'.png')
                if open == True:
                    webbrowser.open('https://'+url)

        else:
            print(colored('\n'+url + title) +
                  colored("\n     [*] No login detected", 'red'))

            matches["results"].append({"subdomain": url, "pub_login": False})

    driver.quit()

    return matches
