'''
Created on 2021. 10. 21.

@author: 신재현
'''
import requests, json, re

api_key = "90d0e27636f760e0ce5b5d2a38c09a7a" #themoviedb apikey
lan = re.compile('[a-z]{2}-[A-Z]{2}')
reg = re.compile('[A-Z]{2}')
squidgame = "93405"
venom = "580489"
poster_url = "https://image.tmdb.org/t/p/original"
noimage = "../static/images/noimage.jpg"

#tmdb 인기 순위 불러오기    
def getPopular(get_type,language="ko-KR",region="KR"):
    url = "https://api.themoviedb.org/3/" + get_type +"/popular?api_key=" + api_key + "&language=" + language + "&region=" + region
    rq = requests.get(url)
    t = rq.text
    datas = json.loads(t)

    return datas

# tmdb 검색
def searchDb(search_type, query, language="ko-KR"):
    url = "https://api.themoviedb.org/3/search/" + search_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language
    rq = requests.get(url)
    t = rq.text
    datas = json.loads(t)
    
    return datas

def getPage(media_type, query, language="ko-KR", region="KR"):
    url = "https://api.themoviedb.org/3/search/" + media_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language
    rq = requests.get(url)
    t = rq.text
    datas = json.loads(t)
    pages = datas['total_pages']
    
    return pages

def getGenre(genreCd):
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key + "&language=ko-KR"
    rq = requests.get(url)
    t = rq.text
    datas = json.loads(t)
    genre = ""
    
    for i in range(len(datas['genres'])) :
        if datas['genres'][i]['id'] in genreCd :
            genre += " , " + datas['genres'][i]['name']
            
    return genre[2:]

def getCredit(media_type,contentId,language="ko-KR"):
    url = "https://api.themoviedb.org/3/" + media_type + "/" + contentId +"/credits?api_key=" + api_key + "&language=" + language
    rq =requests.get(url)
    t = rq.text
    datas = json.loads(t)
    
    credit = {}
    actors = []
    crews = []
    if datas['cast'] :
        for i in range(len(datas['cast'])) :
            actor = {}
            actor['actorCd'] = datas['cast'][i]['id']
            actor['actorNm'] = datas['cast'][i]['name']
            actor['character'] = datas['cast'][i]['character']
            if datas['cast'][i]['profile_path'] :
                actor['profile'] = poster_url + datas['cast'][i]['profile_path']
            else :
                actor['profile'] = noimage
            actors.append(actor)
    if datas['crew'] :
        for i in range(len(datas['crew'])) :
            crew ={}
            crew['crewCd'] = datas['crew'][i]['id']
            crew['crewNm'] = datas['crew'][i]['name']
            if datas['crew'][i]['profile_path'] :
                crew['profile'] = poster_url + datas['crew'][i]['profile_path']
            else :
                crew['profile'] = noimage
            crew['department'] = datas['crew'][i]['department']
            crew['job'] = datas['crew'][i]['job']
            
            crews.append(crew)
    credit['cast'] = actors
    credit['crew'] = crews
    
    return credit

# 인데스 페이지 영화인 필모
def indexPeople(name):
    peoples = []
    person = searchDb("person", name)['results']
    for i in range(len(person)):
        p_dict = {}
        
        filmos = []
        
        p_dict['peopleCd'] = person[i]['id']
        p_dict['peopleNm'] = person[i]['name']
        p_dict['role'] = person[i]['known_for_department']
        if person[i]['profile_path'] : 
            p_dict['profile'] = poster_url + person[i]['profile_path']
        else :
            p_dict['profile'] = noimage
        if len(person[i]['known_for']) > 0 : 
            for j in range(len(person[i]['known_for'])):
                f_dict = {}
                f_dict['media_type'] = person[i]['known_for'][j]['media_type']
                f_dict['contentCd'] = person[i]['known_for'][j]['id']
                if(f_dict['media_type'] == "movie") :
                    f_dict['contentNm'] = person[i]['known_for'][j]['title']
                    f_dict['poster'] = poster_url + person[i]['known_for'][j]['poster_path']
                    f_dict['release_date'] = person[i]['known_for'][j]['release_date']
                elif (f_dict['media_type'] == "tv") :
                    f_dict['contentNm'] = person[i]['known_for'][j]['name']
                    f_dict['poster'] = poster_url + person[i]['known_for'][j]['poster_path']
                    f_dict['release_date'] = person[i]['known_for'][j]['first_air_date']
                else :
                    f_dict['contentNm'] = "데이터 없음"
                    f_dict['poster'] = noimage
                    f_dict['release_date'] = "데이터 없음"
                filmos.append(f_dict)
                
            p_dict['filmos'] = filmos
        else :
            pass
        peoples.append(p_dict)
    return peoples

