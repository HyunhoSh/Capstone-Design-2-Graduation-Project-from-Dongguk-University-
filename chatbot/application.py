        

from flask import Flask, request, jsonify, json
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import urllib.request
import random
from PIL import Image
import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY
from config import BUCKET_NAME
import pymysql

app = Flask(__name__)

mysql = MySQL(app)


global lan
global calories_n
global carbohydrate_n
global protein_n
global fat_n
global sodium_n
global calcium_n
global vitamin_c_n
global saturated_fat_n

calories_n = []
carbohydrate_n = []
protein_n = []
fat_n = []
sodium_n = []
calcium_n = []
vitamin_c_n = []
saturated_fat_n = []

global foodstr  # AI로 인식된 음식 리스트
global foodgl
global foodglcp
global num_diet
global num_solution
global diet_food 
global meal_date
global selection
global diet_food_img

diet_food_img = []
diet_food = []
foodgl=[]
num_diet = random.randrange(0, 1000)
num_solution = random.randrange(0, 1000)

app.config['MYSQL_USER'] = 'hihi'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'userdb'
app.config['MYSQL_HOST'] = 'localhost'
app.secret_key = "ABfdgfdg"

mysql.init_app(app)


global img_food_used
img_food_used = []


def s3_connection():
    s3 = boto3.client('s3',aws_access_key_id = AWS_ACCESS_KEY, aws_secret_access_key = AWS_SECRET_KEY)
    return s3;

s3 = s3_connection()

@app.route('/foodimage', methods=['POST'])
def foodimage():
    req = request.get_json()

    params = req['userRequest']['utterance']

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query='+'단백질이풍부한음식'
    print(url)

    headers = {"Authorization": ""} # confidential
    result = json.loads(str(requests.get(url, headers=headers).text))

    print(result)
    search_url = []
    title = []
    if len(result['documents']) > 0:
        for data in result['documents']:
            title.append(data['place_name'])
            search_url.append('https://map.kakao.com/link/to/{}'.format(data['id']))

        title.insert(0, '🗺 클릭시 카카오맵 길찾기로 연결됩니다.')
        search_url.insert(0, '')
    else:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색이 불가한 지역입니다."
                        }
                    }
                ]
            }
        }
        return jsonify(res)

    listItems = []

    cnt = 0
    if len(title) >= 5:
        items = 6
    else:
        items = len(title)

    for i in range(items):
        if cnt == 0:
            itemtype = 'title'
        else:
            itemtype = 'item'

        listItems.append({
                "type": itemtype,               # 카드 리스트의 아이템 티입
                "title": title[i],              # 제목
                "linkUrl": {
                  "type": "OS",
                          "webUrl": search_url[i]
                    }
                 })
        cnt += 1

    res = {
          "contents": [
            {
              "type": "card.list",
              "cards": [
                {
                  "listItems": listItems
                }
              ]
            }
          ]
         }

    # 전송
    return jsonify(res)


@app.route('/locsearch', methods=['POST'])
def locsearch():
    req = request.get_json()

    params = req['action']['detailParams']

    keyword = params['sys_location']['value']

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query='+keyword+'병원'
    print(url)

    headers = {"Authorization": ""} # confidential
    result = json.loads(str(requests.get(url, headers=headers).text))

    print(result)
    search_url = []
    title = []
    if len(result['documents']) > 0:
        for data in result['documents']:
            title.append(data['place_name'])
            search_url.append('https://map.kakao.com/link/to/{}'.format(data['id']))

        title.insert(0, '🗺 클릭시 카카오맵 길찾기로 연결됩니다.')
        search_url.insert(0, '')
    else:
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "검색이 불가한 지역입니다."
                        }
                    }
                ]
            }
        }
        return jsonify(res)

    listItems = []

    cnt = 0
    if len(title) >= 5:
        items = 6
    else:
        items = len(title)

    for i in range(items):
        if cnt == 0:
            itemtype = 'title'
        else:
            itemtype = 'item'

        listItems.append({
                "type": itemtype,               # 카드 리스트의 아이템 티입
                "title": title[i],              # 제목
                "linkUrl": {
                  "type": "OS",
                          "webUrl": search_url[i]
                    }
                 })
        cnt += 1

    res = {
          "contents": [
            {
              "type": "card.list",
              "cards": [
                {
                  "listItems": listItems
                }
              ]
            }
          ]
         }

    # 전송
    return jsonify(res)


