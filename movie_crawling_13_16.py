from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime
import requests

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())

# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

url_base = 'https://movie.daum.net/ranking/boxoffice/monthly?date=202309'

df_titles = pd.DataFrame()

for year in range(13, 14):
    if year == 13:
        month_start, month_end = 1, 8
    else:
        month_start, month_end = 1, 12

    for month in range(month_start, month_end + 1):
        month_formatted = '{:02}'.format(month)
        url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20{}{}'.format(year, month_formatted)
        driver.get(url)
        # time.sleep(0.5)   get()가 완전히 사이트를 로드될 때까지 기다리으로 필요없음!

        title = []
        review = []

        for i in range(1, 31):
            try:
                title_element = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(i)).text

                # 영화 제목 클릭
                driver.find_element('xpath',
                                    '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(i)).click()
                if driver.current_url == 'https://movie.daum.net/moviedb/main?movieId=':
                    driver.back()
                    continue    # continue를 사용하여 특정 조건이 충족되었을 때 반복을 건너뛰고 다음 반복 주기로 이동할 수 있습니다.

                # 평점 클릭
                while(1):
                    try:
                        driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[2]/div[1]/div/div/div')
                        break
                    except:
                        continue
                driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span').click()
                time.sleep(0.5)
                # 리뷰 더보기 5번
                for j in range(1, 6):
                    try:
                        driver.find_element('xpath', '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button').click()
                        time.sleep(0.5)
                    except NoSuchElementException:
                        break
                for k in range(1, 161):
                    try:
                        review_element = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(k)).text
                        review_element = re.compile('[^가-힣]').sub(' ', review_element)
                        review.append(review_element)
                        title.append(title_element)
                    except NoSuchElementException:
                        pass
                        # pass는 문법적으로 무언가가 필요하지만 아무 작업을 수행할 필요가 없는 경우에 사용됩니다.
                        # 예를 들어, 함수나 클래스를 정의할 때 구현 내용이 아직 없는 경우에 사용할 수 있습니다.

                driver.back()
                driver.back()

            except:
                print('date_20{}{}_{}'.format(year, month_formatted, i))

        df_data = pd.DataFrame({'title': title, 'review': review})
        df_data.to_csv('C:/Users/wjgk0/PycharmProjects/pythonProject/crawling_data/data_{}_{}.csv'.format(year, month), index=False)

print(title)
print(review)