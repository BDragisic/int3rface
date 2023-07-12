import sys
import requests
import time

from bs4 import BeautifulSoup
from termcolor import colored

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


def check_alive(to_check):
    try:
        web_response = requests.get(to_check,timeout=1)
        return True
    except:
        return False

def crawl_site(url,uTimeout):
    
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    driver = uc.Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(uTimeout)

    try:
        driver.get("https://" + url)
        time.sleep(1)
        page_source = driver.page_source
    except Exception as e:
        print(e)
        return 
    soup = BeautifulSoup(page_source, "html.parser")

    matches = soup.find_all("a")
    driver.quit()
    
    internal_links = []
    for link in matches:
        href_link = link.get('href')
        if href_link:
            href_link = href_link.replace('https://','')
            if href_link != '/' or href_link != url:
                if '#' not in href_link or '?' not in href_link:
                    if href_link[0] == '/':
                        internal_links.append(url+href_link)
                    elif url in link:
                        internal_links.append(href_link)
                        
                    
    return internal_links
    
    