@app.route("/calories", methods=["GET", "POST"])
def calorie():
    
    req = request.get_json()
    print(req)

    select = req["action"]["detailParams"]["선택지"]["origin"]
    print(select)
    
    conn = mysql.connect
    cur = conn.cursor()

    sql = "select * from Nutrient where food_name = '%s'" % (foods)
       
    cur.execute(sql)
    # conn.commit()
    nutrient = cur.fetchall()
    print(nutrient)
        
    cur.close()
    conn.close()
    
    
    
    
    nutrient_ = nutrient[0]
    calories = nutrient_[1]
    carbohydrate = nutrient_[2]
    protein = nutrient_[3]
    fat = nutrient_[4]
    sodium = nutrient_[5]
    calcium = nutrient_[6]
    vitamin_c = nutrient_[7]
    saturated_fat = nutrient_[8]
    
    if (select=="choice_01"):
      rate = float(choice_01)/float(choice_02)
      calories *=rate
      carbohydrate*=rate
      protein *=rate
      fat*=rate
      sodium*=rate
      calcium*=rate
      vitamin_c*=rate
      saturated_fat*=rate

    
        
    elif(select=="choice_03"):
      rate = float(choice_03)/float(choice_02)
      calories *=rate
      carbohydrate*=rate
      protein *=rate
      fat*=rate
      sodium*=rate
      calcium*=rate
      vitamin_c*=rate
      saturated_fat*=rate
    
    calories_n.append(calories)
    carbohydrate_n.append(carbohydrate)
    protein_n.append(protein)
    fat_n.append(fat)
    sodium_n.append(sodium)
    calcium_n.append(calcium)
    vitamin_c_n.append(vitamin_c)
    saturated_fat_n.append(saturated_fat)
    
    
    print("칼로리거침")
    

    ## 기타일 때는 추후 작성
       
        

    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        # "text": "섭취한 양은 ~~ 칼로리는~~~\n\n다음 음식은 무엇을 드셨나요?\n\n계속 입력하시려면 [계속 입력]을 \n 없다면 [종료]를 눌러주세요."
                        "text": "다음 음식은 무엇을 드셨나요?\n\n계속 입력하시려면 [계속 입력]을 \n 없다면 [종료]를 눌러주세요." 
                }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "직접 입력",
                    "action": "message",
                    "label": "계속 입력"
                }, {
                    "messageText": "종료",
                    "action": "message",
                    "label":  "🏠종료"
                }
            ]
        }
    }

    return jsonify(res)

