from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

# 알림창 끄기
option = Options()
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 1
})
driver = webdriver.Chrome(options=option, executable_path='D:/학교/4-2/데사/크롤링/chromedriver.exe')

#로딩
url = 'https://data.kma.go.kr/data/typhoonData/typInfoTYList.do?pgmNo=689'
driver.get(url)
driver.implicitly_wait(time_to_wait=5)

selectIndex = Select(driver.find_element_by_xpath('//*[@id="typNameLst"]'))
year=['2012','2012']
data = []
#,'2013','2014','2015','2016','2017','2018','2019','2020','2021','2022'


p_names = []
df_x = pd.DataFrame()
df_y = pd.DataFrame()
count = 0

for y in year:
    if count == 1:
        if y =='2012':
            driver.implicitly_wait(time_to_wait=5)
            Select(driver.find_element_by_class_name('slt')).select_by_value(value=y)
            names = ((driver.find_element_by_xpath('//*[@id="typNameLst"]')).text).split('\n')
            print(names)

            for n in names:
                p_names.append(n.lstrip())
            df_x['names'] = p_names[1:]
    else:
        Select(driver.find_element_by_class_name('slt')).select_by_value(value=y)
        names = ((driver.find_element_by_xpath('//*[@id="typNameLst"]')).text).split('\n')
        count = 1
print(df_x)

df_x.to_csv('D:/학교/4-2/데사/크롤링/names.csv',encoding="utf-8-sig")
