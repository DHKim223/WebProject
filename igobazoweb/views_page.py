from django.shortcuts import render, redirect
import logging
from django.http.response import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.dateformat import DateFormat
from IGOBAZO.settings import PAGE_SIZE, PAGE_BLOCK
from igobazoweb.models import Review, Album, People, Movie, Tv, ctCast, ctCrew,\
    mvSeries, tvNetworks, ctGenre, ctCompany, ctCountry, TvLike, MovieLike,\
    PeopleLike
from igobazoweb import tmdb

logger = logging.getLogger(__name__)
now = datetime.now().strftime('%Y:%m:%d:%H:%M:%S')

@csrf_exempt
def index( request ) :
    template = loader.get_template( "index.html" )
    id = request.session.get("id")
    review_cnt = Review.objects.all().count()
    context = {
        "movies" : tmdb.indexPopular("movie"),
        "tvs" : tmdb.indexPopular("tv"),
        "actor" : tmdb.indexPeople("이정재")[0]['filmos'],
        "director" : tmdb.indexPeople("황동혁")[0]['filmos'],
        "review_cnt" : review_cnt,
        "id" : id,
    }
     
    return HttpResponse( template.render( context, request ) )

@csrf_exempt
def searchpro(request):
    id = request.session.get("id")
    query = request.GET.get("barbar")
    logger.info(id,query,now)
    movies = tmdb.searchResultSimple("movie", query)
    if movies is None :
        m_cnt = 0
    else :
        m_cnt = len(tmdb.searchResultAll("movie", query))
    tvs = tmdb.searchResultSimple("tv", query)
    if tvs is None :
        t_cnt = 0
    else : 
        t_cnt = len(tmdb.searchResultAll("tv", query))
    peoples = tmdb.searchResultSimple("person", query)
    if peoples is None :
        p_cnt = 0
    else :
        p_cnt = len(tmdb.searchResultAll("person", query))
    cnt = m_cnt + t_cnt + p_cnt
    
    template = loader.get_template( "searchpage.html" )
    context = {
        "query" : query,
        "movies" : movies,
        "tvs" : tvs,
        "peoples" : peoples,
        "id" : id,
        "cnt" : cnt,
        "m_cnt" : m_cnt,
        "t_cnt" : t_cnt,
        "p_cnt" : p_cnt,
    }
     
    return HttpResponse( template.render( context, request ) )

@csrf_exempt
def searchmore(request):
    id = request.session.get("id")
    media_type = request.GET.get("media_type")
    query = request.GET.get("query")
    cnt = request.GET.get("cnt")
    contents = []
    
    if media_type == "movie" :
        contents = tmdb.searchResultAll("movie", query)
    elif media_type == "tv" :
        contents = tmdb.searchResultAll("tv", query)
    elif media_type == "person" :
        contents = tmdb.searchResultAll("person", query)
    else :
        pass
    
    
    
    template = loader.get_template( "searchmore.html" )
    context = {
        "query" : query,
        "contents" : contents,
        "media_type" : media_type,
        "id" : id,
        "cnt" : cnt,
    }
     
    return HttpResponse( template.render( context, request ) )