@app.route("/calories_02", methods=["GET", "POST"])
def calorie_02():
    
    req = request.get_json()
    print(req)

    select = req["action"]["detailParams"]["선택"]["origin"]
    print(select)
    
    conn = mysql.connect
    cur = conn.cursor()

    sql = "select * from Nutrient where food_name = '%s'" % (lan)
       
    cur.execute(sql)
    # conn.commit()
    nutrient = cur.fetchall()
    print(nutrient)
        
    cur.close()
    conn.close()
    
    


    global foodgl
    global foodglcp
    global diet_food_img
    nutrient_ = nutrient[0]
    calories = nutrient_[1]
    carbohydrate = nutrient_[2]
    protein = nutrient_[3]
    fat = nutrient_[4]
    sodium = nutrient_[5]
    calcium = nutrient_[6]
    vitamin_c = nutrient_[7]
    saturated_fat = nutrient_[8]
    
    if (select=="첫번째"):
      rate = float(choice_01_img)/float(choice_02_img)
      calories *=rate
      carbohydrate*=rate
      protein *=rate
      fat*=rate
      sodium*=rate
      calcium*=rate
      vitamin_c*=rate
      saturated_fat*=rate

    
        
    elif(select=="세번째"):
      rate = float(choice_03_img)/float(choice_02_img)
      calories *=rate
      carbohydrate*=rate
      protein *=rate
      fat*=rate
      sodium*=rate
      calcium*=rate
      vitamin_c*=rate
      saturated_fat*=rate
    
    calories_n.append(calories)
    carbohydrate_n.append(carbohydrate)
    protein_n.append(protein)
    fat_n.append(fat)
    sodium_n.append(sodium)
    calcium_n.append(calcium)
    vitamin_c_n.append(vitamin_c)
    saturated_fat_n.append(saturated_fat)
    
    
    print("칼로리거침_02")
        

    ## 기타일 때는 추후 작성
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        # "text": "섭취한 양은 ~~ 칼로리는~~~\n\n다음 음식은 무엇을 드셨나요?\n\n계속 입력하시려면 [계속 입력]을 \n 없다면 [종료]를 눌러주세요."
                        "text": "아래에서 인식된 음식의 양을 입력해주세요." 
                }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "끝",
                    "action": "message",
                    "label": "끝"
                }
            ]
        }            
    }
    
    str_img_version = ""
    
    for food in foodglcp:
        res['template']['quickReplies'].append({"messageText": food, "action":"message", "label":food})
        str_img_version = ""+food+", "
        print('----------------',food)
    print('--------!!--------',foodglcp)


    
    # img_food_used.append(res['template']['quickReplies'])
    
    # np.array(img_food_used).flatten().tolist()
    
    for i in res['template']['quickReplies']:
        print('+++++++++++d:', diet_food_img)
        if i['messageText'] in diet_food_img:
            print('===============i:',i)
            foodglcp.remove(i['messageText'])
            res['template']['quickReplies'].remove(i)
            print(res['template']['quickReplies'])

                    
    return jsonify(res)




@app.route("/getPh", methods=["GET", "POST"])
def start():
    global foodgl
    print("start func")
    req = request.get_json()

    print(req)

    photo_type3 = req["action"]["detailParams"]["image"]["value"]
    photo_json = json.loads(photo_type3)
    # foods = [] //AI통해서 인식한 음식
    print('3', photo_type3)

    # print(photo_json["secureUrls"])
    photo_url = photo_json["secureUrls"]
    u = photo_url[5:-1]
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
        
    urllib._urlopener = AppURLopener()

    urllib._urlopener.retrieve(u, "test.jpg")
    urlretrieve_img = Image.open("test.jpg")
    print("1////////")

    upload = {'image': open('/workspace/habit/test.jpg', 'rb')} # 업로드하기위한 파일
    print("2////////")

    res = requests.post('http://210.94.185.39:5000/receive', files=upload).json() # JSON 포맷, POST 형식으로 해당 URL에 파일 전송
    print("3////////")
    imgurl = res[0]['imgurl']
    food = res[1]['food']
    foodgl = []
    for i in food:
        foodgl.append(i)
    foodstr = ",".join(food)
    print(":::::::::::::::::;",imgurl,food)
    # imgurl = "https://habit-2021.s3.ap-northeast-2.amazonaws.com/image/"+imgurl
    conn = mysql.connect
    cur = conn.cursor()

    
    sql = "update Diet set image = '%s' where date = '%s' and mealtime = '%s'" % (""+imgurl, meal_date, selection) # AWS S3 address is confidential 

    cur.execute(sql)
    conn.commit()
    cur.fetchall()
    print(res)
    print("4////////")
    cur.close()
    print(foodstr)
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "인식된 식단사진",
                        "description": foodstr + "을 드셨군요.",
                        "thumbnail": {
                            "imageUrl":""+imgurl,     # AWS S3 address is confidential 
                            "fixedRatio": True
                        }
                    }
                }
            ],
            "quickReplies":[
                {
                    "messageText": "직접 입력",
                    "action": "message",
                    "label": "아니요,없는 음식이 있습니다."
                }, {
                    "messageText": "양",
                    "action": "message",
                    "label": "네,인식이 잘되었습니다."
                }
            ]
        }
    }
    return jsonify(res)




