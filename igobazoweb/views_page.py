from django.shortcuts import render, redirect
import logging
from django.http.response import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from IGOBAZO.settings import PAGE_SIZE, PAGE_BLOCK
from igobazoweb.models import Review, Album
from igobazoweb import tmdb
from pickle import NONE

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
    contentCd = request.GET.get("contentCd")
    
    info = tmdb.getDetail(media_type,contentCd)
    rsAlbum = Album.objects.all().filter(usage='1').filter(contentCd=contentCd)
    
    template = loader.get_template("detailpage.html")
    
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
        "rsAlbum": rsAlbum
        }
    return HttpResponse(template.render(context,request))