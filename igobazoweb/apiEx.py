import json
import urllib.request
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from test.test_audioop import datas



client_id = 'uJYiiTGG_b6KE_OSUNq6'      #네이버 api key
client_secret = 'wTVxr4iBwC'
# apikey = "50b0981ddb27056a9923b2aac3902757"     # 영화진흥원 api key
# apikey = "c48796c983a73002305cc02636174e27"
apikey = "0f771c6f76bce84b4700e3029d302689" # 윤홍주 회원가입
culturekey = "eefa896a-2546-45e9-9cb3-c59e96bf88b2" #문화진흥원 api key



def boxOffice(): 
    ##### 박스오피스 가져오기 주의! 영화 포스터 이미지가 없음 #####        
    yesterday = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day - 1)
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'  + "?key=" + apikey + "&targetDt="  + yesterday +"&itemPerPage=10"
    rq = urllib.request.Request(url)
    response = urllib.request.urlopen(rq)
    response_body = response.read()
    result = json.loads(response_body.decode('utf-8'))
    boxoffice = result.get('boxOfficeResult')
    box_mv = boxoffice.get('dailyBoxOfficeList')
    
    return box_mv

def boxOfficeNation(KorF): 
    ##### 박스오피스 가져오기 주의! 영화 포스터 이미지가 없음 #####        
    yesterday = str(datetime.now().year) + str(datetime.now().month) + str(datetime.now().day - 1)
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'  + "?key=" + apikey + "&targetDt="  + yesterday +"&itemPerPage=10" + "&repNationCd=" + KorF
    rq = urllib.request.Request(url)
    response = urllib.request.urlopen(rq)
    response_body = response.read()
    result = json.loads(response_body.decode('utf-8'))
    boxoffice = result.get('boxOfficeResult')
    box_mv = boxoffice.get('dailyBoxOfficeList')
    
    return box_mv


def directorByMovieNm(movieCd):##### 영화 코드로 감독 이름 가져오기 #####
    #for box in box_mv :
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=" +apikey + "&movieCd=" +movieCd
    rq = requests.get(url)
    t = rq.text
    infors = json.loads(t)
    directors = infors['movieInfoResult']['movieInfo']['directors']
    director = []
    if len(directors) > 0 :
        for i in range(len(directors)):
            director.append(directors[i]['peopleNm'])
        return director
    else :
        return director
        

def movieInfoByTitle(movieNm):
    ##### 영화 타이틀로 영화 목록 가져오기 #####
    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=" +apikey + "&movieNm=" +movieNm
    rq = requests.get(url)
    t = rq.text
    infors = json.loads(t)
    infor = infors['movieListResult']['movieList']
    
    return infor

def movieInfoByDirector(directorNm):
    ##### 감독이름으로 영화 목록 가져오기 #####
    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=" +apikey + "&directorNm=" +directorNm
    rq = requests.get(url)
    t = rq.text
    info = json.loads(t)
    
    return info
    
def poster(movieNm,mv_director):
    ##### 영화 제목과 감독 이름이 일치하는 영화 포스터 image와 별점 가져오기  
    encText = urllib.parse.quote("{}".format(movieNm))
    url = "https://openapi.naver.com/v1/search/movie?query=" + encText  # json 결과
    movie_api_request = urllib.request.Request(url)
    movie_api_request.add_header("X-Naver-Client-Id", client_id)
    movie_api_request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(movie_api_request)
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        result = json.loads(response_body.decode('utf-8'))
        items = result['items']
        for item in items :
            nd =item['director']
            nd_index = nd.find('|')
            if nd[:nd_index] in mv_director :
                data = {}
                poster_image = item['image']
                rating = item['userRating']
                data['image'] = poster_image
                data['rating'] = rating
                return data


def boxOfficeMovie():
    ## 전날의 박스오피스 영화의 정보와 포스터를 가져옵니다 ## 
    box_list =[]
    boxs = boxOffice()
    for box in boxs :
        movieCd = box['movieCd']
        movieNm = box['movieNm']
        mv_director = directorByMovieNm(movieCd)
        image = poster(movieNm, mv_director)
        box['image'] = image
        box_list.append(box)
    return box_list