@app.route("/foods", methods=['POST'])
def food():
    global foods
    print("Start to enter: ")
    req = request.get_json()
    
    print(req)
    
    food = req["action"]["detailParams"]["음식이름"]["value"]
    foods = food
    print(foods)
    diet_food.append(foods)
    
    print(diet_food)
    
    conn = mysql.connect
    cur = conn.cursor()
 
    sql = "select choice_01, choice_02, choice_03, unit from Food where food_type = '%s'" % (foods)
    print("::::::::::::::::::::::::::{0}".format(sql))
    cur.execute(sql)
    # conn.commit()
    food_str = cur.fetchall()
    print(food_str)
    cur.close()
    conn.close()

    food_tuple = food_str[0]
    global choice_01
    global choice_02
    global choice_03
    choice_01 = food_tuple[0]
    choice_02 = food_tuple[1]
    choice_03 = food_tuple[2]
    unit = food_tuple[3]

    res = {
             "version": "2.0",
             "template": {
                   "outputs": [
                     {
                         "simpleText": {
                         "text": foods + "을 드셨군요\n 아래에서 드신량을 선택해주세요."
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "choice_01",
                    "action": "message",
                    "label": choice_01
                }, {
                    "messageText": "choice_02",
                    "action": "message",
                    "label":  choice_02 + unit
                }, {
                    "messageText": "choice_03",
                    "action": "message",
                    "label": choice_03
                }, {
                    "messageText": "기타",
                    "action": "message",
                    "label": "기타"
                }
            ]
        }
    }

    return jsonify(res)
    # conn = mysql.connect
    # cursor = conn.cursor()

    # sql = ""


@app.route("/date", methods=["GET", "POST"])
def date():
    print("Start to enter: ")
    req = request.get_json()

    print(req)

    time = req["action"]["detailParams"]["date"]["value"]
    date_json = json.loads(time)
    global meal_date
    meal_date = date_json["value"]
    print(meal_date)

    conn = mysql.connect
    cur = conn.cursor()
    print(6)
    sql = "insert into Diet(date) values ('%s')" % (meal_date)

    cur.execute(sql)
    conn.commit()
    # cur.fetchall()
    # print(hi)
    cur.close()
    conn.close()
    
    conn = mysql.connect
    cur = conn.cursor()
    print(6)
    sql = "insert into Solution(solution_date) values ('%s')" % (meal_date)

    cur.execute(sql)
    conn.commit()
    # cur.fetchall()
    # print(hi)
    cur.close()
    conn.close()

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "아래에서 아침, 점심, 저녁, 간식 중 하나를 골라주세요."
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "아침",
                    "action": "message",
                    "label": "아침"
                }, {
                    "messageText": "점심",
                    "action": "message",
                    "label": "점심"
                }, {
                    "messageText": "저녁",
                    "action": "message", 
                    "label": "저녁"
                }, {
                    "messageText": "간식",
                    "action": "message",
                    "label": "간식"
                }
            ]
        }
    }
    return jsonify(res)


