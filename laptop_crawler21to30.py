#한글 지우고 공백지우고
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

#-심플- -GPU- , -무게- , -가격- , 경로 URL 여러페이지 
browser = webdriver.Chrome()
#다나와 접속
url = "http://prod.danawa.com/list/?cate=112758&logger_kw=ca_main_more"
browser.get(url)
time.sleep(4)
#다음 페이지 클릭
elem = browser.find_element_by_xpath("//*[@id='productListArea']/div[5]/div/a").click()
#다음 페이지 클릭
time.sleep(3)
elem = browser.find_element_by_xpath("//*[@id='productListArea']/div[4]/div/a[2]").click()
time.sleep(2)

#strong_cnt = 3 #인기순위 넘버가 없는 2페이지부터 strong의 1개값 삭감
cnt = 0

cnt_page = 10 #검색할 페이지 수

# //*[@id="productListArea"]/div[4]/div/div/a[1]
# //*[@id="productListArea"]/div[4]/div/div/a[2]
# //*[@id="productListArea"]/div[4]/div/div/a[3]
# //*[@id="productListArea"]/div[4]/div/div/a[4]
# //*[@id="productListArea"]/div[4]/div/div/a[5]
# //*[@id="productListArea"]/div[4]/div/div/a[6]
# //*[@id="productListArea"]/div[4]/div/div/a[7]
# //*[@id="productListArea"]/div[4]/div/div/a[8]
# //*[@id="productListArea"]/div[4]/div/div/a[9]
# //*[@id="productListArea"]/div[4]/div/div/a[10]
# 이후로 동일 

db=cx_Oracle.connect("class13/class13@nullmaster.iptime.org:1521/orcl")
cursor = db.cursor()

for i in range(1,cnt_page+1):
    
    browser.find_element_by_class_name("num")
    # browser.find_element_by_link_text("{}".format(i)).click()

    browser.find_element_by_xpath("//*[@id='productListArea']/div[{}]/div/div/a[{}]".format(4,i)).click()
    
   
    soup = BeautifulSoup(browser.page_source, "lxml")

    #검색결과와 무관한 ad 광고를 제외한 태그 삭제 
    product = soup.find_all("li", attrs = {"class":"prod_item prod_layer"})


    


    for pd in product :
        # if(cnt == 20):
        #     break
        cnt = cnt + 1
        title = pd.find("p", attrs = {"class":"prod_name"}).get_text().replace("\n","").replace("\t","").replace("인기 순위","").strip()
        #해당 페이지 url 추가 생성 -> VO 추가 요망
        spec = pd.find("dl", attrs = {"class":"prod_spec_set"}).get_text().replace("\n","").replace("\t","").replace("상세 스펙","")
        #replace대신 strip만 적어도 가능하다.
        
        price_excep = pd.find("a", attrs = {"title":"관심상품에 담기"}).get_text().strip()
        list = spec.split(" / ")

        image_div= pd.find("a", attrs = {"class":"thumb_link"})
        img_url = image_div.select("a.thumb_link > img")[0].get("data-original")
        
        laptop_url_a = pd.find("div", attrs = {"class":"thumb_image"})
        LAPTOP_URL = laptop_url_a.select("div.thumb_image > a")[0].get("href")
        
        LAPTOP_PRICE = pd.find("p", attrs = {"class":"price_sect"}).get_text().replace(" ","").replace("가격정보 더보기","").replace("원","").replace(",","").replace("가격정보더보기","").replace("일시품절","0").strip()
        #print(laptop_price_a)
        
        #print(LAPTOP_PRICE)
        #가끔 strong이 3번째있어 [4]여야할 때가 있네.
        # price = image_div.select("p.price_sect > strong")[0].get_text()

        if(img_url != None):
            if img_url.startswith("//"):
             img_url = "https:" + img_url
            
        elif(img_url == None):
            img = pd.find("img")
            img_url = img['src'] 
            

        # if img_url.startswith("//"):
        #     img_url = "https:" + img_url
        #     img_url.replace("130:130","500:500")    


        LAPTOP_NAME = title
        
        if not (list[4].startswith('i')):
            CPU_NAME = " "+list[4]
        else:
            CPU_NAME = list[4]

        GPU_NAME = "none"
        if any("외장그래픽" in gpu_word for gpu_word in list):
            GPU_NAME = list[(list.index("외장그래픽"))+1].replace(" ","").replace("라데온","").replace("쿼드로","")
            print(GPU_NAME)
            
                

        # GPU_NAME = "none"#test를 위해 cpu만 추출
        #test는 cpu로만 하고 gpu 외장 그래픽의 index 위치 추출하고,
        #그 다음 인덱스의 값을 그대로 빼오면 pgu_name 값.

        #memory 용량 추출
        memory_matching = [s for s in list if "GB" in s][0]
            
        if memory_matching.find(':') != -1:
            memory_matching=[s for s in list if "GB" in s][1]
        LAPTOP_MEMORY = memory_matching

        LAPTOP_WEIGHT = [lw for lw in list if "무게:" in lw][0].strip().replace("무게:","").replace(".kg","").replace("kg","").replace(",",".")
        if "g" in LAPTOP_WEIGHT:
            LAPTOP_WEIGHT = ("0."+LAPTOP_WEIGHT.replace("g","")).replace(" ","")
        #print(LAPTOP_WEIGHT)

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
        LAPTOP_IMAGEURL = img_url.replace("130:130","500:500")
        #print(img_url)
        #print("{}/{}/{} /{}/ {} / {} / {} / {} / {} / {} / {}".format(cnt,laptop_url,price,LAPTOP_WEIGHT,LAPTOP_NAME,CPU_NAME,GPU_NAME,LAPTOP_MEMORY,LAPTOP_OS,LAPTOP_MONITORSIZE,LAPTOP_IMAGEURL))
        #출력 모두 성공


        #노트북 중복을 없에 즐겨찾기에 저장하기 위해 f_key 포함
        sql = "insert into laptop (laptop_seq,LAPTOP_PRICE,LAPTOP_URL,LAPTOP_WEIGHT,LAPTOP_NAME,CPU_NAME,GPU_NAME,LAPTOP_MEMORY,LAPTOP_OS,LAPTOP_MONITORSIZE,LAPTOP_IMAGEURL) values(laptop_seq.NEXTVAL,:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)"
        data = (LAPTOP_PRICE,LAPTOP_URL,LAPTOP_WEIGHT,LAPTOP_NAME,CPU_NAME,GPU_NAME,LAPTOP_MEMORY,LAPTOP_OS,LAPTOP_MONITORSIZE,LAPTOP_IMAGEURL)
        cursor.execute(sql,data)
        #n개 데이터만 빼오기 위함.


db.commit()
cursor.close()
db.close()