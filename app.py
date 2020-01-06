＃！/ usr / bin / python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import time
import random

app = Flask(__name__)


def validation_digit(name, val):
    error_msg = ''
    if not val:
        error_msg = f'{name}を入力してください。'
    return error_msg

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        res = {}
        res['username'] = request.form.get('username', '')
        res['password'] = request.form.get('password', '')
        res['good_time'] = int(request.form.get('good_time'))
        res['good_max'] = int(request.form.get('good_max'))
        res['goods_time'] = int(request.form.get('goods_time'))
        
        res['error_username'] = validation_digit('ユーザーネーム', res['username'])
        res['error_password'] = validation_digit('パスワード', res['password'])

        driver = webdriver.Chrome('static/chromedriver')

        def login():
            driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
            time.sleep(random.randint(2, 5))
            
            #usernameとpasswordを入力
            driver.find_element_by_name('username').send_keys(res['username'])
            time.sleep(random.randint(2, 5))
            driver.find_element_by_name('password').send_keys(res['password'])
            time.sleep(random.randint(2, 5))

            #ログインボタンを押す
            driver.find_element_by_class_name('L3NKy       ').click()
            time.sleep(random.randint(2, 5))

        def tagsearch(tag):
            instaurl = 'https://www.instagram.com/explore/tags/'
            driver.get(instaurl + tag)
            time.sleep(random.randint(2, 10))
            time.sleep(2)

        def clicknice():
            target = driver.find_elements_by_class_name('_9AhH0')[10]
            actions = ActionChains(driver)
            actions.move_to_element(target)
            actions.perform()
            time.sleep(random.randint(res['good_time']-2, res['good_time']+2))

            try:
                driver.find_elements_by_class_name('_9AhH0')[9].click()
                time.sleep(random.randint(res['good_time']-2, res['good_time']+2))
                driver.find_element_by_class_name('fr66n').click()
                time.sleep(random.randint(res['good_time']-2, res['good_time']+2))

            except WebDriverException:
                f = open('insta.txt','a')
                f.write("エラーが発生しました\n")
                f.close()
                return

            for i in range(random.randint(res['good_max']-5, res['good_max']-2)):
                try:
                    driver.find_element_by_class_name('coreSpriteRightPaginationArrow').click()
                    time.sleep(random.randint(res['good_time']-2, res['good_time']+2))

                except WebDriverException:
                    f = open('insta.txt','a')
                    f.write("２つ目の位置でエラーが発生しました\n")
                    f.close()
                    time.sleep(5)

                try:
                    driver.find_element_by_class_name('fr66n').click()
                    time.sleep(random.randint(res['good_time']-2, res['good_time']+2))
                    
                except WebDriverException:
                    f = open('insta.txt','a')
                    f.write("3つ目の位置でエラーが発生しました\n")
                    f.close()

        if not res['error_username'] and not res['error_password']:
            
            taglist = request.form.getlist('hashtag')
            a = 0

            while True:
                if taglist[a] != '':
                    login()
                    tagsearch(taglist[a])
                    clicknice()

                    driver.close()
                    res['now_time'] = datetime.now()

                    return render_template('index.html', res=res)
                
                else:
                    f = open('insta.txt','a')
                    f.write("リストでエラーが発生しました\n")
                    f.close()
                    break

                a = random.randint(0, len(taglist)-1)
                time.sleep(res['goods_time'] * 60)

    else:
        return render_template('index.html')
    
