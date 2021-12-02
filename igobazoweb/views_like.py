from django.shortcuts import render, redirect
import logging
from django.http.response import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from igobazoweb.models import MovieLike, PeopleLike, TvLike
from django.utils.dateformat import DateFormat
from datetime import datetime


@csrf_exempt  
def addwishlist(request):
    id = request.session.get('id')
    media_type = request.GET.get("media_type")
    
    if media_type == "person" :
        peopleCd = request.GET.get("peopleCd")
        
        PeopleLike.objects.create(
            id = id,
            peopleCd = peopleCd,
            regdate = DateFormat( datetime.now() ).format("Y-m-d")
        )
        print("PeopleLike DB insert", peopleCd, media_type)
        
    elif media_type == "movie" :
        contentCd = request.GET.get("contentCd")
        
        MovieLike.objects.create(
            id = id,
            contentCd = contentCd,
            media_type = media_type,
            regdate = DateFormat( datetime.now() ).format("Y-m-d")
        )
        print("MovieLike DB insert", contentCd, media_type)
        
    elif media_type == "tv" :
        contentCd = request.GET.get("contentCd")
        
        TvLike.objects.create(
            id = id,
            contentCd = contentCd,
            media_type = media_type,
            regdate = DateFormat( datetime.now() ).format("Y-m-d")
        )
        print("TvLike DB insert", contentCd, media_type)
        
    else : pass
    
    return redirect("index")

@csrf_exempt    
def rmwishlist(request):   
    id = request.session.get( "id" )
    media_type = request.GET.get("media_type")
    
    if media_type == "movie" :
        contentCd = request.GET.get("contentCd")
        dto= MovieLike.objects.filter(id = id).filter(contentCd=contentCd)
        print("MovieLike DB delete", contentCd, media_type)
        
    elif media_type == "tv" :
        contentCd = request.GET.get("contentCd")
        dto= TvLike.objects.filter(id = id).filter(contentCd=contentCd)
        print("TvLike DB delete", contentCd, media_type)
        
    elif media_type == "person" :
        peopleCd = request.GET.get("peopleCd")
        dto= PeopleLike.objects.filter(id = id).filter(peopleCd=peopleCd)
        print("PeopleLike DB delete", peopleCd, media_type)
        
    else: pass
    
    if dto :
        dto.delete()        
        return redirect( "index" )
            
    else :
        return redirect("index")
        
    
    template = loader.get_template("detailpage.html")
    context ={
        
       }
    
    return HttpResponse( template.render( context, request ) )

