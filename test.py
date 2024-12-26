import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
import time
import urllib.parse
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

keywords = ['dreamcatcher gahyeon','gahyeon of dreamcatcher','nightmare era gahyeon dreamcatcher','dystopia era gahyeon dreamcatcher','apocalypse era gahyeon dreamcatcher']
file_prefix = 'gahyeon'
target_folder = 'gahyeon'

img_urls = []
for keyword in keywords:
    url = 'https://www.bing.com/images/search?q='+urllib.parse.quote(keyword)

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight;"):
            break

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img', {'class': 'mimg'})

    # print(len(img_tags))
    # print(img_tags[0].attrs['asd'])
    # exit()
    for img in img_tags:
        if 'src' in img.attrs:
            img_urls.append(img['src'])
        elif 'data-src' in img.attrs:
            img_urls.append(img['data-src'])

curr_idx_foto = 1
for idx,url in enumerate(img_urls):
    response = requests.get(url)
    fotoname = file_prefix + '-' + str(curr_idx_foto) + '.jpg'

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    open(target_folder + '/' + fotoname, 'wb').write(response.content)

    img_read = cv2.imread(target_folder + '/' + fotoname)
    gray = cv2.cvtColor(img_read, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        curr_idx_foto += 1
    else:
        os.remove(target_folder + '/' + fotoname)

print('done')