'''
Created on 2021. 10. 21.

@author: 신재현
'''
import requests, json, re

api_key = "90d0e27636f760e0ce5b5d2a38c09a7a"  # themoviedb apikey
lan = re.compile('[a-z]{2}-[A-Z]{2}')
reg = re.compile('[A-Z]{2}')
squidgame = "93405"
venom = "580489"
poster_url = "https://image.tmdb.org/t/p/original"
noimage = "../static/images/noimage.jpg"
nodata = ""
# 이정재 = "73249"


# tmdb 인기 순위 불러오기    
def getPopular(get_type, language="ko-KR", region="KR"):
    url = "https://api.themoviedb.org/3/" + get_type + "/popular?api_key=" + api_key + "&language=" + language + "&region=" + region
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


def getPage(media_type, query, language="ko-KR"):
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
    
    for i in range(len(datas['genres'])):
        if datas['genres'][i]['id'] in genreCd:
            genre += " , " + datas['genres'][i]['name']
            
    return genre[2:]


def getCredit(media_type, contentId, language="ko-KR"):
    
    credits = ""
    
    if media_type == "person":
        credits = "combined_credits"
    else:
        credits = "credits"
        
    url = "https://api.themoviedb.org/3/" + media_type + "/" + contentId + "/" + credits + "?api_key=" + api_key + "&language=" + language
    rq = requests.get(url)
    t = rq.text
    datas = json.loads(t)
    
    credit = {}
    casts = []
    crews = []
    
    if media_type == "person":
        if datas['cast']:
            for i in range(len(datas['cast'])):
                cast = {}
                if datas['cast'][i]['id']:
                    cast['contentCd'] = datas['cast'][i]['id']
                else:
                    cast['contentCd'] = nodata
                
                if datas['cast'][i]['media_type']:
                    cast['media_type'] = datas['cast'][i]['media_type']
                    if datas['cast'][i]['media_type'] == "movie":
                        if datas['cast'][i]['title']:
                            cast['contentNm'] = datas['cast'][i]['title']
                        else:
                            cast['contentNm'] = nodata
                        
                        if datas['cast'][i]['original_title']:
                            cast['originalNm'] = datas['cast'][i]['original_title']
                        else:
                            cast['originalNm'] = nodata
                            
                        if datas['cast'][i]['release_date'] :
                            cast['release_date'] = datas['cast'][i]['release_date']
                        else :
                            cast['release_date'] = nodata
                            
                        if datas['cast'][i]['poster_path']:
                            cast['poster'] = poster_url + datas['cast'][i]['poster_path']
                        else:
                            cast['poster'] = noimage
                            
                        if datas['cast'][i]['backdrop_path']:
                            cast['backdrop'] = poster_url + datas['cast'][i]['backdrop_path']
                        else:
                            cast['backdrop'] = noimage
                        
                        if datas['cast'][i]['character']:
                            cast['character'] = datas['cast'][i]['character']
                        else:
                            cast['character'] = nodata
                        
                    elif datas['cast'][i]['media_type'] == "tv":
                        if datas['cast'][i]['name']:
                            cast['contentNm'] = datas['cast'][i]['name']
                        else:
                            cast['contentNm'] = nodata
                            
                        if datas['cast'][i]['original_name']:
                            cast['originalNm'] = datas['cast'][i]['original_name']
                        else:
                            cast['originalNm'] = nodata
                        
                        if datas['cast'][i]['first_air_date'] :
                            cast['release_date'] = datas['cast'][i]['first_air_date']
                        else :
                            cast['release_date'] = nodata
                            
                        if datas['cast'][i]['poster_path']:
                            cast['poster'] = poster_url + datas['cast'][i]['poster_path']
                        else:
                            cast['poster'] = noimage
                            
                        if datas['cast'][i]['backdrop_path']:
                            cast['backdrop'] = poster_url + datas['cast'][i]['backdrop_path']
                        else:
                            cast['backdrop'] = noimage
                            
                        if datas['cast'][i]['character']:
                            cast['character'] = datas['cast'][i]['character']
                        else:
                            cast['character'] = nodata
                        
                    else :
                        cast['contentNm'] = nodata
                        cast['originalNm'] = nodata
                        cast['release_date'] = nodata
                        cast['character'] = nodata
                        cast['poster'] = noimage
                        cast['backdrop'] = noimage
                        
                else: 
                    cast['media_type'] = nodata
                    cast['contentNm'] = nodata
                    cast['originalNm'] = nodata
                    cast['release_date'] = nodata
                    cast['character'] = nodata
                    cast['poster'] = noimage
                    cast['backdrop'] = noimage
                
                casts.append(cast)
                      
        if datas['crew']:
            for i in range(len(datas['crew'])):
                crew = {}
                if datas['crew'][i]['id']:
                    crew['contentCd'] = datas['crew'][i]['id']
                else:
                    crew['contentCd'] = nodata
                
                if datas['crew'][i]['media_type']:
                    crew['media_type'] = datas['crew'][i]['media_type']
                    
                    if datas['crew'][i]['media_type'] == "movie":
                        if datas['crew'][i]['title']:
                            crew['contentNm'] = datas['crew'][i]['title']
                        else:
                            cast['contentNm'] = nodata
                        
                        if datas['crew'][i]['original_title']:
                            crew['originalNm'] = datas['crew'][i]['original_title']
                        else:
                            crew['originalNm'] = nodata
                            
                        if datas['crew'][i]['release_date'] :
                            crew['release_date'] = datas['crew'][i]['release_date']
                        else :
                            crew['release_date'] = nodata
                            
                        if datas['crew'][i]['poster_path']:
                            crew['poster'] = poster_url + datas['crew'][i]['poster_path']
                        else:
                            crew['poster'] = noimage
                            
                        if datas['crew'][i]['backdrop_path']:
                            crew['backdrop'] = poster_url + datas['crew'][i]['backdrop_path']
                        else:
                            crew['backdrop'] = noimage
                        
                        if datas['crew'][i]['department']:
                            crew['department'] = datas['crew'][i]['department']
                        else:
                            crew['department'] = nodata
                            
                        if datas['crew'][i]['job']:
                            crew['job'] = datas['crew'][i]['job']
                        else:
                            crew['job'] = nodata
                        
                    elif datas['crew'][i]['media_type'] == "tv":
                        if datas['crew'][i]['name']:
                            crew['contentNm'] = datas['crew'][i]['name']
                        else:
                            crew['contentNm'] = nodata
                            
                        if datas['crew'][i]['original_name']:
                            crew['originalNm'] = datas['crew'][i]['original_name']
                        else:
                            crew['originalNm'] = nodata
                        
                        if datas['crew'][i]['first_air_date'] :
                            crew['release_date'] = datas['crew'][i]['first_air_date']
                        else :
                            crew['release_date'] = nodata
                            
                        if datas['crew'][i]['poster_path']:
                            crew['poster'] = poster_url + datas['crew'][i]['poster_path']
                        else:
                            crew['poster'] = noimage
                            
                        if datas['crew'][i]['backdrop_path']:
                            crew['backdrop'] = poster_url + datas['crew'][i]['backdrop_path']
                        else:
                            crew['backdrop'] = noimage
                            
                        if datas['crew'][i]['department']:
                            crew['department'] = datas['crew'][i]['department']
                        else:
                            crew['department'] = nodata
                            
                        if datas['crew'][i]['job']:
                            crew['job'] = datas['crew'][i]['job']
                        else:
                            crew['job'] = nodata
                        
                    else :
                        cast['contentNm'] = nodata
                        cast['originalNm'] = nodata
                        cast['release_date'] = nodata
                        crew['department'] = nodata
                        crew['job'] = nodata
                        cast['poster'] = noimage
                        cast['backdrop'] = noimage
                        
                else: 
                    cast['media_type'] = nodata
                    cast['contentNm'] = nodata
                    cast['originalNm'] = nodata
                    cast['release_date'] = nodata
                    crew['department'] = nodata
                    crew['job'] = nodata
                    cast['poster'] = noimage
                    cast['backdrop'] = noimage
                
                crews.append(crew)    
         
        credit['cast'] = casts
        credit['crew'] = crews
            
    else:
        if datas['cast']:
            for i in range(len(datas['cast'])):
                cast = {}
                if datas['cast'][i]['id']:
                    cast['actorCd'] = datas['cast'][i]['id']
                else:
                    cast['actorCd'] = nodata
                    
                if datas['cast'][i]['name']:
                    cast['actorNm'] = datas['cast'][i]['name']
                else:
                    cast['actorNm'] = nodata
                
                if datas['cast'][i]['character']:
                    cast['character'] = datas['cast'][i]['character']
                else:
                    cast['character'] = nodata
                    
                if datas['cast'][i]['profile_path']:
                    cast['profile'] = poster_url + datas['cast'][i]['profile_path']
                else:
                    cast['profile'] = noimage
                    
                casts.append(cast)
        if datas['crew']:
            for i in range(len(datas['crew'])):
                crew = {}
                if datas['crew'][i]['id']:
                    crew['crewCd'] = datas['crew'][i]['id']
                else:
                    crew['crewCd'] = nodata
                    
                if datas['crew'][i]['name']: 
                    crew['crewNm'] = datas['crew'][i]['name']
                else:
                    crew['crewNm'] = nodata
                    
                if datas['crew'][i]['profile_path']:
                    crew['profile'] = poster_url + datas['crew'][i]['profile_path']
                else:
                    crew['profile'] = noimage
                    
                if datas['crew'][i]['department']:
                    crew['department'] = datas['crew'][i]['department']
                else:
                    crew['department'] = nodata
                      
                if datas['crew'][i]['job']:
                    crew['job'] = datas['crew'][i]['job']
                else:
                    crew['job'] = nodata
                crews.append(crew)
                
        credit['cast'] = casts
        credit['crew'] = crews
    
    return credit