# 인덱스 페이지 인기 순위
def indexPopular(media_type):
    populars = []
    popular = getPopular(media_type)['results']
    
    if media_type == "movie" :
        for i in range(len(popular)):
            pm_dict ={}
            pm_dict["media_type"] = "movie"
            pm_dict['contentCd'] = popular[i]['id']
            pm_dict['contentNm'] = popular[i]['title']
            pm_dict['rank'] = i + 1
            
            if popular[i]['poster_path'] :
                pm_dict['poster'] = poster_url + popular[i]['poster_path']
            else :
                pm_dict['poster'] = noimage
                
            pm_dict['release_date'] = popular[i]['release_date']
            populars.append(pm_dict)
            
    elif media_type == "tv" :
        for i in range(len(popular)):
            pt_dict ={}
            pt_dict["media_type"] = "tv"
            pt_dict['contentCd'] = popular[i]['id']
            pt_dict['contentNm'] = popular[i]['name']
            pt_dict['rank'] = i + 1
            
            if popular[i]['poster_path'] :
                pt_dict['poster'] = poster_url + popular[i]['poster_path']
            else :
                pt_dict['poster'] = noimage
            
            pt_dict['release_date'] = popular[i]['first_air_date']
            populars.append(pt_dict)
            
    return populars

# 해당 프로그램 세부정보 불러오기
def getDetail(media_type, contentId, language="ko-KR"):
    #get_type은 영상 종류(movie,tv...) get_id(세부정보를 찾고싶은 id) 반드시 기입.
    url = "https://api.themoviedb.org/3/"+ media_type + "/" + contentId + "?api_key=" + api_key + "&language=" + language
    rq = requests.get(url)
    t = rq.text
    data = json.loads(t)
    credit = getCredit(media_type, contentId)
    
    result = {}
    genre=""
    genreCd=[]
    company=""
    companyCd=[]
    country=""
    countryCd=[]
    network=""
    networkCd=[]
    
    if media_type == "movie" :
        result['contentCd'] = data['id']
        result['contentNm'] = data['title']
        result['originalNm'] = data['original_title']
        result['status'] = data['status']
        result['release_date'] = data['release_date']
        result['runtime'] = data['runtime']
        result['tagline'] = data['tagline']
        result['overview'] = data['overview']
        
        if data['poster_path'] :
            result['poster'] = poster_url + data['poster_path']
        else :
            result['poster'] = noimage
        if data['backdrop_path'] :
            result['backdrop_path'] = poster_url + data['backdrop_path']
        result['homepage'] = data['homepage']
        
        if data['genres'] :
            for i in range(len(data['genres'])):
                genreCd.append(data['genres'][i]['id'])
                genre += " , " + data['genres'][i]['name']
                
        result['genreCd'] = genreCd
        result['genre'] = genre[3:]
        
        if data['production_companies'] :
            for i in range(len(data['production_companies'])):
                companyCd.append(data['production_companies'][i]['id'])
                company += " | " + data['production_companies'][i]['name']
                
        result['companyCd'] = companyCd
        result['company'] = company[3:]
        
        if data['production_countries'] :
            for i in range(len(data['production_countries'])) :
                countryCd.append(data['production_countries'][i]['iso_3166_1'])
                country += " | " + data['production_countries'][i]['name']
                
        result['countryCd'] =countryCd
        result['country'] = country[3:]
        
        if data['belongs_to_collection']:
            result['seriesCd'] = data['belongs_to_collection']['id']
            result['seriesNm'] = data['belongs_to_collection']['name']
            result['series_poster_path'] = poster_url + data['belongs_to_collection']['poster_path']
            result['series_backdrop_path'] = poster_url + data['belongs_to_collection']['backdrop_path']
        
        result['cast'] = credit['cast']
        result['crew'] = credit['crew']
        
    elif media_type == "tv" :
        result['contentCd'] = data['id']
        result['contentNm'] = data['name']
        result['originalNm'] = data['original_name']
        result['status'] = data['status']
        result['number_of_episodes'] = data['number_of_episodes']
        result['number_of_seasons'] = data['number_of_seasons']
        result['release_date'] = data['first_air_date']
        result['tagline'] = data['tagline']
        result['overview'] = data['overview']
        
        if data['poster_path'] :
            result['poster'] = poster_url + data['poster_path']
        else :
            result['poster'] = noimage
            
        if data['backdrop_path'] :
            result['backdrop_path'] = poster_url + data['backdrop_path']
        
        result['homepage'] = data['homepage']
        
        if data['genres'] :
            for i in range(len(data['genres'])):
                genreCd.append(data['genres'][i]['id'])
                genre += " , " + data['genres'][i]['name']
                
        result['genreCd'] = genreCd
        result['genre'] = genre[3:]
        
        if data['production_companies'] :
            for i in range(len(data['production_companies'])):
                companyCd.append(data['production_companies'][i]['id'])
                company += " | " + data['production_companies'][i]['name']
                
        result['companyCd'] = companyCd
        result['company'] = company[3:]
        
        if data['production_countries'] :
            for i in range(len(data['production_countries'])) :
                countryCd.append(data['production_countries'][i]['iso_3166_1'])
                country += " | " + data['production_countries'][i]['name']
                
        result['countryCd'] =countryCd
        result['country'] = country[3:]
        
        if data['networks']:
            for i in range(len(data['networks'])):
                network += " , " + data['networks'][i]['name']
                networkCd.append(data['networks'][i]['id'])
        
        result['networkCd'] = networkCd
        result['network'] = network[3:]
        
        result['cast'] = credit['cast']
        result['crew'] = credit['crew']
    
    return result