@app.route("/time", methods=["POST"])
def time():
    req = request.get_json()
    
    global selection
    selection = req['userRequest']['utterance']
    print(selection)

    conn = mysql.connect
    cur = conn.cursor()
    print(selection+"06")
    sql = "update Diet set mealtime='%s' where date = '%s'" % (selection, meal_date)
    # sql = 'select * from Diet'

    cur.execute(sql)
    conn.commit()
    # print(hi)
    cur.close()
    conn.close()
    
    conn = mysql.connect
    cur = conn.cursor()
    print(6)
    sql = "update Solution set solution_mealtime = '%s' where solution_date= '%s'" % (selection, meal_date)

    cur.execute(sql)
    conn.commit()
    # cur.fetchall()
    # print(hi)
    cur.close()
    conn.close()
    # if select == "아침":
    #     answer2 = "아침 식사로 드셨군요"
    # elif select == "점심":
    #     answer2 = "점심 식사로 드셨군요"
    # elif select == "저녁":
    #     answer2 = "저녁 식사로 드셨군요"
    # elif select == "간식":
    #     answer2 = "간식으로 드셨군요"
    #     print(answer2)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "야"
                    }
                }
            ],
        }
    }
    return jsonify(res)

@app.route("/solution", methods=["POST"])
def solution():
    global foodglcp
    global foodgl
    global diet_food_img

    req = request.get_json()

    select = req['userRequest']['utterance']
    print(select)
    
    calories_res = 0
    carbohydrate_res = 0
    protein_res = 0
    fat_res = 0
    sodium_res = 0
    calcium_res = 0
    vitamin_c_res = 0
    saturated_fat_res = 0
    
    for i in calories_n:
        calories_res+=i
    for i in carbohydrate_n:
        carbohydrate_res+=i
    for i in protein_n:
        protein_res+=i
    for i in fat_n:
        fat_res+=i
    for i in sodium_n:
        sodium_res+=i
    for i in calcium_n:
        calcium_res+=i
    for i in vitamin_c_n:
        vitamin_c_res+=i
    for i in saturated_fat_n:
        saturated_fat_res+=i
    
    k = len(diet_food)
    m  = 0
    str_ = ""
    while(1):
        if k==m: 
            break
        else:
            str_ = str_ + str(diet_food[m])
            str_ = str_ + " "
        
        m+=1
        
        
        
    
    conn = mysql.connect
    cur = conn.cursor()

    
    sql = "update Diet set foods = '%s', calories = '%s',carbohydrate='%s', protein='%s',fat = '%s',sodium='%s',calcium = '%s',vitamin_c='%s',saturated_fat='%s' where mealtime = '%s' and date = '%s'" % (str_,calories_res, carbohydrate_res,protein_res,fat_res, sodium_res,calcium_res,vitamin_c_res,saturated_fat_res,selection,meal_date)

    cur.execute(sql)
    conn.commit()
    cur.fetchall()
    # print(hi)
    cur.close()
    conn.close()
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "섭취하신 음식의 영양정보는\n칼로리: %skcal, \n탄수화물: %sg , \n단백질: %sg, \n지방: %sg, \n나트륨: %smg, \n칼슘: %smg, \n비타민 C: %smg, \n포화지방산: %smg입니다. \n\n"%(round(calories_res,2),
                        round(carbohydrate_res,2),round(protein_res,2),round(fat_res,2),round(sodium_res,2),round(calcium_res,2),round(vitamin_c_res,2),round(saturated_fat_res,2))
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "솔루션",
                    "action": "message",
                    "label": "솔루션 보러가기"
                }
            ]
        }
    }
    foodglcp=[]
    foodgl=[]
    diet_food_img=[]
    return jsonify(res)

