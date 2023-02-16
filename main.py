import pandas as pd
import numpy as np
import wget
from selenium import webdriver
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.by import By
from tqdm import tqdm
from tqdm import tqdm_notebook
import re
from time import sleep
import time
import zipfile
import requests
import io
import os
from bs4 import BeautifulSoup

def setChromeDriver():
    # get the latest chrome driver version number
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text

    # build the donwload url
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"

    # download the zip file using the url built above
    latest_driver_zip = wget.download(download_url, 'chromedriver.zip')

    # extract the zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())  # you can specify the destination folder path here
    # delete the zip file downloaded above
    os.remove(latest_driver_zip)

def login(id, pw, nicknames):
    setChromeDriver()
    driver = webdriver.Chrome(os.getcwd() + 'chromedriver.exe')
    driver.get("https://www.instagram.com/")
    time.sleep(10)
    login_form = driver.find_element(By.TAG_NAME, "form")
    inputs = login_form.find_elements(By.TAG_NAME, "input")
    inputs[0].send_keys(id)
    inputs[1].send_keys(pw)
    login_btn = login_form.find_elements(By.TAG_NAME, "button")[1]
    login_btn.click()
    time.sleep(10)
    for i in nicknames :
        crawling(driver, i)

def crawling(driver, accountName):
    driver.get("https://www.instagram.com/" + accountName + '/')
    time.sleep(10)
    imgs = driver.find_elements(By.TAG_NAME, "img")
    print(imgs)


if __name__ == '__main__':
    USER_ID = input("로그인할 ID 를 입력하세요.")
    USER_PW = input("로그인할 PW 를 입력하세요.")
    USER_ACCOUNTS = input("검색할 계정명을 입력하세요")
    USER_ACCOUNTS = USER_ACCOUNTS.split(',')
    login(USER_ID, USER_PW, USER_ACCOUNTS)