def searchResultPage(media_type, query, pages, language="ko-KR", region="KR"):
    url = "https://api.themoviedb.org/3/search/"+ media_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language + "&page=" + pages
    rq = requests.get(url)
    t = rq.text
    results = json.loads(t)

    if results['results'] :
        idata= results['results']
        datas =[]
        for y in range(len(idata)):
            data = {}
            if media_type == "movie" :
                data['contentCd'] = idata[y]['id']
                data['media_type'] = media_type
                data['contentNm'] = idata[y]['title']
                data['originalNm'] = idata[y]['original_title']
                if 'release_date' in idata[y] :
                    data['release_date'] = idata[y]['release_date']
                else :
                    data['release_date'] = "데이터 없음"
                data['genre'] = getGenre(idata[y]['genre_ids'])
                data['overview'] = idata[y]['overview']
                if idata[y]['poster_path'] :
                    data['poster'] = poster_url + idata[y]['poster_path']
                else:
                    data['poster'] = noimage

            elif media_type == "tv" :
                data['contentCd'] = idata[y]['id']
                data['media_type'] = media_type
                data['contentNm'] = idata[y]['name']
                data['originalNm'] = idata[y]['original_name']
                data['release_date'] = idata[y]['first_air_date']
                data['genre'] = getGenre(idata[y]['genre_ids'])
                data['overview'] = idata[y]['overview']
                if idata[y]['poster_path'] :
                    data['poster'] = poster_url + idata[y]['poster_path']
                else:
                    data['poster'] = noimage
            
            elif media_type == "person" :
                data['peopleCd'] = idata[y]['id']
                data['media_type'] = media_type
                data['peopleNm'] = idata[y]['name']
                if idata[y]['profile_path']:
                    data['profile'] = poster_url + idata[y]['profile_path']
                else:
                    data['profile'] = noimage
                if idata[y]['known_for'] :
                    filmoCd = []
                    filmoNm = ""
                    for z in range(len(idata[y]['known_for'])):
                        if idata[y]['known_for'][z]['media_type'] == "movie" :
                            filmoCd.append(idata[y]['known_for'][z]['id'])
                            filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                        elif idata[y]['known_for'][z]['media_type'] == "tv" :
                            filmoCd.append(idata[y]['known_for'][z]['id'])
                            filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                    data['filmoCd'] = filmoCd 
                    data['filmoNm'] = filmoNm[3:]
            else :
                pass
            datas.append(data)
    
    return datas
