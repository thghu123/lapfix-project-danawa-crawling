#다나와 상품코드 크롤링
#필요한 패키지 로딩
import time
import requests
from bs4 import BeautifulSoup
import re

def getPcode(page):
    pCodeList = []
    pSpecList = []
    for i in range(1,page+1):
        print(i,"페이지 입니다")
        headers = {
               "Referer" : "http://prod.danawa.com/",
               "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
                }

        params = {"page" : page, "listCategoryCode" : 112758, 
                    "categoryCode" : 206, "physicsCate1":860, 
                  "physicsCate2":869,"physicsCate3":0, "physicsCate4":0, "viewMethod": "LIST", "sortMethod":"BoardCount",
                  "listCount":30, "group": 10, "depth": 2, "brandName":"","makerName":"","searchOptionName":"",
                  "sDiscountProductRate":0, "sInitialPriceDisplay":"N", 
                  "sPowerLinkKeyword":"노트북", "oCurrentCategoryCode":"a:2:{i:1;i:144;i:2;i:206;}", 
                    "innerSearchKeyword":"",
                  "listPackageType":1, "categoryMappingCode":176, "priceUnit":0, "priceUnitValue":0, "priceUnitClass":"",
                  "cmRecommendSort":"N", "cmRecommendSortDefault":"N", "bundleImagePreview":"N", "nPackageLimit":5, 
                  "nPriceUnit":0, "isDpgZoneUICategory": "N", "sProductListApi":"search","priceRangeMinPrice":"","priceRangeMaxPrice":"",
                 "btnAllOptUse":"false"
                
                 }
   


        res = requests.post("http://prod.danawa.com/list/ajax/getProductList.ajax.php", headers = headers, data=params)
        soup = BeautifulSoup(res.text, "html.parser")
        #상세한 페이지에 들어갈 수도 있으니 Productname은 주석
        #a = soup.findAll("a", attrs = {"name":"productName"})
        a = soup.findAll("p", attrs = {"class":"prod_name"})
        spec_a = soup.findAll("div", attrs = {"class":"spec_list"})

        #productName 값을 매번 뽑아 오니까 그때마다 값을 저장하면된다.
        #prod_spec_set
        #prod_name 둘다 겟 텍스트하면 값 추출
        #일단 유저 에이전트 적용하자. url 밑에 headers
        #a1 = soup.find_all("a", attrs={"class":re.compile("^click_log_product_standard_title")})
        #a2 = soup.find_all("a", attrs={"class":re.compile("^spec_list")})

        
        

        for i in range(len(a)):
           
            pCodeList.append(a[i].find("a").get_text().replace("\t","").replace("\n",""))
            print(a[i].find("a").get_text(" ",strip=True).replace("\t","").replace("\n",""))
            
        for i in range(len(spec_a)):
            #pSpecList.append(spec_a[i].find("a").get_text())
            print(spec_a[i].get_text().replace("\t","").replace("\n",""))
            

        #맵구조로 리스트와 이름으로 정리해서 반환하고 세탁기를 노트북으로 변경
     
              
        #a1 = soup.findAll("a", attrs = {"class":"spec_list"})   
        #pCodeList.append(a1[i].get_text())
        #print(a1[i].get_text())

    return pCodeList

    #다나와 리뷰 크롤링

"""def danawaCraw(pcode, page):
    reviewlist = []
    for idx in range(1,page+1):
        headers = {"Referer" : "http://prod.danawa.com/info/?pcode=2703774&cate=102206", "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"}
        params = {"t" : 0.3180507575057596, "prodCode" : pcode, "page" : idx, "limit":10, "score":0,"usefullScore":"Y", "_":1550639162598}

        res = requests.get("http://prod.danawa.com/info/dpg/ajax/companyProductReview.ajax.php?t=0.3180507575057596&prodCode=2703774&page=1&limit=10&score=0&sortType=&usefullScore=Y&_=1550639162598", headers = headers, params = params)
        soup = BeautifulSoup(res.text, "html.parser")
        #divs = soup.find_all("div", attrs = {"style":"display:none;"})
        divs = soup.find_all("div", attrs = {"class":"items"})
        
        print(idx,'페이지에서', len(divs),'개의 리뷰 크롤링완료')
        
        for i in range(len(divs)):
            reviewlist.append(" ".join(divs[i].text.split()))
        print('리스트에 리뷰 넣기 완료')
    return reviewlist

"""

#걸리는 시간 측정
start_time = time.time() 

#리뷰가 담길 리스트 생성
TotalReview = []

#가져온 상품코드를 사용해서 해당 리뷰 크롤링하기
"""for p in getPcode(1): #괄호안에 원하는 상품페이지 수 입력 (1페이지당 상품 30개)
    TotalReview.append(danawaCraw(p,1)) # 괄호안 순자에 원하는 리뷰 페이지 수 입력
"""

TotalReview = getPcode(1)

#최종으로 걸리는 시간 파악
print("--- %s seconds ---" %(time.time() - start_time))

print(TotalReview)