# 인데스 페이지 영화인 필모
def indexPeople(name):
    peoples = []
    person = searchDb("person", name)['results']
    for i in range(len(person)):
        p_dict = {}
        
        filmos = []
        if person[i]['id']:
            p_dict['peopleCd'] = person[i]['id']
        else:
            p_dict['peopleCd'] = nodata
            
        if person[i]['name']:
            p_dict['peopleNm'] = person[i]['name']
        else:
            p_dict['peopleNm'] = nodata
            
        if person[i]['known_for_department']:
            p_dict['role'] = person[i]['known_for_department']
        else:
            p_dict['role'] = nodata
        
        if person[i]['profile_path']: 
            p_dict['profile'] = poster_url + person[i]['profile_path']
        else:
            p_dict['profile'] = noimage
        if len(person[i]['known_for']) > 0: 
            for j in range(len(person[i]['known_for'])):
                f_dict = {}
                
                if person[i]['known_for'][j]['media_type']:
                    f_dict['media_type'] = person[i]['known_for'][j]['media_type']
                else:
                    f_dict['media_type'] = nodata
                
                if person[i]['known_for'][j]['id']:
                    f_dict['contentCd'] = person[i]['known_for'][j]['id']
                else:
                    f_dict['contentCd'] = nodata
                
                if(f_dict['media_type'] == "movie"):
                    if person[i]['known_for'][j]['title']:
                        f_dict['contentNm'] = person[i]['known_for'][j]['title']
                    else:
                        f_dict['contentNm'] = nodata
                    
                    if person[i]['known_for'][j]['poster_path']:
                        f_dict['poster'] = poster_url + person[i]['known_for'][j]['poster_path']
                    else:
                        f_dict['poster'] = noimage
                        
                    if person[i]['known_for'][j]['release_date']:
                        f_dict['release_date'] = person[i]['known_for'][j]['release_date']
                    else:
                        f_dict['release_date'] = nodata
                        
                elif (f_dict['media_type'] == "tv"):
                    if person[i]['known_for'][j]['name']:
                        f_dict['contentNm'] = person[i]['known_for'][j]['name']
                    else:
                        f_dict['contentNm'] = nodata
                    
                    if person[i]['known_for'][j]['poster_path']:
                        f_dict['poster'] = poster_url + person[i]['known_for'][j]['poster_path']
                    else:
                        f_dict['poster'] = nodata
                        
                    if person[i]['known_for'][j]['first_air_date']:
                        f_dict['release_date'] = person[i]['known_for'][j]['first_air_date']
                    else:
                        f_dict['release_date'] = nodata
                else:
                    f_dict['contentNm'] = nodata
                    f_dict['poster'] = noimage
                    f_dict['release_date'] = nodata
                filmos.append(f_dict)
                
            p_dict['filmos'] = filmos
        else:
            pass
        peoples.append(p_dict)
    return peoples


