import re
import requests,operator,pandas,glob2
from bs4 import BeautifulSoup
from datetime import datetime
 
from collections import Counter 
import nltk
from konlpy.tag import Twitter
from matplotlib import font_manager, rc
t=Twitter()
font_name = font_manager.FontProperties(fname="C:\Windows\Fonts\malgun.ttf").get_name()
rc('font', family=font_name)
 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import tf_idf
import matplotlib 


def graph(dic):
    dic = sorted(dic.items(), key=lambda t : t[1], reverse = True)

    a_list = []
    b_list = []

    for i in range(0,10):
        a, b = dic[i]
        a_list.append(a)
        b_list.append(b)
    
    print(a_list)
    print(b_list)
    xs = [i + 0.1 for i, _ in enumerate(a_list)]
    
    #matplotlib 라이브러리를 통해 워드크라우드를 이미지 형식으로 보여줌
    plt.bar(xs, b_list)
    plt.ylabel("tf-idf value+1")
    plt.xticks([i for i, _ in enumerate(a_list)], a_list)
    plt.show()
 
 
# 윤년 확인 함수
def yoondal(year):
    year = int(year)
    if year%400 == 0:
        return "29"
    elif year%100 == 0:
        return "28"
    elif year%4 == 0 :
        return "29"
 


# 크롤링한 데이터 분석 함수
def analyze(content):
    # 매게변수로 전달받은 content 를 string 형태로 변경하고
    # 명사형으로 바꾸어 nouns 라는 변수에 저장
    nouns=t.nouns(str(content))

    # 더미데이터 제거
    trash=["조선","연합뉴스","일보","중앙","기자","뉴스","헤럴드경제"]
    for i in trash:
        for j in nouns:
            if i==j:
                nouns.remove(i)

    ko=nltk.Text(nouns,name="분석")

    #ranking이라는 변수를 사전형으로 변경
    ranking=ko.vocab().most_common(100)
    tmpData=dict(ranking)

    print(tmpData)
    

########################################################################################
########################################################################################
########################################################################################    
########################################################################################

 
# crawlingDate
def crawlingDate(date):
 
    l = [] # 리스트 l
 
    # pagecount는 1페이지부터 사용자가 입력한 페이지 수까지 됨
    for pagecount in range(1, 31):
 
        # 동적으로, 사용자가 입력한 날짜와 뉴스 페이지에 접속
        r = requests.get("http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100&date=" + str(date) + "&page=" + str(pagecount))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        all = soup.find_all("li")
 
        for item in all:
            for item2 in item.find_all("dl"):
                d = {} # 사전 d
                try:
                    linkTag = item2.find("dt", {"class": ""}).find("a")
                    d["LinkSrc"] = linkTag['href'] # 사전 d의 LinkSrc라는 키에 href 내용을 가져와 저장
                    d["Title"] = linkTag.text.replace("\t", "").replace("\n", "").replace(",", "").replace('"',"").replace("\r", "")[1:len(linkTag.text) + 1]
                except:
                    d["LinkSrc"] = "None"
                    d["Title"] = "None"
 
                try:
                    contentTag = item2.find("dd")
                    d["Content"] = \
                    contentTag.text.replace("\t", "").replace("\n", "").replace("\r", "").replace(",", "").replace('"',"").split("…")[0]
                    d["Company"] = contentTag.find("span", {"class": "writing"}).text
                    d["Date"] = contentTag.find("span", {"class": "date"}).text
                except:
                    d["Content"] = "None"
                    d["Company"] = "None"
                    d["Date"] = "None"
 
                l.append(d) # 리스트에 사전 추가 / 한 행마다 사전에 추가
 
    df = pandas.DataFrame(l) # pandas 사용 l의 데이터프레임화
    fresh_data = df.drop_duplicates(["Title"], keep ="first")
 
    # now(현재 시각)을 이용해 csv 파일로 저장
    fresh_data.to_csv(date+'.csv',encoding='utf-8-sig', index=False)
    print("Success Get DataFIle and Save Data")
 
 
 
# crawlingMonth
def crawlingMonth(year, month):
 
    # 윤년인지 확인하고 date 결정
    if month == "02":
        date = yoondal(year)
    elif month == "01" or "03" or "05" or "07" or "08" or "10" or "12":
        date = "31"
    elif month == "04" or "06" or "09" or "11":
        date = "30"
 
 
 
    # 십의 자리
    for ten in range(0, 4):
     
        l = [] # 리스트 l
        
        # 일의 자리
        for one in range(0, 10):
 
            if str(ten)+str(one) == "00":
                continue
            else:
                real_date = year+month+str(ten)+str(one)
 
 
            # pagecount는 1페이지부터 사용자가 입력한 페이지 수까지 됨
            for pagecount in range(1, 5):
 
                # 동적으로, 사용자가 입력한 날짜와 뉴스 페이지에 접속
                r = requests.get("http://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=100&date=" + str(real_date) + "&page=" + str(pagecount))
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                all = soup.find_all("li")
 
                for item in all:
                    for item2 in item.find_all("dl"):
                        d = {} # 사전 d
                        try:
                            linkTag = item2.find("dt", {"class": ""}).find("a")
                            d["LinkSrc"] = linkTag['href'] # 사전 d의 LinkSrc라는 키에 href 내용을 가져와 저장
                            d["Title"] = linkTag.text.replace("\t", "").replace("\n", "").replace(",", "").replace('"',"").replace("\r", "")[1:len(linkTag.text) + 1]
                        except:
                            d["LinkSrc"] = "None"
                            d["Title"] = "None"
 
                        try:
                            contentTag = item2.find("dd")
                            d["Content"] = \
                            contentTag.text.replace("\t", "").replace("\n", "").replace("\r", "").replace(",", "").replace('"',"").split("…")[0]
                            d["Company"] = contentTag.find("span", {"class": "writing"}).text
                            d["Date"] = contentTag.find("span", {"class": "date"}).text
                        except:
                            d["Content"] = "None"
                            d["Company"] = "None"
                            d["Date"] = "None"
 
                        l.append(d) # 리스트에 사전 추가 / 한 행마다 사전에 추가
 
        df = pandas.DataFrame(l) # pandas 사용 l의 데이터프레임화
        fresh_data = df.drop_duplicates(["Title"], keep ="first")
 
        fresh_data.to_csv(year+month+"_"+str(ten)+'.csv',encoding='utf-8-sig', index=False)
        print("Success Get DataFIle and Save Data "+str(ten+1))



 
