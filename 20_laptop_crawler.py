from selenium import webdriver
import cx_Oracle
import csv
import requests
import time
from bs4 import BeautifulSoup
#페이지 딜레이를 위한 라이브러리
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#csv이식을 위한 코드 == 성공

browser = webdriver.Chrome()
#다나와 접속
url = "http://www.danawa.com/?src=adwords&kw=GA0000020&gclid=EAIaIQobChMIspmGg8HJ7AIVwdaWCh0HbgvsEAAYASAAEgLg9vD_BwE"
browser.get(url)

elem = browser.find_element_by_link_text("컴퓨터/노트북/조립PC").click()

time.sleep(1)
browser.find_element_by_class_name("category_all_dot").click()

time.sleep(1)
browser.find_element_by_xpath("//*[@id='categoryExplodeLayer11']/div[1]/div[2]/ul/li[1]/a").click()

time.sleep(2)
soup = BeautifulSoup(browser.page_source, "lxml")

#검색결과와 무관한 ad 광고를 제외한 태그 삭제 
product = soup.find_all("li", attrs = {"class":"prod_item prod_layer"})

time.sleep(2)

cnt = 0
db=cx_Oracle.connect("class13/class13@nullmaster.iptime.org:1521/orcl")
cursor = db.cursor()

for pd in product :
    if(cnt == 10):
        break

    title = pd.find("p", attrs = {"class":"prod_name"}).get_text().replace("\n","").replace("\t","").replace("인기 순위","").strip()
    #해당 페이지 url 추가 생성 -> VO 추가 요망
    spec = pd.find("dl", attrs = {"class":"prod_spec_set"}).get_text().replace("\n","").replace("\t","").replace("상세 스펙","")
    #replace대신 strip만 적어도 가능하다.
    list = spec.split(" / ")

    image_div= pd.find("a", attrs = {"class":"thumb_link"})
    img_url = image_div.select("a.thumb_link > img")[0].get("data-original")
    
    if(img_url != None):

      if img_url.startswith("//"):
        img_url = "https:" + img_url
      
    elif(img_url == None):
      img = pd.find("img")
      img_url = img['src']     
      if img_url.startswith("//"):
        img_url = "https:" + img_url


    LAPTOP_NAME = title
    
    if not (list[4].startswith('i')):
        CPU_NAME = " "+list[4]
    else:
        CPU_NAME = list[4]

    GPU_NAME = "none"#test를 위해 cpu만 추출
    #test는 cpu로만 하고 gpu 외장 그래픽의 index 위치 추출하고,
    #그 다음 인덱스의 값을 그대로 빼오면 pgu_name 값.

    #memory 용량 추출
    memory_matching = [s for s in list if "GB" in s][0]
        
    if memory_matching.find(':') != -1:
        memory_matching=[s for s in list if "GB" in s][1]
    LAPTOP_MEMORY = memory_matching

   


    LAPTOP_OS = list[6][10:len(list[6])] 
    if (len(LAPTOP_OS) > 8):
        LAPTOP_OS = LAPTOP_OS[0:3]
    #print(LAPTOP_OS)#table os 문자열 제한으로 인한 미포함 뒤의 문자열 잘라내기
    #:이후의 글자만 추출

    #모니터 크기 추출
    #   (이후의 문자열 자르기) cm를 표기하려면 해당 index이후로 [:]자르고
    #   소수점을 제외한 인치값을 얻어오기 위해 출력
    start = list[0].find("(")
    #end = list[0].find(".",1) 오류
    LAPTOP_MONITORSIZE = list[0][start+1:(len(list[0])-5)] #인치만 표현한다.
    LAPTOP_IMAGEURL = img_url
    #print(img_url)
    #print("{} {} {} {} {} {} {}".format(LAPTOP_NAME,CPU_NAME,GPU_NAME,LAPTOP_MEMORY,LAPTOP_OS,LAPTOP_MONITORSIZE,LAPTOP_IMAGEURL))
    #출력 테스트 성공

    #항상 5번째 CPU 존재, 항상 7번째 os 존재, 모니터사이즈 항상 첫번째. 이미지 추출 14번째 메모리
    # LAPTOP_NAME
    # CPU_NAME
    # GPU_NAME
    # LAPTOP_MEMORY
    # LAPTOP_OS
    # LAPTOP_MONITORSIZE
    # LAPTOP_IMAGEURL
    



    sql = "insert into laptop (LAPTOP_NAME,CPU_NAME,GPU_NAME,LAPTOP_MEMORY,LAPTOP_OS,LAPTOP_MONITORSIZE,LAPTOP_IMAGEURL) values(:1,:2,:3,:4,:5,:6,:7)"
    data = (LAPTOP_NAME,CPU_NAME,GPU_NAME,LAPTOP_MEMORY,LAPTOP_OS,LAPTOP_MONITORSIZE,LAPTOP_IMAGEURL)
    cursor.execute(sql,data)
    cnt = cnt + 1 #n개 데이터만 빼오기 위함.


db.commit()

# sql = "select * from laptop"
# cursor.execute(sql) #laptopOS의 이름이 너무 길다 maximum:20

# for row in cursor:
#     for i in range(len(row)):

#         print(row[i],end="  ")
#     print("")

cursor.close()
db.close()

#image url이 너무 작다. 수정 완료
#         #if i==3:
#             # if(row[3] != None):
#             #     description = row[3].read()
#위 기록 부분 삭제로 정상 동작

   #해당 페이지 url 추가 생성 -> VO 추가 요망
   #30개 이상 페이지 넘어가는 부분 [0] 인덱스로 구현
   #gpu 추출 부 미구현
   #이미지 url 부분 varchar2 제한 늘려야할 것 같아서 class11 의 테이블 드랍하고 재생성