# 인덱스 페이지 인기 순위
def indexPopular(media_type):
    populars = []
    popular = getPopular(media_type)['results']
    
    if media_type == "movie":
        for i in range(len(popular)):
            pm_dict = {}
            pm_dict["media_type"] = "movie"
            
            if popular[i]['id']:
                pm_dict['contentCd'] = popular[i]['id']
            else:
                pm_dict['contentCd'] = nodata
                
            if popular[i]['title']:
                pm_dict['contentNm'] = popular[i]['title']
            else:
                pm_dict['contentNm'] = nodata
                
            pm_dict['rank'] = i + 1
            
            if popular[i]['poster_path']:
                pm_dict['poster'] = poster_url + popular[i]['poster_path']
            else:
                pm_dict['poster'] = noimage
            
            if popular[i]['release_date']:
                pm_dict['release_date'] = popular[i]['release_date']
            else:
                pm_dict['release_date'] = nodata
                
            populars.append(pm_dict)
            
    elif media_type == "tv":
        for i in range(len(popular)):
            pt_dict = {}
            pt_dict["media_type"] = "tv"
            
            if popular[i]['id']:
                pt_dict['contentCd'] = popular[i]['id']
            else:
                pt_dict['contentCd'] = nodata
            
            if popular[i]['name']:
                pt_dict['contentNm'] = popular[i]['name']
            else: 
                pt_dict['contentNm'] = nodata
                
            pt_dict['rank'] = i + 1
            
            if popular[i]['poster_path']:
                pt_dict['poster'] = poster_url + popular[i]['poster_path']
            else:
                pt_dict['poster'] = noimage
            
            if popular[i]['first_air_date']:
                pt_dict['release_date'] = popular[i]['first_air_date']
            else:
                pt_dict['release_date'] = nodata
                
            populars.append(pt_dict)
            
    return populars


