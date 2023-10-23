from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = ChromeOptions()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
# chrome driver
driver = webdriver.Chrome(service=service, options=options)  # <- options로 변경

titles = []
reviews = []

df_save = pd.DataFrame(columns=['titles', 'reviews'])

for year in range(17, 21): # 년도 넣기

    for month in range(1, 13): # 월 넣기
        if month < 10:
            url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20{}0{}'.format(year, month)
        else:
            url = 'https://movie.daum.net/ranking/boxoffice/monthly?date=20{}{}'.format(year, month)
        driver.get(url)
        time.sleep(0.5)

        for page in range(1, 31): # 월 당 페이지 수
            try:
                title_element = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/ol/li[{}]/div/div[2]/strong/a'.format(page))
                title = title_element.text # 영화 제목의 xpath, text 옵션으로 저장
                titles.append(title) # titles 변수에 영화 제목 저장
                title_element.click() # 영화 제목 클릭함
                time.sleep(0.5)

                rating = driver.find_element('xpath', '//*[@id="mainContent"]/div/div[2]/div[1]/ul/li[4]/a/span')
                # 영화 평점 변수
                rating.click() # 영화 평점 클릭
                time.sleep(0.5)
            except:
                print("페이지 에러_{}_{}_{}".format(year, month, page))

            for x in range(0, 5): # 더보기 클릭 5번
                try:
                    more = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="alex-area"]/div/div/div/div[3]/div[1]/button')))
                    more.click()
                except:
                    print("더보기 에러_{}_{}_{}".format(year, month, title))

            for rv in range(1, 161): # 리뷰 갯수
                try:
                    review_element = driver.find_element('xpath', '/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{}]/div/p'.format(rv))
                    review = review_element.text
                    review = re.compile('[^가-힣|a-z|A-Z|0-9]').sub(' ', review)
                    time.sleep(0.2)
                    reviews.append(review)
                except:
                    print('리뷰 에러 20{}_{}_{}_{}'.format(year, month, page, rv))

            driver.back()
            # time.sleep(5)
            driver.back()
            # time.sleep(5)

            df_review = pd.DataFrame(reviews, columns=['reviews'])

            df_review['titles'] = titles[page - 1]
            df_save = pd.concat([df_save, df_review], axis='rows')
            df_save.to_csv('./crawling_data/movie_{}_{}.csv'.format(month, page), index=False)

        df_save.to_csv('./crawling_data/movie_{}_{}.csv'.format(year, month), index=False)
    df_save.to_csv('./crawling_data/movie_20{}.csv'.format(year), index=False)
driver.close()