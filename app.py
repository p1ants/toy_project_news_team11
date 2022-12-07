from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://toyNews:toyNews@cluster0.opg0fml.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta


import requests
from bs4 import BeautifulSoup

# 정치 완료
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

politics = soup.select('#main_content > div > div._persist > div:nth-child(1) > div')
db.politics.delete_many({})
for politic in politics:
    if politic != None:
        politicsTitle= politic.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a').text
        politicsLink= politic.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a')['href']
        politicsImage= politic.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div > a')
        politicsDesc = politic.select_one ('div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_lede').text
        
        if politicsImage != None:
           politics_image = politicsImage.img['src']
        else:
            politics_image ="1"
           
        
        doc = {
            'politics_title':politicsTitle,
            'politics_link':politicsLink,
            'politics_image':politics_image,
            'politics_desc':politicsDesc
            }
        
        db.politics.insert_one(doc)
# 경제 완료
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

economys = soup.select('#main_content > div > div._persist > div:nth-child(1) > div')
db.economy.delete_many({})
for economy in economys:
    economyTitle = economy.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a')
    if economyTitle is not None:
        title = economyTitle.text
        link = economyTitle['href']
        lede = economy.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_lede').text.strip()
        if economy.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div > a') != None:
            economy_image = economy.select_one('div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div > a').img['src']
        else:
            economy_image =""    
        # alt = economy.select_one('dl > dt.photo > a').img['alt']

        doc = {
            'economy_title': title,
            'economy_link': link,
            'economy_desc': lede,
            'economy_image':economy_image,
            }
        
        db.economy.insert_one(doc)

        



# 세계완료
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=104&sid2=322', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

gloBals = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li')
db.gloBals.delete_many({})
for gloBal in gloBals:
    gloBalTitle = gloBal.select_one('dl > dt:nth-child(2) > a')
    if gloBalTitle is not None:
        gloBaltitle = gloBalTitle.text.strip()
        gloBalLink = gloBalTitle['href']
        gloBallede = gloBal.select_one('dl > dd > span.lede').text.strip()
        gloBalthumbnail = gloBal.select_one('dl > dt.photo > a')
        if gloBalthumbnail != None:
            gloBalimage = gloBalthumbnail.img['src']
        else:
            gloBalimage ='1'

        doc = {
            'gloBal_title': gloBaltitle,
            'gloBal_link':gloBalLink,
            'gloBal_desc': gloBallede,
            'gloBal_image':gloBalimage,
            
        }

        
        db.gloBals.insert_one(doc)


# 문화 완료

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)


soup = BeautifulSoup(data.text, 'html.parser')

culture = soup.select('#main_content > div > div._persist > div:nth-child(1) > div')
news_list= []
db.culture.delete_many({})
for report in culture:
    r = report.select_one('div.cluster_body > ul > li')
    if r is not None:
        title = r.select_one('div.cluster_text > a').text
        link = r.select_one('div.cluster_text > a')['href']
        if r.select_one('div.cluster_thumb > div > a') is not None:
            image = r.select_one('div.cluster_thumb > div > a').img['src']
        else:
            image = ""
        lede = r.select_one('div.cluster_text > div.cluster_text_lede').text

        doc = {
                "culture_title":title,
                "culture_link":link,    
                "culture_image":image,
                "culture_desc":lede
        }
        
        db.culture.insert_one(doc)

# 테크 완료
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

tech = soup.select('#main_content > div > div._persist > div:nth-child(1) > div')

db.tech.delete_many({})
for report in tech:

    r = report.select_one('div.cluster_body > ul > li')
    if report is not None:
        tech_title = r.select_one('div.cluster_text > a').text
        tech_link = r.select_one('div.cluster_text > a')['href']
        image = r.select_one('div.cluster_thumb > div > a')
        if image != None:
            tech_image = image.img['src']
        else:
            tech_image ='1'   
        
        tech_lede = r.select_one('div.cluster_text > div.cluster_text_lede').text
    
        
        doc = {
                'tech_title':tech_title,
                'tech_link':tech_link,
                'tech_image':tech_image,
                'tech_desc':tech_lede
        }
        
        db.tech.insert_one(doc)

@app.route('/')
def home():
    return render_template('index.html')

# 정치 get방식
@app.route("/politics", methods=["GET"])
def politics_get():
    politicsList = list(db.politics.find({},{'_id':False}))
    
    return jsonify({'politicsList':politicsList})

# 경제 get방식
@app.route("/economy", methods=["GET"])
def economy_get():
    economyList = list(db.economy.find({},{'_id':False}))
    
    return jsonify({'economyList':economyList})

# 세계 get방식
@app.route("/gloBals", methods=["GET"])
def gloBal_get():
    gloBalList = list(db.gloBals.find({},{'_id':False}))
    
    return jsonify({'gloBalList':gloBalList})

# 문화 get방식
@app.route("/culture", methods=["GET"])
def culture_get():
    cultureList = list(db.culture.find({},{'_id':False}))
    
    return jsonify({'cultureList':cultureList})

# 테크 get방식
@app.route("/tech", methods=["GET"])
def tech_get():
    techList = list(db.tech.find({},{'_id':False}))

    return jsonify({'techList':techList})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
    
    


# 이미지
# main_content > div > div._persist > div:nth-child(1) > div:nth-child(1) > div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div > a
# main_content > div > div._persist > div:nth-child(1) > div:nth-child(2) > div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div > a
# 타이틀
# main_content > div > div._persist > div:nth-child(1) > div:nth-child(1) > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a
# main_content > div > div._persist > div:nth-child(1) > div:nth-child(2) > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a

# 내용
# main_content > div > div._persist > div:nth-child(1) > div:nth-child(1) > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_lede
# main_content > div > div._persist > div:nth-child(1) > div:nth-child(2) > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_lede

