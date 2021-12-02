from django.shortcuts import render, redirect
import logging
from django.template import loader
from django.http.response import HttpResponse
from igobazoweb.models import Review, Member, Album, ReviewSymp, DetailStar,\
    Movie, Tv
from IGOBAZO.settings import PAGE_SIZE, PAGE_BLOCK
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import random
import os
from igobazoweb.tmdb import getDetail

logger = logging.getLogger(__name__)
# Create your views here.

# 리뷰페이지
def review(request):
    template = loader.get_template("review.html")
    count = Review.objects.all().count()
    id = request.session.get('id') 
    
    pagenum = request.GET.get("pagenum")
    if not pagenum :
        pagenum = "1"
    pagenum = int( pagenum )
    
    start = ( pagenum - 1) * int(PAGE_SIZE)
    end = start + int (PAGE_SIZE)
    
    if end > count :
        end = count
    
    #dtos = Review.objects.order_by("-ref")[start:end]
    dtos = Review.objects.order_by("-num")[start:end]
    
    number = count - (pagenum-1)*int(PAGE_SIZE)                     # 50 - (2-1) * 5
    
    startpage = pagenum // PAGE_BLOCK * PAGE_BLOCK + 1      # (보고싶은 페이지)/5 * 5 + 1
    if pagenum % PAGE_BLOCK == 0 :                                      # 엔드페이지에도 영향이 가게 앞서서 위치 잡아줘야함
        startpage -= PAGE_BLOCK
    endpage = startpage + PAGE_BLOCK - 1
    pagecount = count //PAGE_SIZE
    
    if count % PAGE_SIZE > 0 :
        pagecount += 1
    if endpage > pagecount :
        endpage = pagecount
    
    pages = range(startpage, endpage + 1)
    
    context = {
        "id" : id,
        "count" : count,
        "dtos" : dtos,
        "pagenum" : pagenum,
        "number" : number,
        "startpage" : startpage,
        "endpage" : endpage,
        "pageblock" : PAGE_BLOCK,
        "pagecount" : pagecount,
        "pages" : pages,
        }
    return HttpResponse(template.render(context,request))




# 글보기
def detail( request ) :
    id = request.session.get('id')
    num = request.GET.get( "num" )
    pagenum = request.GET.get( "pagenum" )
    number = request.GET.get( "number" )
    media_type = request.GET.get("media_type")
    contentCd = request.GET.get("contentCd")
    
    template = loader.get_template( "detail.html" )
              
    dto = Review.objects.get( num = num )
    
    dto.readcount += 1
    dto.save()
    
    context = {
        "id":id,
        "dto" : dto,
        "pagenum" : pagenum,
        "number" : number,
        "contentCd" : contentCd
        }
    return HttpResponse( template.render( context, request ) )

# # 공감 누르기
# @csrf_exempt
# def detailsymp( request ):
#     if request.method == "POST" :
#         num = request.POST["num"]
#         sympathystr = request.POST["sympathy"]
#
#         sympathy = int(sympathystr)
#
#         sympathy +=1
#
#         dto = Review.objects.get( num = num )
#         dto.sympathy = sympathy
#         dto.save()
#     return redirect( "index" )   



@csrf_exempt
def writeprohong(request):
    id = request.session.get('id')
    dto = Member.objects.get(id=id)
    nickname = dto.nickname
    
    if request.method == "GET" :
        media_type = request.GET.get("media_type")
        contentCd = request.GET.get("contentCd")
        content = getDetail(media_type, contentCd)
        title = content['contentNm']
        ref = 1                             # 그룹화 아이디
        #restep = 0                          # 글순서
        #relevel = 0                         # 글레벨
        num = request.GET.get( "num" )
        if num == None :
            # 제목글인 경우
            try :
                # 글이 있는 경우
                maxnum = Review.objects.order_by("-num").values()[0]["num"]
                ref = maxnum + 1        # 그룹화  아이디 = 글번호 최대값 + 1
            except IndexError :
                # 글이 없는 경우
                ref = 1     

        template = loader.get_template( "reviewwrite.html" )
             
        context = {
            "id":id,
            "num" : num,
            "ref" : ref,
            "contentCd" : contentCd,
            "media_type":media_type,
            "title" : title,
            "nickname" : nickname
            #"restep" : restep,
            #"relevel" : relevel,
            }
        return HttpResponse( template.render( context, request ) )
    
