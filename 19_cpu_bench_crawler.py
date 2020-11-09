from selenium import webdriver
import cx_Oracle
import csv
import requests
import time
import re
from bs4 import BeautifulSoup
#페이지 딜레이를 위한 라이브러리
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
#다나와 접속
#url = "https://www.cpubenchmark.net/high_end_cpus.html"
url = "https://www.cpubenchmark.net/mid_range_cpus.html"
#url = "https://www.videocardbenchmark.net/high_end_gpus.html"
#url = "https://www.videocardbenchmark.net/mid_range_gpus.html"

#cpu, gpu high, mid
browser.get(url)
time.sleep(6)

soup = BeautifulSoup(browser.page_source, "lxml")

cpu_li = soup.find_all("li", attrs = {"id":re.compile("^rk")})
#success
#print(cpu_li)

# cnt = 0
db=cx_Oracle.connect("class13/class13@nullmaster.iptime.org:1521/orcl")
cursor = db.cursor()

for cl in cpu_li :
    # if(cnt >= 5):
    #     break

    cpu_name = cl.find("span", attrs = {"class":"prdname"}).get_text().strip()
    cpu_point = cl.find("span", attrs = {"class":"count"}).get_text().replace(",","").strip()

    # print(cpu_name)
    # print(cpu_point)

    sql = "insert into cpu_bench values(:1,:2)"
    data = (cpu_name,cpu_point)
    cursor.execute(sql,data)

    # cnt = cnt+1
    

db.commit()

cursor.close()
db.close()

#cx_Oracle.DatabaseError: ORA-01722: invalid number
#error -> 중간의 ,가 있기에 숫자로 인식하지 못한다.