def searchResultSimple (media_type,query,language="ko-KR"):
    url = "https://api.themoviedb.org/3/search/"+ media_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language
    rq = requests.get(url)
    t = rq.text
    results = json.loads(t)

    if results['results'] :
        idata= results['results']
        datas =[]
        
        if len(idata) < 5 :
            for y in range(len(idata)):
                data = {}
                if media_type == "movie" :
                    data['contentCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['contentNm'] = idata[y]['title']
                    data['originalNm'] = idata[y]['original_title']
                    if 'release_date' in idata[y] :
                        data['release_date'] = idata[y]['release_date']
                    else :
                        data['release_date'] = "데이터 없음"
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                    data['overview'] = idata[y]['overview']
                    if idata[y]['poster_path'] :
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
    
                elif media_type == "tv" :
                    data['contentCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['contentNm'] = idata[y]['name']
                    data['originalNm'] = idata[y]['original_name']
                    data['release_date'] = idata[y]['first_air_date']
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                    data['overview'] = idata[y]['overview']
                    if idata[y]['poster_path'] :
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
                
                elif media_type == "person" :
                    data['peopleCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['peopleNm'] = idata[y]['name']
                    if idata[y]['profile_path']:
                        data['profile'] = poster_url + idata[y]['profile_path']
                    else:
                        data['profile'] = noimage
                    if idata[y]['known_for'] :
                        filmoCd = []
                        filmoNm = ""
                        for z in range(len(idata[y]['known_for'])):
                            if idata[y]['known_for'][z]['media_type'] == "movie" :
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                                filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                            elif idata[y]['known_for'][z]['media_type'] == "tv" :
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                                filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                        data['filmoCd'] = filmoCd 
                        data['filmoNm'] = filmoNm[3:]
                else :
                    pass
                datas.append(data)
                
        else :
            for y in range(0,5):
                data = {}
                if media_type == "movie" :
                    data['contentCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['contentNm'] = idata[y]['title']
                    data['originalNm'] = idata[y]['original_title']
                    if 'release_date' in idata[y] :
                        data['release_date'] = idata[y]['release_date']
                    else :
                        data['release_date'] = "데이터 없음"
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                    data['overview'] = idata[y]['overview']
                    if idata[y]['poster_path'] :
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
    
                elif media_type == "tv" :
                    data['contentCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['contentNm'] = idata[y]['name']
                    data['originalNm'] = idata[y]['original_name']
                    data['release_date'] = idata[y]['first_air_date']
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                    data['overview'] = idata[y]['overview']
                    if idata[y]['poster_path'] :
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
                
                elif media_type == "person" :
                    data['peopleCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['peopleNm'] = idata[y]['name']
                    if idata[y]['profile_path']:
                        data['profile'] = poster_url + idata[y]['profile_path']
                    else:
                        data['profile'] = noimage
                    if idata[y]['known_for'] :
                        filmoCd = []
                        filmoNm = ""
                        for z in range(len(idata[y]['known_for'])):
                            if idata[y]['known_for'][z]['media_type'] == "movie" :
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                                filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                            elif idata[y]['known_for'][z]['media_type'] == "tv" :
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                                filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                        data['filmoCd'] = filmoCd 
                        data['filmoNm'] = filmoNm[3:]
                else :
                    pass
                datas.append(data)
                
        return datas

def searchResultAll(media_type,query,language="ko-KR"):
    pages = getPage(media_type,query)
    datas = []
    for i in range(1,pages+1):
        url = "https://api.themoviedb.org/3/search/"+ media_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language + "&page=" + str(i)
        rq = requests.get(url)
        t = rq.text
        results = json.loads(t)
        
        if results['results'] :
            idata = results['results']
            for y in range(len(idata)):
                data = {}
                if media_type == "movie" :
                    data['contentCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['contentNm'] = idata[y]['title']
                    data['originalNm'] = idata[y]['original_title']
                    if 'release_date' in idata[y] :
                        data['release_date'] = idata[y]['release_date']
                    else :
                        data['release_date'] = "데이터 없음"
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                    data['overview'] = idata[y]['overview']
                    if idata[y]['poster_path'] :
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
    
                elif media_type == "tv" :
                    data['contentCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['contentNm'] = idata[y]['name']
                    data['originalNm'] = idata[y]['original_name']
                    data['release_date'] = idata[y]['first_air_date']
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                    data['overview'] = idata[y]['overview']
                    if idata[y]['poster_path'] :
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
                
                elif media_type == "person" :
                    data['peopleCd'] = idata[y]['id']
                    data['media_type'] = media_type
                    data['peopleNm'] = idata[y]['name']
                    if idata[y]['profile_path']:
                        data['profile'] = poster_url + idata[y]['profile_path']
                    else:
                        data['profile'] = noimage
                    if idata[y]['known_for'] :
                        filmoCd = []
                        filmoNm = ""
                        for z in range(len(idata[y]['known_for'])):
                            if idata[y]['known_for'][z]['media_type'] == "movie" :
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                                filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                            elif idata[y]['known_for'][z]['media_type'] == "tv" :
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                                filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                        data['filmoCd'] = filmoCd 
                        data['filmoNm'] = filmoNm[3:]
                else :
                    pass
                datas.append(data)
    
    return datas
# print(searchByPage("movie","007","1"))
# print(searchResultAll("movie", "007"))