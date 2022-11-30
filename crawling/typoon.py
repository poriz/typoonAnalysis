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
driver = webdriver.Chrome(options=option, executable_path='./chromedriver.exe')

#로딩
url = 'https://data.kma.go.kr/data/typhoonData/typInfoTYList.do?pgmNo=689'
driver.get(url)
driver.implicitly_wait(time_to_wait=5)




selectIndex = Select(driver.find_element_by_xpath('//*[@id="typNameLst"]'))
year=['2012']
data = []

for y in year:
    Select(driver.find_element_by_class_name('slt')).select_by_value(value=y)

#12년도~22년도 갯수 286개.
    for indexc in range(286):
        if indexc==0:
            print('1장')
            pass
        else:
            sleep(2)
            Select(driver.find_element_by_xpath('//*[@id="typNameLst"]')).select_by_index(indexc)

            print('{dd} 다음장'.format(dd=indexc))

            driver.find_element_by_xpath('//*[@id="schForm"]/div[2]/button').click()

            print([e.text for e in driver.find_elements_by_xpath('//*[@id="wrap_content"]/div[4]/div[2]/div/table/tbody/tr[1]')][0])
            data.append([e.text for e in driver.find_elements_by_xpath('//*[@id="wrap_content"]/div[4]/div[2]/div/table/tbody/tr[1]')][0])


df = pd.DataFrame(columns = ['Time','latitude','longitude','CentalPressure','maxwindSpeed(m/s)','maxwindSpeed(km/h)',
                           'windRadius','strength','size','direction','speed'])


names = ((driver.find_element_by_xpath('//*[@id="typNameLst"]')).text).split('\n')
p_names = []
for n in names:
    p_names.append(n.lstrip())
p_names.pop(0)

for line in data:
    etcData = line[21:]
    sp = etcData.split()

    df2 = pd.DataFrame({'Time':line[:12], 'latitude':sp[0],'longitude': sp[1],'CentalPressure': sp[2],
                       'maxwindSpeed(m/s)':sp[3],'maxwindSpeed(km/h)': sp[4],'windRadius': sp[5],
                       'strength':sp[6],'size': sp[7],'direction':sp[8],'speed':sp[9]},index =[0])
    print(df2)
    df = pd.concat([df,df2],axis=0)


df_x = pd.DataFrame()
df_x['names'] = p_names


#저장
df.to_csv('./result.csv',encoding="utf-8-sig")

