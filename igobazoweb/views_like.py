from django.shortcuts import render, redirect
import logging
from django.http.response import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from igobazoweb.models import MovieLike
from django.utils.dateformat import DateFormat
from datetime import datetime


@csrf_exempt  
def addmvwishlist(request):
    id = request.session.get('id')
    contentCd = request.GET.get("contentCd")
    media_type = request.GET.get("media_type")
    #contentCd = request.POST["contentCd"]
    num = MovieLike.objects.all().count()
    if num == None :          
        num = 1
    else :       
        num += 1
    
        
    
    #template = loader.get_template("detailpage.html")
    #context = {
     #  
      # }

    dto = MovieLike(
        mlnum = num,
        mlid = id,
        contentCd = contentCd,
        modmvldate = DateFormat(datetime.now()).format("Y-m-d"),       
        )
    dto.save()
    
    return redirect("index")
    #return HttpResponse( template.render( context, request ) )
    #return redirect("detailpage?contentCd="+contentCd+"&media_type"+media_type)  
    #return HttpResponseRedirect(request.POST['path'])
    #return redirect(request.POST.get('next'))
@csrf_exempt    
def rmmvwishlist(request):   
    id = request.session.get( "id" )
    
    contentCd = request.GET.get("contentCd")

    dto= MovieLike.objects.filter(mlid = id ).filter(contentCd=contentCd)
    
    if dto :
        dto.delete()        
        return redirect( "index" )
            
    else :
        return redirect("index")
        
    
    template = loader.get_template("detailpage.html")
    context ={
        
       }
    
    return HttpResponse( template.render( context, request ) )