########################################################################################
########################################################################################
########################################################################################    
########################################################################################

 
# newsCrawlingDate 함수
def newsCrawlingDate(linkSrc):
 
    l=[]
    tfidf = []
    only_article = ""
    
    for i in range(0, 140):
        url=requests.get(linkSrc[i])
        c=url.content
        soup=BeautifulSoup(c,"html.parser")
        article=soup.find('div',id="articleBodyContents")
 
        only_article =  re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', "",article.text)
        only_article =  re.sub('[a-zA-Z]', "",only_article)
        only_article =  re.sub('오류를 우회하기 위한 함수 추가','',only_article)
        only_article =  re.sub('연합뉴스', "", only_article)
        l.append(only_article)

    for i, doc in enumerate(tf_idf.tfidfScorer(l)):
        ranking = sorted(doc, key=lambda x: x[1], reverse=True)
        print("[%i] %r ... ranking" % (i, ranking[:20]))
        tfidf.append(ranking)

    new = []        
    for l in tfidf:
        pro = Counter(dict(l))
        new.append(pro)
        
    t = Counter()
    for n in new:
        t = t + n

    dic = dict(t)
    graph(dic)


# newsCrawlingMonth 함수
def newsCrawlingMonth(linkSrc):
    l=[]
    tfidf = []
    only_article = ""
    
    for i in range(0, 30):
        url=requests.get(linkSrc[i])
        c=url.content
        soup=BeautifulSoup(c,"html.parser")
        article=soup.find('div',id="articleBodyContents")
 
        only_article =  re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]', "",article.text)
        only_article =  re.sub('[a-zA-Z]', "",only_article)
        only_article =  re.sub('오류를 우회하기 위한 함수 추가','',only_article)
        only_article =  re.sub('연합뉴스', "", only_article)
        l.append(only_article)

    for i, doc in enumerate(tf_idf.tfidfScorer(l)):
        ranking = sorted(doc, key=lambda x: x[1], reverse=True)
        print("[%i] %r ... ranking" % (i, ranking[:20]))
        tfidf.append(ranking)

    new = []        
    for l in tfidf:
        pro = Counter(dict(l))
        new.append(pro)
        
    t1 = Counter()
    for n in new:
        t1 = t1 + n

    return t1


########################################################################################
########################################################################################
########################################################################################    
########################################################################################




# loadFile 함수
def loadFile(fileName,analyzeValue):
    # checkFileName함수를 호출, 파일이 존재하나 존재하지 않는가 확인
    outputFileName = checkFileName(fileName)
 
    if outputFileName is not -1:
        df = pandas.read_csv(outputFileName)
        linkSrc = df["LinkSrc"]
        content = df["Content"]
        title = df["Title"]
        company = df["Company"]
 
        print("csv FIle Load Success")
 
        if analyzeValue==1:
            newsCrawlingDate(linkSrc)

        elif analyzeValue==2:
            return newsCrawlingMonth(linkSrc)
            
        
        elif analyzeValue==3:
            # analyze(title)
            analyze(content)
 
    else:
        print("Error csv File")
 
 
# checkFileName 함수
# 사용자가 입력한 파일명이 존재하지 않을시 -1 리턴, 존재시 파일명 리턴
def checkFileName(fileName):
 
    # 같은 경로에 csv 파일이 하나도 없다면 -1 리턴
    if len(glob2.glob("*.csv")) == 0:
        print("No file found in this directory")
        return -1
    
    else:
        return fileName
 
 
 
 
# 메인 세팅 함수, 사용자로부터 값을 입력받아 함수를 호출
def mainSetting():
    while (1):
        kb = input("$ ")
        if kb == "exit":
            break
        
        elif kb == "crawlingDate":
            date = input("Enter your date (ex. 20171125) : ")
            crawlingDate(date)
            
        elif kb == "crawlingMonth":
            year = input("Enter your year (ex. 2017) : ")
            month = input("Enter your month (ex. 03) : ")
            crawlingMonth(year, month)
 
        elif kb == "newsCrawlingDate":
            fileName = input("Enter your csv file name (ex. 20171125) : ")
            fileName = fileName +".csv"
            loadFile(fileName,1)
 
        elif kb == "newsCrawlingMonth":
            fileName = input("Enter your csv file name (ex, 201711) : ")
            t=Counter()
            for i in range(0, 4):
                file_Name = fileName
                file_Name = fileName + "_" + str(i) + ".csv"
                t = t + loadFile(file_Name,2)
            
            dic = dict(t)
            graph(dic)
        elif kb=="analyze":
            fileName = input("Enter your csv file name : ")
            loadFile(fileName,3)
 
        else:
            print("command error")
 
 
 
 
mainSetting()