# 해당 프로그램 세부정보 불러오기
def getDetail(media_type, contentId, language="ko-KR"):
    # get_type은 영상 종류(movie,tv...) get_id(세부정보를 찾고싶은 id) 반드시 기입.
    contentId = str(contentId)
    url = "https://api.themoviedb.org/3/" + media_type + "/" + contentId + "?api_key=" + api_key + "&language=" + language
    rq = requests.get(url)
    t = rq.text
    data = json.loads(t)
    
    result = {}
    genre = ""
    genreCd = []
    company = ""
    companyCd = []
    country = ""
    countryCd = []
    network = ""
    networkCd = []
    
    if media_type == "movie":
        credit = getCredit(media_type, contentId)
        if data['id']:
            result['contentCd'] = data['id']
        else:
            result['contentCd'] = nodata
            
        if data['title']:
            result['contentNm'] = data['title']
        else:
            result['contentNm'] = nodata
            
        if data['original_title']:
            result['originalNm'] = data['original_title']
        else:
            result['originalNm'] = nodata
            
        if data['status']:
            result['status'] = data['status']
        else: 
            result['status'] = nodata
            
        if data['release_date']:
            result['release_date'] = data['release_date']
        else:
            result['release_date'] = nodata
        
        if data['runtime']:
            result['runtime'] = data['runtime']
        else:
            result['runtime'] = 0
        
        if data['tagline']:
            result['tagline'] = data['tagline']
        else:
            result['tagline'] = nodata
        
        if data['overview']:
            result['overview'] = data['overview']
        else: 
            result['overview'] = nodata
        
        if data['poster_path']:
            result['poster'] = poster_url + data['poster_path']
        else:
            result['poster'] = noimage
            
        if data['backdrop_path']:
            result['backdrop'] = poster_url + data['backdrop_path']
        else: 
            result['backdrop'] = noimage
        
        if data['homepage']:
            result['homepage'] = data['homepage']
        else:
            result['homepage'] = nodata
        
        if data['genres']:
            for i in range(len(data['genres'])):
                genreCd.append(data['genres'][i]['id'])
                genre += " , " + data['genres'][i]['name']
            result['genreCd'] = genreCd
            result['genre'] = genre[3:]
        else:
            result['genreCd'] = nodata
            result['genre'] = nodata
        
        if data['production_companies']:
            for i in range(len(data['production_companies'])):
                companyCd.append(data['production_companies'][i]['id'])
                company += " | " + data['production_companies'][i]['name']
            result['companyCd'] = companyCd
            result['company'] = company[3:]
        else:
            result['companyCd'] = nodata
            result['company'] = nodata
        
        if data['production_countries']:
            for i in range(len(data['production_countries'])):
                countryCd.append(data['production_countries'][i]['iso_3166_1'])
                country += " | " + data['production_countries'][i]['name']
            result['countryCd'] = countryCd
            result['country'] = country[3:]
        else:
            result['countryCd'] = nodata
            result['country'] = nodata
        
        if data['belongs_to_collection']:
            if data['belongs_to_collection']['id']:
                result['seriesCd'] = data['belongs_to_collection']['id']
            else: 
                result['seriesCd'] = nodata
            
            if data['belongs_to_collection']['name']:
                result['seriesNm'] = data['belongs_to_collection']['name']
            else:
                result['seriesNm'] = nodata
                
            if data['belongs_to_collection']['poster_path']:
                result['poster'] = poster_url + data['belongs_to_collection']['poster_path']
            else:
                result['poster'] = noimage
                
            if data['belongs_to_collection']['backdrop_path']:
                result['backdrop'] = poster_url + data['belongs_to_collection']['backdrop_path']
            else: 
                result['backdrop'] = noimage
        else:
            result['seriesCd'] = nodata
            result['seriesNm'] = nodata
            result['poster'] = noimage
            result['backdrop'] = noimage
        
        result['cast'] = credit['cast']
        result['crew'] = credit['crew']
        
    elif media_type == "tv":
        credit = getCredit(media_type, contentId)
        if data['id']:
            result['contentCd'] = data['id']
        else:
            result['contentCd'] = nodata
        
        if data['name']:
            result['contentNm'] = data['name']
        else:
            result['contentNm'] = nodata
        
        if data['original_name']:
            result['originalNm'] = data['original_name']
        else:
            result['originalNm'] = nodata
        
        if data['status']:
            result['status'] = data['status']
        else:
            result['status'] = nodata
        
        if data['number_of_episodes']:
            result['number_of_episodes'] = data['number_of_episodes']
        else:
            result['number_of_episodes'] = 0
        
        if data['number_of_seasons']:
            result['number_of_seasons'] = data['number_of_seasons']
        else: 
            result['number_of_seasons'] = 0
        
        if data['first_air_date']:
            result['release_date'] = data['first_air_date']
        else:
            result['release_date'] = nodata
        
        if data['tagline']:
            result['tagline'] = data['tagline']
        else:
            result['tagline'] = nodata
            
        if data['overview']:
            result['overview'] = data['overview']
        else:
            result['overview'] = nodata
        
        if data['poster_path']:
            result['poster'] = poster_url + data['poster_path']
        else:
            result['poster'] = noimage
            
        if data['backdrop_path']:
            result['backdrop'] = poster_url + data['backdrop_path']
        else: 
            result['backdrop'] = noimage
        
        if data['homepage']:
            result['homepage'] = data['homepage']
        else:
            result['homepage'] = nodata
        
        if data['genres']:
            for i in range(len(data['genres'])):
                genreCd.append(data['genres'][i]['id'])
                genre += " , " + data['genres'][i]['name']
            result['genreCd'] = genreCd
            result['genre'] = genre[3:]
        else:
            result['genreCd'] = nodata
            result['genre'] = nodata
        
        if data['production_companies']:
            for i in range(len(data['production_companies'])):
                companyCd.append(data['production_companies'][i]['id'])
                company += " | " + data['production_companies'][i]['name']
            result['companyCd'] = companyCd
            result['company'] = company[3:]
        else:
            result['companyCd'] = nodata
            result['company'] = nodata
        
        if data['production_countries']:
            for i in range(len(data['production_countries'])):
                countryCd.append(data['production_countries'][i]['iso_3166_1'])
                country += " | " + data['production_countries'][i]['name']
            result['countryCd'] = countryCd
            result['country'] = country[3:]
        else:
            result['countryCd'] = nodata
            result['country'] = nodata
        
        if data['networks']:
            for i in range(len(data['networks'])):
                network += " , " + data['networks'][i]['name']
                networkCd.append(data['networks'][i]['id'])
            result['networkCd'] = networkCd
            result['network'] = network[3:]
        else:
            result['networkCd'] = nodata
            result['network'] = nodata
        
        result['cast'] = credit['cast']
        result['crew'] = credit['crew']
    
    elif media_type == "person":
        credit = getCredit(media_type, contentId)
        
        if data['id']:
            result['peopleCd'] = data['id']
        else:
            result['peopleCd'] = nodata
        
        if data['name']:
            result['peopleNm'] = data['name']
        else:
            result['peopleNm'] = nodata
            
        if data['gender']:
            if data['gender'] == 0:
                result['gender'] = "명시되지 않음"
            elif data['gender'] == 1:
                result['gender'] = "여자"
            elif data['gender'] == 2:
                result['gender'] = "남자"
            else:
                result['gender'] = "해당없음"
        else:
            result['gender'] = nodata
            
        if data['birthday']:
            result['birthday'] = data['birthday']
        else:
            result['birthday'] = nodata
            
        if data['deathday']:
            result['deathday'] = data['deathday']
        else:
            result['deathday'] = nodata
        
        if data['place_of_birth']:
            result['birth_place'] = data['place_of_birth'] 
        else:
            result['birth_place'] = nodata
        
        if data['known_for_department']:
            result['department'] = data['known_for_department']
        else:
            result['department'] = nodata
        
        if data['profile_path']:
            result['profile'] = poster_url + data['profile_path']
        else:
            result['profile'] = noimage
            
        if data['homepage']:
            result['homepage'] = data['homepage']
        else:
            result['homopage'] = nodata
            
        if data['also_known_as']:
            result['known'] = data['also_known_as']
        else:
            result['known'] = nodata
            
        result['cast'] = credit['cast']
        result['crew'] = credit['crew']
    
    return result