@app.route("/solution_02", methods=["POST"])
def solution_02():
    global foodglcp
    global foodgl
    global diet_food_img
    req = request.get_json()

    select = req['userRequest']['utterance']
    print(select)
    
    calories_res = 0
    carbohydrate_res = 0
    protein_res = 0
    fat_res = 0
    sodium_res = 0
    calcium_res = 0
    vitamin_c_res = 0
    saturated_fat_res = 0
    
    for i in calories_n:
        calories_res+=i
    for i in carbohydrate_n:
        carbohydrate_res+=i
    for i in protein_n:
        protein_res+=i
    for i in fat_n:
        fat_res+=i
    for i in sodium_n:
        sodium_res+=i
    for i in calcium_n:
        calcium_res+=i
    for i in vitamin_c_n:
        vitamin_c_res+=i
    for i in saturated_fat_n:
        saturated_fat_res+=i
    
    k = len(diet_food_img)
    m  = 0
    str_ = ""
    while(1):
        if k==m: 
            break
        else:
            str_ = str_ + str(diet_food_img[m])
            str_ = str_ + " "
        
        m+=1
        
        
        
    
    conn = mysql.connect
    cur = conn.cursor()

    
    sql = "update Diet set foods = '%s', calories = '%s',carbohydrate='%s', protein='%s',fat = '%s',sodium='%s',calcium = '%s',vitamin_c='%s',saturated_fat='%s' where mealtime = '%s' and date = '%s'" % (str_,calories_res, carbohydrate_res,protein_res,fat_res, sodium_res,calcium_res,vitamin_c_res,saturated_fat_res,selection,meal_date)

    cur.execute(sql)
    conn.commit()
    cur.fetchall()
    # print(hi)
    cur.close()
    conn.close()
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "섭취하신 음식의 영양정보는\n칼로리: %skcal, \n탄수화물: %sg , \n단백질: %sg, \n지방: %sg, \n나트륨: %smg, \n칼슘: %smg, \n비타민 C: %smg, \n포화지방산: %smg입니다. \n\n"%(round(calories_res,2),
                        round(carbohydrate_res,2),round(protein_res,2),round(fat_res,2),round(sodium_res,2),round(calcium_res,2),round(vitamin_c_res,2),round(saturated_fat_res,2))
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "솔루션",
                    "action": "message",
                    "label": "솔루션 보러가기"
                }
            ]
        }
    }
    foodglcp=[]
    foodgl=[]
    diet_food_img=[]
    return jsonify(res)

