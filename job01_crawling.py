# csv file
# column ['title','reviews]

from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

# https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page=1 ~ 37까지
# //*[@id="old_content"]/ul/li[1]/a                   title
# //*[@id="old_content"]/ul/li[2]/a
# //*[@id="old_content"]/ul/li[20]/a
# //*[@id="reviewTab"]/div/div/ul/li[1]/a            review_title
# //*[@id="reviewTab"]/div/div/ul/li[2]/a
# //*[@id="reviewTab"]/div/div/ul/li[10]/a
# //*[@id="pagerTagAnchor1"]                         review page
# //*[@id="pagerTagAnchor2"]

review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'
review_number_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'                   #review button
#                      //*[@id="movieEndTabMenu"]/li[6]/a
for i in range(11, 38): #38
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2020&page={}'.format(i)
    titles = []
    reviews = []
    try:
        for j in range(1, 21):  #21
            driver.get(url)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
            try:
                title = driver.find_element("xpath", movie_title_xpath).text
                driver.find_element("xpath", movie_title_xpath).click()
                time.sleep(0.1)
                driver.find_element('xpath', review_button_xpath).click()
                time.sleep(0.1)
                review_range = driver.find_element('xpath', review_number_xpath).text
                review_range = review_range.replace(',', '')
                review_range = (int(review_range)-1) // 10 + 2
                for k in range(1, review_range): #review_range
                    review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]'.format(k)
                    try:
                        driver.find_element('xpath', review_page_button_xpath).click()
                        for l in range(1, 11): #11
                            review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(l)
                            try:
                                review = driver.find_element('xpath', review_title_xpath).click()
                                back_flag=True
                                time.sleep(0.1)
                                review = driver.find_element('xpath', review_xpath).text
                                titles.append(title)
                                reviews.append(review)
                                driver.back()
                            except:
                                if back_flag:
                                    driver.back()
                                driver.back()
                                print('review', i, j, k, l)
                        driver.back()
                    except:
                        print('review page', i, j, k)
            except:
                print('movie', i, j)
        df=pd.DataFrame({'title':titles, 'reviews':reviews})
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(2020,i), index=False)
    except:
        print('page', i)

driver.close()