import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import os
import shutil
import uuid
import time
from datetime import datetime
import datetime
import requests



class WebDriver(object):

    def __init__(self):
        self.options = Options()

        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')

    def get(self):
        driver = Chrome('/opt/chromedriver', options=self.options)
        return driver



def lambda_handler(event, context):
    crawlerMacbookShoppe()
    return True

def crawlerMacbookShoppe(link = 'https://shopee.vn/apple_flagship_store?page=0&shopCollection=10957665&sortBy=pop'):
    urlHook = 'https://hooks.slack.com/services/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'
    instance_ = WebDriver()
    driver = instance_.get()
    driver.get(link)
    time.sleep(5)
    elements = driver.find_elements_by_xpath('//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[4]/div[2]/div[2]/div[1]/div[2]/div/div')
    for el in elements:
        infor = el.text.split('\n')
        discount = infor[0]
        productName = infor[2]
        price = infor[5]
        textInfor = productName + ' - ' + discount + ' - ' + price
        sendToSlackChannel(textInfor, urlHook)
        print(textInfor)

    sendToSlackChannel('--------------------------------------------------------------------------------------', urlHook)
    driver.close()

def sendToSlackChannel(textSending, urlHook):
    try:
        payload = dict(text=textSending)
        requests.post(urlHook, json=payload)
    except:
        print('err')