@app.route("/nusolution", methods=["POST"])
def nusolution():
    req = request.get_json()

    select = req['userRequest']['utterance']
    print(select)

    # conn = mysql.connect
    # cur = conn.cursor()
    # sql = "update Diet set mealtime='%s' where date = '%s'" % (selection, meal_date)
    

    # cur.execute(sql)
    # conn.commit()
    # # print(hi)
    # cur.close()
    # conn.close()
    
    conn = mysql.connect
    cur = conn.cursor()
    sql = "select foods, calories, carbohydrate, protein, fat, sodium, calcium, vitamin_c, saturated_fat from Diet where date = '%s' and mealtime = '%s'" % (meal_date,selection)
    

    cur.execute(sql)
    food_set = cur.fetchall()
    print(food_set)
    cur.close()
    conn.close()
    
    food_set = food_set[0]
    food_list = food_set[0]
    calories_sol = food_set[1]
    carbohydrate_sol = food_set[2]
    protein_sol = food_set[3]
    fat_sol = food_set[4]
    sodium_sol = food_set[5]
    calcium_sol = food_set[6]
    vitamin_c_sol = food_set[7]
    saturated_fat_sol = food_set[8]
    
    
    
    carbohydrate_ss = ""
    protein_ss = ""
    fat_ss = ""
    sodium_ss = ""
    calcium_ss = ""
    vitamin_ss = ""
    saturated_fat_ss = ""
    
    rcmd = "" # 식단 추천
    
    if "라면" in food_list :
        a = "<라면>\n"+ "튀기지 않은 면으로 가급적 드시기 바랍니다."
        rcmd = rcmd + a
    print("")
    if "튀김" in food_list:
        b = "튀김은 고지방 음식입니다. 높은 지방은 대장 건강에 좋지 않습니다.지방을 줄이기 위해 재료를 가급적이면 삶거나 쪄서 식사를 하시길 바랍니다."
        rcmd = rcmd + b
    print("")
    if "소주" in food_list:
        c= "\n<소주>\n"+"술은 피하세요."
        rcmd = rcmd+c
    print("")
    if "제육볶음" in food_list:
        d= "붉은 육류와 가공육은 지방 함유량이 높아 대장이 좋지 않습니다. 두부는 단백질을 붉은육류의 85%나 함량하고 있으며 붉은육류에 비해 콜레스테롤과 포화지방산의 함량이 거의없고 칼로리도 아주적습니다. 따라서 붉은 육류를 줄이고 두부요리로 대체하는것을 추천합니다. 생선은 지방 함유량이 붉은 육류에 비해 적은데다, 생선 역시동물성 단백질을 가지고 있기 때문에 단백질 섭취에 적절합니다. 또한, 비타민D를함유하고 있기 떄문에 대장암의 위험을 직접적으로 낮춥니다."
        rcmd = rcmd+d
    
    print("<탄수화물>")
    
    if carbohydrate_sol<=104.5:
        carbohydrate_ss = "한끼섭취량 대비 탄수화물 부족이며"
    elif carbohydrate_sol<115.5:
        carbohydrate_ss = "한끼섭취량 대비 탄수화물 적정이며."
    else:
        carbohydrate_ss = "한끼섭취량 대비 탄수화물 과다이며."
        
    print("<단백질>")
    
    if protein_sol<=17.5:
        protein_ss = "단백질 부족,"
    elif protein_sol<19.2:
        protein_ss = "단백질 적정,"
    else:
        protein_ss = "단백질 과다,"
    print("<지방>")
    if fat_sol<=16.15:
        fat_ss = "지방 부족입니다."
    elif fat_sol<17.85:
        fat_ss = "지방 적정입니다."
    else:
        fat_ss = "지방 과다입니다."
    print("")
    
    solution_fin = carbohydrate_ss+protein_ss+fat_ss
    # print("solution final:"+foodgl)
    conn = mysql.connect
    cur = conn.cursor()

    
    sql = "update Solution set solution = '%s' where solution_date = '%s' and solution_mealtime = '%s'" % (rcmd + solution_fin ,meal_date, selection)

    cur.execute(sql)
    conn.commit()
    # cur.fetchall()
    # print(hi)
    cur.close()
    conn.close()
    
    
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "<영양성분 분석>\n\n"+rcmd+"\n"+carbohydrate_ss +"\n"+protein_ss +fat_ss+"\n\n"+"더 자세한 솔루션은 아래의 홈페이지를 참고해주세요\n\n"+"http://3.36.96.100:5000/"
                    }
                }
            ],
               "quickReplies": [
                {
                    "messageText": "추천음식",
                    "action": "message",
                    "label": "추천음식 보러가기"
                }
            ]
        }
    }       
    return jsonify(res)

@app.route("/amount", methods=["GET", "POST"])
def amount():

    print('getPhotos end')
    req = request.get_json()
    global foodglcp
    foodglcp = foodgl
    select = req['userRequest']['utterance']
    print(select)
    
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        # "text": "섭취한 양은 ~~ 칼로리는~~~\n\n다음 음식은 무엇을 드셨나요?\n\n계속 입력하시려면 [계속 입력]을 \n 없다면 [종료]를 눌러주세요."
                        "text": "아래에서 인식된 음식의 양을 입력해주세요." 
                }
                }
            ],
            "quickReplies": [
                # {
                #     "messageText": foodgl[0],
                #     "action": "message",
                #     "label": foodgl[0]
                # }, {
                #     "messageText": foodgl[1],
                #     "action": "message",
                #     "label":  "쌀밥"
                # },
                #  {
                #     "messageText": foodgl[2],
                #     "action": "message",
                #     "label":  foodgl[2]
                # }
            ]
        }            
    }
    
    str_img_version = ""
    
    for food in foodglcp:
        res['template']['quickReplies'].append({"messageText": food, "action":"message", "label":food})
        str_img_version = ""+food+", "
    
    
    return jsonify(res)