def searchResultPage(media_type, query, pages, language="ko-KR"):
    url = "https://api.themoviedb.org/3/search/" + media_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language + "&page=" + pages
    rq = requests.get(url)
    t = rq.text
    results = json.loads(t)

    if results['results']:
        idata = results['results']
        datas = []
        for y in range(len(idata)):
            data = {}
            if media_type == "movie":
                if nodata:
                    data['contentCd'] = idata[y]['id']
                else:
                    data['contentCd'] = nodata
                    
                data['media_type'] = media_type
                
                if idata[y]['title']:
                    data['contentNm'] = idata[y]['title']
                else:
                    data['contentNm'] = nodata
                
                if idata[y]['original_title']:
                    data['originalNm'] = idata[y]['original_title']
                else:
                    data['originalNm'] = nodata
                
                if 'release_date' in idata[y]:
                    data['release_date'] = idata[y]['release_date']
                else:
                    data['release_date'] = nodata
                    
                if idata[y]['genre_ids']:
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                else:
                    data['genre'] = nodata
                
                if idata[y]['overview']:
                    data['overview'] = idata[y]['overview']
                else:
                    data['overview'] = nodata
                    
                if idata[y]['poster_path']:
                    data['poster'] = poster_url + idata[y]['poster_path']
                else:
                    data['poster'] = noimage

            elif media_type == "tv":
                if idata[y]['id']:
                    data['contentCd'] = idata[y]['id']
                else:
                    data['contentCd'] = nodata
                    
                data['media_type'] = media_type
                
                if idata[y]['name']:
                    data['contentNm'] = idata[y]['name']
                else: 
                    data['contentNm'] = nodata
                
                if idata[y]['original_name']:
                    data['originalNm'] = idata[y]['original_name']
                else:
                    data['originalNm'] = nodata
                
                if idata[y]['first_air_date']:
                    data['release_date'] = idata[y]['first_air_date']
                else:
                    data['release_date'] = nodata
                
                if idata[y]['genre_ids']:
                    data['genre'] = getGenre(idata[y]['genre_ids'])
                else: 
                    data['genre']
                
                if idata[y]['overview']:
                    data['overview'] = idata[y]['overview']
                else:
                    data['overview'] = nodata
                    
                if idata[y]['poster_path']:
                    data['poster'] = poster_url + idata[y]['poster_path']
                else:
                    data['poster'] = noimage
            
            elif media_type == "person":
                if idata[y]['id']:
                    data['peopleCd'] = idata[y]['id']
                else:
                    data['peopleCd'] = nodata
                
                data['media_type'] = media_type
                
                if idata[y]['name']:
                    data['peopleNm'] = idata[y]['name']
                else:
                    data['peopleNm'] = nodata
                
                if idata[y]['profile_path']:
                    data['profile'] = poster_url + idata[y]['profile_path']
                else:
                    data['profile'] = noimage
                    
                if idata[y]['known_for']:
                    filmoCd = []
                    filmoNm = ""
                    for z in range(len(idata[y]['known_for'])):
                        if idata[y]['known_for'][z]['media_type'] == "movie":
                            if idata[y]['known_for'][z]['id']:
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                            else: 
                                pass
                            if idata[y]['known_for'][z]['title']:
                                if idata[y]['known_for'][z]['release_date']:
                                    filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                                else:
                                    filmoNm += "|" + idata[y]['known_for'][z]['title']
                            else:
                                pass
                        elif idata[y]['known_for'][z]['media_type'] == "tv":
                            if idata[y]['known_for'][z]['id']:
                                filmoCd.append(idata[y]['known_for'][z]['id'])
                            else:
                                pass
                            if idata[y]['known_for'][z]['name']:
                                if idata[y]['known_for'][z]['first_air_date']:
                                    filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                                else:
                                    filmoNm += " | " + idata[y]['known_for'][z]['name']
                            else:
                                pass
                            
                    if len(filmoCd) > 0:
                        data['filmoCd'] = filmoCd 
                    else:
                        data['filmoCd'] = nodata
                        
                    if len(filmoNm) > 0:
                        data['filmoNm'] = filmoNm[3:]
                    else:
                        data['filmoNm'] = nodata
                        
            else:
                pass
            
            datas.append(data)
    
    return datas