# 글쓰기 처리
    else :
        num = Review.objects.all().count()
        id = request.session.get('id')
        
        if num == None :
            #글이 없는 경우
            num = 1
        else :
            #글이 있는 경우
            num += 1

            
        dto = Review(
            num = num,
            writer = request.POST["writer"],
            media_type = request.POST["media_type"],
            contentCd = request.POST["contentCd"],
            title = request.POST["title"],
            subject = request.POST["subject"],
            passwd2 = request.POST["passwd2"],
            content = request.POST["content"],
            #starpoint = request.POST["starpoint"],
            readcount = 0,
            regdate = DateFormat( datetime.now() ).format("Y-m-d"),
            ip = request.META.get("REMOTE_ADDR")
            )
        dto.save()
        
        return redirect("index")    

# 글수정
@csrf_exempt
def modifyviewhong( request ) :
    id = request.session.get("id")
    if request.method == "GET" :
        num = request.GET.get( "num" )
        pagenum = request.GET.get( "pagenum" )
        number = request.GET.get( "number" )
        template = loader.get_template( "modify.html" )
        context = {
            "id":id,
            "num" : num,
            "pagenum" : pagenum,
            "number" : number
            } 
        return HttpResponse( template.render( context, request ) )
    else :
        num = request.POST["num"]
        pagenum = request.POST["pagenum"]
        number = request.POST["number"]
        passwd2 = request.POST["passwd2"]
        
        dto = Review.objects.get( num = num )
        if passwd2 == dto.passwd2 :
            template = loader.get_template( "modifyviewhong.html" )
            context = {
                "id":id,
                "num": num,
                "pagenum": pagenum,
                "number" : number,
                "dto": dto
                }
        else :
            template = loader.get_template( "modify.html" )
            context = {
                "id":id,
                "num" : num,
                "pagenum": pagenum,
                "number": number,
                "msg" : "비밀번호가 다릅니다."
                }
        return HttpResponse( template.render( context, request ) )
    

@csrf_exempt
def modifyprohong( request ) :
    if request.method == "POST" :
        num = request.POST["num"]
        subject = request.POST["subject"]
        content = request.POST["content"]
        passwd2 = request.POST["passwd2"]
        #starpoint = request.POST["starpoint"]
        
        dto = Review.objects.get( num = num )
        dto.subject = subject
        dto.content = content
        dto.passwd2 = passwd2
        #dto.starpoint = starpoint
        dto.save()
    return redirect( "index" )

# 글삭제
@csrf_exempt    
def deleteprohong( request ) :
    id = request.session.get('id')
    if request.method == "GET" :
        num = request.GET.get( "num" )
        pagenum = request.GET.get( "pagenum" )
        template = loader.get_template( "deletehong.html" )
     
        context = {
            "id":id,
            "num" : num,
            "pagenum" : pagenum
            }
                
        return HttpResponse( template.render( context, request ) )
    else :
        num = request.POST["num"]
        pagenum = request.POST["pagenum"]
        passwd2 = request.POST["passwd2"]
        
        dto = Review.objects.get(num = num)
        if passwd2 != dto.passwd2 :
            # 비밀번호가 다르다 - delete.html
            template = loader.get_template( "deletehong.html" )
            context = {
                "id":id,
                "num" : num,
                "pagenum" : pagenum,
                "msg" : "비밀번호가 다릅니다.",
                }
            return HttpResponse( template.render( context, request ) )        
        else :
            # 비밀번호가 같다 - review.html
            dto.subject = "삭제된 글입니다."
            dto.title = ""
            dto.readcount = -1
            dto.save()        
            return redirect( "index" )


#################################################################


def album(request):
    rsAlbum = Album.objects.all().filter(usage='1')

    return render(request, "album_list.html", {
         'rsAlbum': rsAlbum
     })    
@csrf_exempt   
def album_write(request):
    contentCd = request.GET.get("contentCd")
    media_type = request.GET.get("media_type")
    # print("write_contentCd : " , contentCd) 
    # print("write_media_type : " , media_type)
    
    template = loader.get_template( "album_write.html" )
    context = {
        "contentCd" : contentCd,
        "media_type" : media_type
        }    
    
    return HttpResponse( template.render( context, request ) ) 
    # return render(request, "album_write.html")