def detailpage(request):
    id = request.session.get('id')
    media_type = request.GET.get("media_type")
    template = loader.get_template("detailpage.html")
    
    ## media_type is person ##
    if media_type == "person" :
        peopleCd = request.GET.get("peopleCd")
        info = tmdb.getDetail(media_type,peopleCd)
        
        if not People.objects.filter(peopleCd = peopleCd) :
            People.objects.create(
                peopleCd = peopleCd,
                peopleNm = info['peopleNm'],
                gender = info['gender'],
                birthday = info['birthday'],
                deathday = info['deathday'],
                birth_place = info['birth_place'],
                department = info['department'],
                profile = info['profile'],
                homepage = info['homepage'],
                update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                regdate = DateFormat( datetime.now() ).format("Y-m-d")
            )
            print("People DB insert")
        else : pass
        
        if info['department'] :
            if info['department'] == "Acting" :
                cast = info['cast']
                for i in range(len(cast)) :
                    if not ctCast.objects.filter(peopleCd = info['peopleCd']).filter(contentCd = cast[i]['contentCd']) :
                        ctCast.objects.create(
                            contentCd = cast[i]['contentCd'],
                            media_type = cast[i]['media_type'],
                            peopleCd = peopleCd,
                            peopleNm = info['peopleNm'],
                            character = cast[i]['character'],
                            poster = cast[i]['poster'],
                            profile = info['profile'],
                            update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                            regdate = DateFormat( datetime.now() ).format("Y-m-d")
                        )
                        print("ctCast DB insert")
                    else :pass
                    
            else :
                crew = info['crew']
                for i in range(len(crew)) :
                    if not ctCrew.objects.filter(peopleCd = peopleCd).filter(contentCd = crew[i]['contentCd']).filter(department = crew[i]['department']) :
                        ctCrew.objects.create(
                            contentCd = crew[i]['contentCd'],
                            media_type = crew[i]['media_type'],
                            peopleCd = peopleCd,
                            peopleNm = info['peopleNm'],
                            department = crew[i]['department'],
                            job = crew[i]['department'],
                            poster = crew[i]['poster'],
                            profile = info['profile'],
                            update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                            regdate = DateFormat( datetime.now() ).format("Y-m-d")
                        )
                    else :pass
                print("ctCrew DB insert") 
        else: pass
        
        like = PeopleLike.objects.filter(id = id).filter(peopleCd = peopleCd)
        print("Peoplelike import")
        
        context = {
            "id":id,
            "info" : info,
            "media_type" : media_type,
            "peopleCd" : peopleCd,
            "like" : like,
        }
    
    ## media_type is not person ##
    else :
        contentCd = request.GET.get("contentCd")
        info = tmdb.getDetail(media_type,contentCd)
        rsAlbum = Album.objects.all().filter(usage='1').filter(media_type=media_type).filter(contentCd=contentCd)
        print("reAlbum import")
        ## media_type is movie ##
        if media_type == "movie" :
            like = MovieLike.objects.filter(id = id).filter(contentCd = contentCd)
            print("MovieLike import")
            
            if not Movie.objects.filter(contentCd = contentCd) :
                Movie.objects.create(
                    contentCd = contentCd,
                    media_type = media_type,
                    contentNm = info['contentNm'],
                    originalNm = info['originalNm'],
                    status = info['status'],
                    release_date = info['release_date'],
                    runtime = info['runtime'],
                    tagline = info['tagline'],
                    overview = info['overview'],
                    poster = info['poster'],
                    backdrop = info['backdrop'],
                    homepage = info['homepage'],
                    update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                    regdate = DateFormat( datetime.now() ).format("Y-m-d")
                )
                print("Movie DB insert")
            else : pass
            
            if info['seriesCd'] :
                if not mvSeries.objects.filter(seriesCd = info['seriesCd']) :
                    mvSeries.objects.create(
                        contentCd = contentCd,
                        seriesCd = info['seriesCd'],
                        seriesNm = info['seriesNm'],
                        poster = info['poster'],
                        backdrop = info['backdrop'],
                        update_time = DateFormat( datetime.now() ).format("Y-m-d"), 
                        regdate = DateFormat( datetime.now() ).format("Y-m-d")
                    )
                    print("mvSeries DB insert")
                else : pass
            else : pass
            
            cast = info['cast']
            crew = info['crew']
            for i in range(len(cast)) :
                if not ctCast.objects.filter(contentCd = contentCd).filter(peopleCd = cast[i]['actorCd']) :
                    ctCast.objects.create(
                        contentCd = contentCd,
                        media_type = media_type,
                        peopleCd = cast[i]['actorCd'],
                        peopleNm = cast[i]['actorNm'],
                        character = cast[i]['character'],
                        poster = info['poster'],
                        profile = cast[i]['profile'],
                        update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                        regdate = DateFormat( datetime.now() ).format("Y-m-d")
                    )
                    print("ctCast DB insert")
                else : pass
            
            for i in range(len(crew)) :
                if not ctCrew.objects.filter(contentCd = contentCd).filter(peopleCd = crew[i]['crewCd']).filter(department = crew[i]['department']) :
                    ctCrew.objects.create(
                        contentCd = contentCd,
                        media_type = media_type,
                        peopleCd = crew[i]['crewCd'],
                        peopleNm = crew[i]['crewNm'],
                        department = crew[i]['department'],
                        job = crew[i]['department'],
                        poster = info['poster'],
                        profile = crew[i]['profile'],
                        update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                        regdate = DateFormat( datetime.now() ).format("Y-m-d")
                    )
                    print("ctCrew DB insert")
                else : pass
            
        ## media_type is Tv ##
        else :
            like = TvLike.objects.filter(id = id).filter(contentCd = contentCd)
            print("TvLike import")
            
            if not Tv.objects.filter(contentCd = contentCd) :
                Tv.objects.create(
                    contentCd = contentCd,
                    media_type = media_type,
                    contentNm = info['contentNm'],
                    originalNm = info['originalNm'],
                    status = info['status'],
                    number_of_seasons = info['number_of_seasons'],
                    number_of_episodes = info['number_of_episodes'],
                    release_date = info['release_date'],
                    tagline = info['tagline'],
                    overview = info['overview'],
                    poster = info['poster'],
                    backdrop = info['backdrop'],
                    homepage = info['homepage'],
                    update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                    regdate = DateFormat( datetime.now() ).format("Y-m-d")
                )
                print("Tv DB insert")
            else : pass
            
            if info['networkCd'] :
                network = info['network'].split(",")
                for i in range(len(network)) :
                    if not tvNetworks.objects.filter(networkCd = info['networkCd'][i]):
                        tvNetworks.objects.create(
                            contentCd = contentCd,
                            networkCd = info['networkCd'][i],
                            networkNm = network[i],
                            update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                            regdate = DateFormat( datetime.now() ).format("Y-m-d")
                        )
                        print("tvNetworks DB insert")
                    else: pass
                    
            else : pass
            
            if info['cast'] :
                cast = info['cast']
                for i in range(len(cast)) :
                    if not ctCast.objects.filter(contentCd = contentCd).filter(peopleCd = cast[i]['actorCd']) :
                        ctCast.objects.create(
                            contentCd = contentCd,
                            media_type = media_type,
                            peopleCd = cast[i]['actorCd'],
                            peopleNm = cast[i]['actorNm'],
                            character = cast[i]['character'],
                            poster = info['poster'],
                            profile = cast[i]['profile'],
                            update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                            regdate = DateFormat( datetime.now() ).format("Y-m-d")
                        )
                        print("ctCast DB insert")
                    else : pass
                    
            else: pass
                
            if info['crew'] :
                crew = info['crew']
                for i in range(len(crew)) :
                    if not ctCrew.objects.filter(contentCd = contentCd).filter(peopleCd = crew[i]['crewCd']).filter(department = crew[i]['department']) :
                        ctCrew.objects.create(
                            contentCd = contentCd,
                            media_type = media_type,
                            peopleCd = crew[i]['crewCd'],
                            peopleNm = crew[i]['crewNm'],
                            department = crew[i]['department'],
                            job = crew[i]['department'],
                            poster = info['poster'],
                            profile = crew[i]['profile'],
                            update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                            regdate = DateFormat( datetime.now() ).format("Y-m-d")
                        )
                        print("ctCrew DB insert")
                    else : pass
                    
            else: pass
        
        ## gerne company country 추가
        if info['genreCd'] :
            genre = info['genre'].split(",")
            for i in range(len(genre)) :
                if not ctGenre.objects.filter(genre = genre[i]):
                    ctGenre.objects.create(
                        contentCd = contentCd,
                        media_type = media_type,
                        genre = genre[i],
                        update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                        regdate = DateFormat( datetime.now() ).format("Y-m-d")
                    )
                    print("ctGenre DB insert")
                else:
                    pass
        else : pass
        
        if info['companyCd'] :
            company = info['company'].split("|")
            for i in range(len(company)) :
                if not ctCompany.objects.filter(company = company[i]):
                    ctCompany.objects.create(
                        contentCd = contentCd,
                        media_type = media_type,
                        company = company[i],
                        update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                        regdate = DateFormat( datetime.now() ).format("Y-m-d")
                    )
                    print("ctCompany DB insert")
                else:
                    pass
        else : pass
        
        if info['countryCd'] :
            country = info['country'].split("|")
            for i in range(len(country)) :
                if not ctCountry.objects.filter(country = country[i]):
                    ctCountry.objects.create(
                        contentCd = contentCd,
                        media_type = media_type,
                        country = country[i],
                        update_time = DateFormat( datetime.now() ).format("Y-m-d"),
                        regdate = DateFormat( datetime.now() ).format("Y-m-d")
                    )
                    print("ctCountry DB insert")
                else:
                    pass
        else : pass
        
        count = Review.objects.all().count()
        
        pagenum = request.GET.get("pagenum")
        if not pagenum :
            pagenum = "1"
        pagenum = int( pagenum )
        
        start = ( pagenum - 1) * int(PAGE_SIZE)
        end = start + int (PAGE_SIZE)
        
        if end > count :
            end = count
        
        dtos = Review.objects.filter(media_type=media_type).filter(contentCd=contentCd).order_by("-num")[start:end]
        
        number = count - (pagenum-1)*int(PAGE_SIZE)                     # 50 - (2-1) * 5
        
        startpage = pagenum // PAGE_BLOCK * PAGE_BLOCK + 1      # (蹂닿퀬�떢�� �럹�씠吏�)/5 * 5 + 1
        if pagenum % PAGE_BLOCK == 0 :                                      # �뿏�뱶�럹�씠吏��뿉�룄 �쁺�뼢�씠 媛�寃� �븵�꽌�꽌 �쐞移� �옟�븘以섏빞�븿
            startpage -= PAGE_BLOCK
        endpage = startpage + PAGE_BLOCK - 1
        pagecount = count //PAGE_SIZE
        
        if count % PAGE_SIZE > 0 :
            pagecount += 1
        if endpage > pagecount :
            endpage = pagecount
        
        pages = range(startpage, endpage + 1)
        
        context = {
            "id":id,
            "count" : count,
            "dtos" : dtos,
            "pagenum" : pagenum,
            "number" : number,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            "pages" : pages,
            "info" : info,
            "media_type" : media_type,
            "contentCd" : contentCd,
            "rsAlbum": rsAlbum,
            "like" : like,
        }
    return HttpResponse(template.render(context,request))