def searchResultSimple (media_type, query, language="ko-KR"):
    url = "https://api.themoviedb.org/3/search/" + media_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language
    rq = requests.get(url)
    t = rq.text
    results = json.loads(t)

    if results['results']:
        idata = results['results']
        datas = []
        
        if len(idata) < 5:
            for y in range(len(idata)):
                data = {}
                if media_type == "movie":
                    if idata[y]['id']:
                        data['contentCd'] = idata[y]['id']
                    else:
                        data['contentCd'] = nodata
                        
                    data['media_type'] = media_type
                    
                    if idata[y]['title']:
                        data['contentNm'] = idata[y]['title']
                    else:
                        data['contentNm'] = nodata
                        
                    if idata[y]['original_title']:
                        data['originalNm'] = idata[y]['original_title']
                    else:
                        data['originalNm'] = nodata
                        
                    if 'release_date' in idata[y]:
                        data['release_date'] = idata[y]['release_date']
                    else:
                        data['release_date'] = nodata
                    
                    if idata[y]['genre_ids']:
                        data['genre'] = getGenre(idata[y]['genre_ids'])
                    else:
                        data['genre'] = nodata
                    
                    if idata[y]['overview']:
                        data['overview'] = idata[y]['overview']
                    else: 
                        data['overview'] = nodata
                        
                    if idata[y]['poster_path']:
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
    
                elif media_type == "tv":
                    if idata[y]['id']:
                        data['contentCd'] = idata[y]['id']
                    else:
                        data['contentCd'] = nodata
                    
                    data['media_type'] = media_type
                    
                    if idata[y]['name']:
                        data['contentNm'] = idata[y]['name']
                    else:
                        data['contentNm'] = nodata
                    
                    if idata[y]['original_name']:
                        data['originalNm'] = idata[y]['original_name']
                    else:
                        data['originalNm'] = nodata
                        
                    if idata[y]['first_air_date']:
                        data['release_date'] = idata[y]['first_air_date']
                    else:
                        data['release_date'] = nodata
                        
                    if idata[y]['genre_ids']:
                        data['genre'] = getGenre(idata[y]['genre_ids'])
                    else:
                        data['genre'] = nodata
                        
                    if idata[y]['overview']:
                        data['overview'] = idata[y]['overview']
                    else: 
                        data['overview'] = nodata
                        
                    if idata[y]['poster_path']:
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
                
                elif media_type == "person":
                    if idata[y]['id']:
                        data['peopleCd'] = idata[y]['id']
                    else:
                        data['peopleCd'] = nodata
                    
                    data['media_type'] = media_type
                    
                    if idata[y]['name']:
                        data['peopleNm'] = idata[y]['name']
                    else:
                        data['peopleNm'] = nodata
                        
                    if idata[y]['profile_path']:
                        data['profile'] = poster_url + idata[y]['profile_path']
                    else:
                        data['profile'] = noimage
                        
                    if idata[y]['known_for']:
                        filmoCd = []
                        filmoNm = ""
                        for z in range(len(idata[y]['known_for'])):
                            if idata[y]['known_for'][z]['media_type'] == "movie":
                                if idata[y]['known_for'][z]['id']:
                                    filmoCd.append(idata[y]['known_for'][z]['id'])
                                else:
                                    pass
                                
                                if idata[y]['known_for'][z]['title']:
                                    if idata[y]['known_for'][z]['release_date']:
                                        filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                                    else:
                                        filmoNm += "|" + idata[y]['known_for'][z]['title']
                                else:
                                    pass
                                
                            elif idata[y]['known_for'][z]['media_type'] == "tv":
                                if idata[y]['known_for'][z]['id']:
                                    filmoCd.append(idata[y]['known_for'][z]['id'])
                                else:
                                    pass
                                
                                if idata[y]['known_for'][z]['name']:
                                    if idata[y]['known_for'][z]['first_air_date']:
                                        filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                                    else:
                                        filmoNm += " | " + idata[y]['known_for'][z]['name']
                                else:
                                    pass
                        if len(filmoCd) > 0:
                            data['filmoCd'] = filmoCd 
                        else:
                            data['filmoCd'] = nodata
                            
                        if len(filmoNm) > 0:
                            data['filmoNm'] = filmoNm[3:]
                        else:
                            data['filmoNm'] = nodata
                            
                else:
                    pass
                datas.append(data)
                
        else:
            for y in range(0, 5):
                data = {}
                if media_type == "movie":
                    if idata[y]['id']:
                        data['contentCd'] = idata[y]['id']
                    else:
                        data['contentCd'] = nodata
                    
                    data['media_type'] = media_type
                    
                    if idata[y]['title']:
                        data['contentNm'] = idata[y]['title']
                    else: 
                        data['contentNm'] = nodata
                        
                    if idata[y]['original_title']:
                        data['originalNm'] = idata[y]['original_title']
                    else:
                        data['originalNm'] = nodata
                        
                    if 'release_date' in idata[y]:
                        data['release_date'] = idata[y]['release_date']
                    else:
                        data['release_date'] = nodata
                        
                    if idata[y]['genre_ids']:
                        data['genre'] = getGenre(idata[y]['genre_ids'])
                    else:
                        data['genre'] = nodata
                        
                    if idata[y]['overview']:
                        data['overview'] = idata[y]['overview']
                    else:
                        data['overview'] = nodata
                        
                    if idata[y]['poster_path']:
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
    
                elif media_type == "tv":
                    if idata[y]['id']:
                        data['contentCd'] = idata[y]['id']
                    else:
                        data['contentCd'] = nodata
                        
                    data['media_type'] = media_type
                    
                    if idata[y]['name']:
                        data['contentNm'] = idata[y]['name']
                    else:
                        data['contentNm'] = nodata
                        
                    if idata[y]['original_name']:
                        data['originalNm'] = idata[y]['original_name']
                    else: 
                        data['originalNm'] = nodata
                        
                    if idata[y]['first_air_date']:
                        data['release_date'] = idata[y]['first_air_date']
                    else: 
                        data['release_date'] = nodata
                        
                    if idata[y]['genre_ids']:
                        data['genre'] = getGenre(idata[y]['genre_ids'])
                    else: 
                        data['genre'] = nodata
                    
                    if idata[y]['overview']:
                        data['overview'] = idata[y]['overview']
                    else:
                        data['overview'] = nodata
                        
                    if idata[y]['poster_path']:
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
                
                elif media_type == "person":
                    if idata[y]['id']:
                        data['peopleCd'] = idata[y]['id']
                    else:
                        data['peopleCd'] = nodata
                        
                    data['media_type'] = media_type
                    
                    if idata[y]['name']:
                        data['peopleNm'] = idata[y]['name']
                    else:
                        data['peopleNm'] = nodata
                        
                    if idata[y]['profile_path']:
                        data['profile'] = poster_url + idata[y]['profile_path']
                    else:
                        data['profile'] = noimage
                        
                    if idata[y]['known_for']:
                        filmoCd = []
                        filmoNm = ""
                        for z in range(len(idata[y]['known_for'])):
                            if idata[y]['known_for'][z]['media_type'] == "movie":
                                if idata[y]['known_for'][z]['id']:
                                    filmoCd.append(idata[y]['known_for'][z]['id'])
                                else:
                                    pass
                                
                                if idata[y]['known_for'][z]['title']:
                                    if idata[y]['known_for'][z]['release_date']:
                                        filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                                    else:
                                        filmoNm += "|" + idata[y]['known_for'][z]['title']
                                else:
                                    pass
                                
                            elif idata[y]['known_for'][z]['media_type'] == "tv":
                                if idata[y]['known_for'][z]['id']:
                                    filmoCd.append(idata[y]['known_for'][z]['id'])
                                else:
                                    pass
                                
                                if idata[y]['known_for'][z]['name']:
                                    if idata[y]['known_for'][z]['first_air_date']:
                                        filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                                    else:
                                        filmoNm += " | " + idata[y]['known_for'][z]['name']
                                else:
                                    pass
                        
                        if len(filmoCd) > 0:
                            data['filmoCd'] = filmoCd 
                        else:
                            data['filmoCd'] = nodata
                        
                        if len(filmoNm) > 0:
                            data['filmoNm'] = filmoNm[3:]
                        else:
                            data['filmoNm'] = nodata
                            
                else:
                    pass
                
                datas.append(data)
                
        return datas