@app.route("/arrary", methods=['POST'])
def arrary():
    req = request.get_json()
    global lan
    lan = req['userRequest']['utterance']
    print(lan)
    
    diet_food_img.append(lan)
    
    print(diet_food_img)
    
    conn = mysql.connect
    cur = conn.cursor()

    sql = "select choice_01, choice_02, choice_03, unit from Food where food_type = '%s'" % (lan)

    cur.execute(sql)
    # conn.commit()
    food_str = cur.fetchall()
    print(food_str)
    cur.close()
    conn.close()

    food_tuple = food_str[0]
    global choice_01_img
    global choice_02_img
    global choice_03_img
    choice_01_img = food_tuple[0]
    choice_02_img = food_tuple[1]
    choice_03_img = food_tuple[2]
    unit = food_tuple[3]

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": lan + "을 드셨군요\n 아래에서 드신량을 선택해주세요."
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "첫번째",
                    "action": "message",
                    "label": choice_01_img
                }, {
                    "messageText": "두번째",
                    "action": "message",
                    "label":  choice_02_img + unit
                }, {
                    "messageText": "세번째",
                    "action": "message",
                    "label": choice_03_img
                }, {
                    "messageText": "기타",
                    "action": "message",
                    "label": "기타"
                }
            ]
        }
    }
    print("거침1")
    return jsonify(res)

@app.route("/direct", methods=['POST'])
def direct():
    req = request.get_json()
    
    global selection
    la = req['userRequest']['utterance']


    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "다음"
                    }
                }
            ],
        }
    }

    return jsonify(res)


@app.route("/printcal", methods=["POST"])
def printcal():
    req = request.get_json()
    global foodglcp
    global foodgl
    global diet_food_img

    select = req['userRequest']['utterance']
    print(select)
    
    calories_res = 0
    carbohydrate_res = 0
    protein_res = 0
    fat_res = 0
    sodium_res = 0
    calcium_res = 0
    vitamin_c_res = 0
    saturated_fat_res = 0
    
    for i in calories_n:
        calories_res+=i
    for i in carbohydrate_n:
        carbohydrate_res+=i
    for i in protein_n:
        protein_res+=i
    for i in fat_n:
        fat_res+=i
    for i in sodium_n:
        sodium_res+=i
    for i in calcium_n:
        calcium_res+=i
    for i in vitamin_c_n:
        vitamin_c_res+=i
    for i in saturated_fat_n:
        saturated_fat_res+=i
    
    k = len(foodgl)
    m  = 0
    str_ = ""
    while(1):
        if k==m: 
            break
        else:
            str_ = str_ + str(foodgl[m])
            str_ = str_ + " "
        
        m+=1
        
        
        
    
    conn = mysql.connect
    cur = conn.cursor()

    
    sql = "update Diet set foods = '%s', calories = '%s',carbohydrate='%s', protein='%s',fat = '%s',sodium='%s',calcium = '%s',vitamin_c='%s',saturated_fat='%s' where mealtime = '%s' and date = '%s'" % (str_,calories_res, carbohydrate_res,protein_res,fat_res, sodium_res,calcium_res,vitamin_c_res,saturated_fat_res,selection,meal_date)

    cur.execute(sql)
    conn.commit()
    cur.fetchall()
    # print(hi)
    cur.close()
    conn.close()
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "섭취하신 음식의 영양정보는\n칼로리: %skcal, \n탄수화물: %sg , \n단백질: %sg, \n지방: %sg, \n나트륨: %smg, \n칼슘: %smg, \n비타민 C: %smg, \n포화지방산: %smg입니다. \n\n"%(round(calories_res,2),
                        round(carbohydrate_res,2),round(protein_res,2),round(fat_res,2),round(sodium_res,2),round(calcium_res,2),round(vitamin_c_res,2),round(saturated_fat_res,2))
                    }
                }
            ],
            "quickReplies": [
                {
                    "messageText": "솔루션",
                    "action": "message",
                    "label": "솔루션 보러가기"
                }
            ]
        }
    }
    
    foodglcp=[]
    foodgl=[]
    diet_food_img=[]
    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)