def boxOfficeMovieNation(KoF):
    ## 전날의 박스오피스 영화의 정보와 포스터를 가져옵니다 ## 
    box_list =[]
    boxs = boxOfficeNation(KoF)
    for box in boxs :
        movieCd = box['movieCd']
        movieNm = box['movieNm']
        mv_director = directorByMovieNm(movieCd)
        image = poster(movieNm, mv_director)
        box['image'] = image
        box_list.append(box)
    return box_list


def peopleInfo(peopleNm,role):
    ## 이름과 분야로 영화인의 코드, 이름, 분야, 필모를 가져옵니다. ##
    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=" + apikey + "&peopleNm="  + peopleNm
    rq = requests.get(url)
    t = rq.text
    infors = json.loads(t)
    peopleinfo = []
    for i in range(len(infors['peopleListResult']['peopleList'])):
        if infors['peopleListResult']['peopleList'][i]['repRoleNm'] == role :
            people = {}
            filmos = infors['peopleListResult']['peopleList'][i]['filmoNames']
            filmo = filmos.split('|')
            people['peopleCd'] = infors['peopleListResult']['peopleList'][i]['peopleCd']
            people['peopleNm'] = infors['peopleListResult']['peopleList'][i]['peopleNm']
            people['repRoleNm'] = infors['peopleListResult']['peopleList'][i]['repRoleNm']
            people['filmoNames'] = filmo
            peopleinfo.append(people)
    
    return(peopleinfo)

def movieInfoDetail(movieCd):
    ## 해당 영화 코드의 세부 정보와 이미지를 불러옵니다.
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key=" + apikey + "&movieCd=" + movieCd
    rq = requests.get(url)
    t = rq.text
    info = json.loads(t)
    
    movieNm = info['movieInfoResult']['movieInfo']['movieNm']
    if len(info['movieInfoResult']['movieInfo']['directors']) <= 0 :
        pass
    else : 
        info_list =  info['movieInfoResult']['movieInfo']
        
        director = []
        corp = ""
        actor =""
        genre = ""
        
        if len(info_list['directors']) > 0 :
            for i in range(len(info_list['directors'])):
                director.append(info_list['directors'][i]['peopleNm'])
        else :
            director.append("감독 없음")
        if len(info_list['companys']) >0 :
            for i in range(len(info_list['companys'])):
                corp += ( " | "  + info_list['companys'][i]['companyNm'])
        else :
            corp.append("")
        
        for i  in range(len(info_list['actors'])) :
            actor += (" | " +  info_list['actors'][i]['peopleNm'])
        for i in range(len(info_list['genres'])):
            genre += (" | " + info_list['genres'][i]['genreNm'])
        info_list.update(poster(movieNm, director))
        info_list['corp'] = corp[2:]
        info_list['director'] = director[0]
        info_list['actor'] = actor[2:]
        info_list['genre'] = genre[2:]
        
        return info_list

def actorFilmo(peopleNm):
    ## 해당 배우의 필모를 가져옵니다 ##
    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=" + apikey + "&peopleNm="  + peopleNm
    rq = requests.get(url)
    t = rq.text
    infors = json.loads(t)
    people_list = []

    for i in range(len(infors['peopleListResult']['peopleList'])) :
        if infors['peopleListResult']['peopleList'][i]['repRoleNm'] == "배우" :
            people = {}
            people['peopleCd'] = infors['peopleListResult']['peopleList'][i]['peopleCd']
            filmo = infors['peopleListResult']['peopleList'][i]['filmoNames']
            people['filmoNames'] = filmo.split('|')
            people_list.append(people)
            
    
    return people_list


def directorFilmo(directorNm):
    movies = movieInfoByDirector(directorNm)
    movie_list = []
    for movie in movies['movieListResult']['movieList'] :
        movieNm = movie['movieNm']
        image = (poster(movieNm,"황동혁"))
        movie['image'] = image
        movie_list.append(movie)
    
    return movie_list

def searchMovie(movieNm):
    encText = urllib.parse.quote("{}".format(movieNm))
    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=" +apikey + "&movieNm=" + encText 
    rq = requests.get(url)
    t = rq.text
    infors = json.loads(t)
    infor = infors['movieListResult']['movieList']
    
    for i in range (len(infor)) :
        directors = infor[i]['directors']
        for director in directors:
            title = infor[i]['movieNm']
            peopleNm = director['peopleNm']
            infor[i]['image'] = poster(title, peopleNm)
            infor[i]['director'] = peopleNm
            
    return infor