def searchResultAll(media_type, query, language="ko-KR"):
    pages = getPage(media_type, query)
    datas = []
    for i in range(1, pages + 1):
        url = "https://api.themoviedb.org/3/search/" + media_type + "?api_key=" + api_key + "&query=" + query + "&language=" + language + "&page=" + str(i)
        rq = requests.get(url)
        t = rq.text
        results = json.loads(t)
        
        if results['results']:
            idata = results['results']
            for y in range(len(idata)):
                data = {}
                if media_type == "movie":
                    if idata[y]['id']:
                        data['contentCd'] = idata[y]['id']
                    else:
                        data['contentCd'] = nodata
                        
                    data['media_type'] = media_type
                    
                    if idata[y]['title']:
                        data['contentNm'] = idata[y]['title']
                    else:
                        data['contentNm'] = nodata
                    
                    if idata[y]['original_title']:
                        data['originalNm'] = idata[y]['original_title']
                    else:
                        data['originalNm'] = nodata
                        
                    if 'release_date' in idata[y]:
                        data['release_date'] = idata[y]['release_date']
                    else:
                        data['release_date'] = nodata
                    
                    if idata[y]['genre_ids']:
                        data['genre'] = getGenre(idata[y]['genre_ids'])
                    else: 
                        data['genre'] = nodata
                        
                    if idata[y]['overview']:
                        data['overview'] = idata[y]['overview']
                    else:
                        data['overview'] = nodata
                        
                    if idata[y]['poster_path']:
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
    
                elif media_type == "tv":
                    if idata[y]['id']:
                        data['contentCd'] = idata[y]['id']
                    else:
                        data['contentCd'] = nodata
                    
                    data['media_type'] = media_type
                    
                    if idata[y]['name']:
                        data['contentNm'] = idata[y]['name']
                    else: 
                        data['contentNm'] = nodata
                        
                    if idata[y]['original_name']:
                        data['originalNm'] = idata[y]['original_name']
                    else:
                        data['originalNm'] = nodata
                    
                    if idata[y]['first_air_date']:
                        data['release_date'] = idata[y]['first_air_date']
                    else:
                        data['release_date'] = nodata
                    
                    if idata[y]['genre_ids']:
                        data['genre'] = getGenre(idata[y]['genre_ids'])
                    else:
                        data['genre'] = nodata
                    
                    if idata[y]['overview']:
                        data['overview'] = idata[y]['overview']
                    else:
                        data['overview'] = nodata
                        
                    if idata[y]['poster_path']:
                        data['poster'] = poster_url + idata[y]['poster_path']
                    else:
                        data['poster'] = noimage
                
                elif media_type == "person":
                    if idata[y]['id']:
                        data['peopleCd'] = idata[y]['id']
                    else:
                        data['peopleCd'] = nodata
                        
                    data['media_type'] = media_type
                    
                    if idata[y]['name']:
                        data['peopleNm'] = idata[y]['name']
                    else:
                        data['peopleNm'] = nodata
                        
                    if idata[y]['profile_path']:
                        data['profile'] = poster_url + idata[y]['profile_path']
                    else:
                        data['profile'] = noimage
                        
                    if idata[y]['known_for']:
                        filmoCd = []
                        filmoNm = ""
                        for z in range(len(idata[y]['known_for'])):
                            if idata[y]['known_for'][z]['media_type'] == "movie":
                                if idata[y]['known_for'][z]['id']:
                                    filmoCd.append(idata[y]['known_for'][z]['id'])
                                else:
                                    pass
                                
                                if idata[y]['known_for'][z]['title']:
                                    if idata[y]['known_for'][z]['release_date']:
                                        filmoNm += "|" + idata[y]['known_for'][z]['title'] + "(" + idata[y]['known_for'][z]['release_date'][:4] + ")"
                                    else:
                                        filmoNm += "|" + idata[y]['known_for'][z]['title']
                                else:
                                    pass
                                
                            elif idata[y]['known_for'][z]['media_type'] == "tv":
                                if idata[y]['known_for'][z]['id']:
                                    filmoCd.append(idata[y]['known_for'][z]['id'])
                                else:
                                    pass
                                
                                if idata[y]['known_for'][z]['name']:
                                    if idata[y]['known_for'][z]['first_air_date']:
                                        filmoNm += " | " + idata[y]['known_for'][z]['name'] + "(" + idata[y]['known_for'][z]['first_air_date'][:4] + ")"
                                    else:
                                        filmoNm += " | " + idata[y]['known_for'][z]['name']
                                else:
                                    pass
                        
                        if len(filmoCd) > 0:
                            data['filmoCd'] = filmoCd 
                        else:
                            data['filmoCd'] = nodata
                        
                        if len(filmoNm) > 0:
                            data['filmoNm'] = filmoNm[3:]
                        else:
                            data['filmoNm'] = nodata
                            
                else:
                    pass
                
                datas.append(data)
    
    return datas


def test():
    url = "https://api.themoviedb.org/3/person/1294471/combined_credits?api_key=" + api_key + "&language=ko-KR"
    rq = requests.get(url)
    t = rq.text
    results = json.loads(t)
    
    return results

# print(getDetail("person", "73249"))