@csrf_exempt   
def album_insert(request):
    id = request.session.get('id')
    dto = Member.objects.get(id=id)
    nickname = dto.nickname
    # print("album_insert ID : ", id)
    # print("album_insert NickName : ", nickname)


    atitle = request.POST['a_title']
    
    anote = request.POST['a_note']
    #atype = request.POST['media_type']
    contentCd = request.POST.get("contentCd")
    media_type = request.POST.get("media_type")
    print("album_insert contentCd : ", contentCd)
    print("album_insert media_type : ", media_type)

    
    name_date = str(DateFormat( datetime.now() ).format("Y-m-d"))
    uploaded_file = request.FILES['ufile']
    name_old = uploaded_file.name
    name_ext = os.path.splitext(name_old)[1]
    name_new = 'C' + name_date + '_' + str(random.randint(10000, 99999))

    fs = FileSystemStorage(location='igobazoweb/static/board/photos')

    name = fs.save(name_new + name_ext, uploaded_file)
    Album.objects.create(media_type= media_type, subject=atitle, regdate=name_date, note=anote, image=name, writer=nickname, contentCd=contentCd, usage='1') # DB 저장
      
    return redirect('index')



def album_view(request):
    ano = request.GET['a_no']

    rsData = Album.objects.get(no=ano)
    rsData.count += 1
    rsData.save()

    rsDetail = Album.objects.filter(no=ano)

    return render(request, "album_view.html", {
        'rsDetail': rsDetail,
        'a_no': ano,
    })

def album_edit(request):
    ano = request.GET['a_no']
    rsDetail = Album.objects.filter(no=ano)

    return render(request, "album_edit.html", {
        'rsDetail': rsDetail,
        'a_no': ano,
    })


def album_update(request):

    ano = request.POST['a_no']
    atitle = request.POST['a_title']
    # atype = request.POST['a_type']
    anote = request.POST['a_note']

    if 'ufile' in request.FILES:
        name_date = str(DateFormat( datetime.now() ).format("Y-m-d"))
        uploaded_file = request.FILES['ufile']
        name_old = uploaded_file.name
        name_ext = os.path.splitext(name_old)[1]
        name_new = 'C' + name_date + '_' + str(random.randint(10000, 99999))

        fs = FileSystemStorage(location='igobazoweb/static/board/photos')

        fname = fs.save(name_new + name_ext, uploaded_file)

        album = Album.objects.get(no=ano)
        album.subject = atitle
        # album.a_type = atype
        album.note = anote
        album.image = fname
        album.save()
    else:
        album = Album.objects.get(no=ano)
        album.subject = atitle
        # album.a_type = atype
        album.note = anote
        album.save()

    return redirect('index')

def album_delete(request):
    ano = request.GET['a_no']
    album = Album.objects.get(no=ano)
    album.usage = '0'
    album.save()

    return redirect('index')

@csrf_exempt
def reviewsymp( request ): 
    id = request.session.get('id')
        
    reviewnum = request.GET.get("num")
    sympathystr = request.GET.get("sympathy")
    
    contentCd = request.GET.get("contentCd")
    media_type = request.GET.get("media_type")

    rsp = ReviewSymp.objects.filter(id=id).filter(reviewnum=reviewnum)
    if rsp.exists() :
        print("아이디 있음")
        
    else :     
        rstb = ReviewSymp.objects.create(id=id, contentCd=contentCd, \
                                         media_type=media_type,\
                                         reviewnum=reviewnum)   
        
        sympathy = int(sympathystr)
        sympathy +=1

        dto = Review.objects.get( num = reviewnum )
        dto.sympathy = sympathy
        dto.save()
    
    return redirect( "index" )

@csrf_exempt
def detailstarp(request):
    id = request.session.get('id')
    
    media_type = request.GET.get("media_type")
    contentCd = request.GET.get("contentCd") 
    starpoint = request.GET.get("starpoint")
    stpint = int(starpoint)
    starpoint2 = stpint / 2;  
    
    dst = DetailStar.objects.filter(id=id).filter(contentCd=contentCd)
    if dst.exists() :
        print("아이디 있음", dst)
    else :  
        dstb = DetailStar.objects.create(id=id, contentCd=contentCd, \
                                         media_type=media_type,\
                                         starpoint=starpoint2)         
            
    return redirect( "index" )