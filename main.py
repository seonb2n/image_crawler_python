import base64
import json
import os
import time
import zipfile
from typing import List

import requests
import requests as r
import wget
from selenium import webdriver
from selenium.webdriver.common.by import By

HUGGING_FACE_ACCESS_TONE = ""
ENDPOINT_URL = "https://api-inference.huggingface.co/models/openai/clip-vit-base-patch32"
IMAGE_TAGS = []

def setChromeDriver():
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    version_number = response.text
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"
    latest_driver_zip = wget.download(download_url, 'chromedriver.zip')
    with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
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
    # 게시물 더 보기 버튼 클릭
    buttons = driver.find_elements(By.TAG_NAME, "button")
    if buttons.size > 5 :
        buttons[5].click()
    SCROLL_PAUSE_TIME = 2.0
    # 하단부까지 스크롤링
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    imgs = driver.find_elements(By.TAG_NAME, "img")
    img_list_size = len(imgs)
    for i in range (4, img_list_size-1) :
        img = imgs[i]
        img_src = img.get_attribute("src")
        classify(img_src)


def classify(img) :
    result = ''
    result = predict(img, IMAGE_TAGS)
    if result is not None:
        print(result[0]['label'] + " : " + str(result[0]['score']))


def predict(path_to_image: str = None, candiates: List[str] = None):
    response = requests.get(path_to_image).content
    b64 = base64.b64encode(response)
    # payload = {"inputs": {"image": b64.decode("utf-8"), "candiates": candiates}}
    payload = {"image": b64.decode("utf-8"), "parameters": {"candidate_labels" : candiates}}
    response = r.post(
        ENDPOINT_URL, headers={"Authorization": "Bearer " + HUGGING_FACE_ACCESS_TONE}, json=payload
    )
    if (response.ok) :
        return response.json()
    else :
        print(response)

if __name__ == '__main__':
    secret_file = os.path.join("./", 'secrets.json')
    with (open(secret_file)) as f:
        secrets = json.loads(f.read())

    tag_file = os.path.join("./", "IMAGE_TAG.txt")
    with (open(tag_file)) as f:
        for line in f:
            line = line.strip('\n')
            IMAGE_TAGS.append(line)
    HUGGING_FACE_ACCESS_TONE = secrets['HUGGING_FACE_TOKEN']
    print(">>> HG 토큰 : " + HUGGING_FACE_ACCESS_TONE)
    USER_ID = input("로그인할 ID 를 입력하세요.")
    USER_PW = input("로그인할 PW 를 입력하세요.")
    USER_ACCOUNTS = input("검색할 계정명을 입력하세요")
    USER_ACCOUNTS = USER_ACCOUNTS.split(',')
    login(USER_ID, USER_PW, USER_ACCOUNTS)

