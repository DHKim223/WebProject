from django.shortcuts import render, redirect
import logging
from django.http.response import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from igobazoweb.models import Member, Review, MovieLike, TvLike, PeopleLike,\
    ReviewSymp
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from IGOBAZO.settings import PAGE_BLOCK, PAGE_SIZE

logger = logging.getLogger(__name__)
# Create your views here.
now = datetime.now().strftime('%Y:%m:%d:%H:%M:%S')

@ csrf_exempt
def registerpro(request):
    
    # romance=request.POST["gender"]
    # logger.info(romance)
    
    genpref = request.POST.getlist("pg")
    gen = [False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    
    for i in genpref :
        i = int(i)
        if i :
            gen[i-1] = True
    
    gender = request.POST["gender"]
    gens = ""
    if gender == "1":
        gens = "남자"
    elif gender == "2":
        gens = "여자"
    else :
        gens = "무지개"
        
    dto = Member(
            id = request.POST["id"],
            passwd = request.POST["passwd"],
            nickname = request.POST["nickname"],
            gender= gens,            
            age=request.POST["ages"],
            pg_romance = gen[0],
            pg_horror = gen[1],
            pg_thriller=gen[2],
            pg_noir=gen[3],
            pg_action=gen[4],
            pg_sf=gen[5],
            pg_fantasy=gen[6],
            pg_teen=gen[7],
            pg_anime=gen[8],
            pg_history=gen[9],
            pg_sports=gen[10],
            pg_music=gen[11],
            pg_comedy=gen[12],
            pg_war=gen[13],            
            join_date = DateFormat(datetime.now()).format("Y-m-d"),        
        )
    
    dto.save() 
    return redirect("index")


@ csrf_exempt
def registers(request):
    
    id = request.POST["id"]
    passwd = request.POST["passwd"]
    
    template = loader.get_template("registers.html")
    context = {
        "id" : id,
        "passwd":passwd,  
        }
    return HttpResponse(template.render(context,request))

@csrf_exempt
def nickcheck(request):
    template = loader.get_template("nickcheck.html")
    nickname= request.GET.get("nickname")
    
    try :
        Member.objects.get(nickname=nickname)
        # 닉네임이 있다.
        result = 1
    except ObjectDoesNotExist :
        # 닉네임이 없다.
        result =0
        
    context={
        "result" : result,
        "nickname" : nickname
        }
    return HttpResponse(template.render(context,request))



@csrf_exempt
def idcheck(request):
    template = loader.get_template("idcheck.html")
    id = request.GET.get("id")
    
    try :
        Member.objects.get(id=id)
        # 아이디가 있다.
        result = 1
    except ObjectDoesNotExist :
        # 아이디가 없다.
        result =0
        
    context={
        "result" : result,
        "id" : id
        } 
    return HttpResponse(template.render(context,request))
    
@csrf_exempt    
def loginpro( request ) :
    id = request.POST["id"]
    passwd = request.POST["passwd"]
    msg = ""
    template = loader.get_template( "login.html" )
    
    try :
        # 아이디가 있다
        dto = Member.objects.get(id=id)
        if passwd == dto.passwd :
            # 비밀번호가 같다
            request.session["id"] = id
            return redirect( "index" )        
        else :
            # 비밀번호가 다르다
            msg = "비밀번호가 다릅니다."      
    except ObjectDoesNotExist :
        # 아이디가 없다
        msg = "입력하신 아이디가 없습니다."
        
    context = {
        "msg" : msg
        }        
    return HttpResponse( template.render( context, request ) )

def logout(request):
    del (request.session["id"])
    return redirect("index")

@csrf_exempt
def userinfo(request):
    id = request.session.get("id")
    dto = Member.objects.get( id = id ) 
    
    count = Review.objects.all().count()
    
    pagenum = request.GET.get("pagenum")
    if not pagenum :
        pagenum = "1"
    pagenum = int( pagenum )
    
    start = ( pagenum - 1) * int(PAGE_SIZE)
    end = start + int (PAGE_SIZE)
    
    if end > count :
        end = count
    dtox = Review.objects.filter(writer = dto.nickname).order_by("-num")[start:end]
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
    
    pg = [dto.pg_romance, dto.pg_thriller, dto.pg_horror, dto.pg_noir, dto.pg_action, dto.pg_sf, dto.pg_fantasy, dto.pg_teen, dto.pg_anime, dto.pg_history, dto.pg_sports, dto.pg_music, dto.pg_comedy, dto.pg_war]
    pgens = ["romance", "thriller", "horror", "noir", "action", "sf", "fantasy", "teen", "anime", "history","sports","music","comedy","war" ]
    pgen = []
    for i in range(len(pg)):
        
        if pg[i] == True:
            pgen.append(pgens[i])
    
    template = loader.get_template("userinfo.html")
    
    
    context={
        "id":id,       
        "dto":dto,
        "pgen":pgen,
        "dtox":dtox,
        "count" : count,
        "pagenum" : pagenum,
        "number" : number,
        "startpage" : startpage,
        "endpage" : endpage,
        "pageblock" : PAGE_BLOCK,
        "pagecount" : pagecount,
        "pages" : pages,
        }
    return HttpResponse(template.render(context,request))

def stat(request):
    id = request.session.get('id')
    
    #####별점######
    #####별점######
    
    #####좋아요######
    dtoml = MovieLike.objects.filter(id = id)
    dtotl = TvLike.objects.filter(id = id)
    dtopl = PeopleLike.objects.filter(id = id)
    #####좋아요######
    
    #####리뷰######
    count = Review.objects.all().count()
    
    pagenum = request.GET.get("pagenum")
    if not pagenum :
        pagenum = "1"
    pagenum = int( pagenum )
    
    start = ( pagenum - 1) * int(PAGE_SIZE)
    end = start + int (PAGE_SIZE)
    
    if end > count :
        end = count
    dtox = Review.objects.filter(num = id).order_by("-num")[start:end] #id 를 ReviewSymp에서 받아온 글번호들로,,,,
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
    #####리뷰######
    template = loader.get_template("stat.html")
    context={
        "id":id,     
        
        #리뷰
        "dtox":dtox,
        "count" : count,
        "pagenum" : pagenum,
        "number" : number,
        "startpage" : startpage,
        "endpage" : endpage,
        "pageblock" : PAGE_BLOCK,
        "pagecount" : pagecount,
        "pages" : pages,
        
        #좋아요
        "dtoml": dtoml,
        "dtotl" : dtotl,
        "dtopl" : dtopl,
        }
    return HttpResponse(template.render(context,request))


def modifyview(request):
    id = request.session.get( "id" )
    dto = Member.objects.get( id = id )
    pg = [dto.pg_romance, dto.pg_thriller, dto.pg_horror, dto.pg_noir, dto.pg_action, dto.pg_sf, dto.pg_fantasy, dto.pg_teen, dto.pg_anime, dto.pg_history, dto.pg_sports, dto.pg_music, dto.pg_comedy, dto.pg_war]
    romance_check=""
    thriller_check=""
    horror_check=""
    noir_check=""
    action_check=""
    sf_check=""
    fantasy_check=""
    teen_check=""
    anime_check=""
    history_check=""
    sports_check=""
    music_check=""
    comedy_check=""
    war_check=""
     
    if dto.pg_romance == True:
        romance_check = "checked"
    if dto.pg_thriller == True:
        thriller_check = "checked"
    if dto.pg_horror == True:
        horror_check = "checked"
    if dto.pg_noir == True:
        noir_check = "checked"
    if dto.pg_action == True:
        action_check = "checked"
    if dto.pg_sf == True:
        sf_check = "checked"
    if dto.pg_fantasy == True:
        fantasy_check = "checked"
    if dto.pg_teen == True:
        teen_check = "checked"   
    if dto.pg_anime == True:
        anime_check = "checked"
    if dto.pg_history == True:
        history_check = "checked"
    if dto.pg_sports == True:
        sports_check = "checked"
    if dto.pg_music == True:
        music_check = "checked"
    if dto.pg_comedy == True:
        comedy_check = "checked"
    if dto.pg_war == True:
        war_check = "checked"
    
    template = loader.get_template( "modifyview.html" )        
    
    context = {
        "dto" : dto,
        "pg" : pg,
        "romance_check":romance_check,
        "thriller_check":thriller_check,
        "horror_check":horror_check,
        "noir_check":noir_check,
        "action_check":action_check,
        "sf_check":sf_check,
        "fantasy_check":fantasy_check,
        "teen_check":teen_check,
        "anime_check":anime_check,
        "history_check":history_check,
        "sports_check":sports_check,
        "music_check":music_check,
        "comedy_check":comedy_check,
        "war_check":war_check,  
        }
    
    return HttpResponse( template.render( context, request ) )

def delete(request):
    id = request.session.get( "id" )
    passwd = request.session.get("passwd")
    dto = Member.objects.get( id = id )
    
    template = loader.get_template( "delete.html" )        
    context = {
        "id" : id,
        "passwd" : passwd,
        "dto" : dto,
        }
    
    return HttpResponse( template.render( context, request ) )

@csrf_exempt
def deletepro( request ) :
    id = request.session.get( "id" )
    passwd = request.POST["passwd"]
    dto= Member.objects.get( id = id )
    if passwd == dto.passwd :
        dto.delete()
        del( request.session["id"] )
        return redirect( "index" )
    else :
        template = loader.get_template( "delete.html" )
        context = {
            "msg" : "입력하신 비밀번호가 다릅니다."
            }
        return HttpResponse( template.render( context, request ) )
    
@csrf_exempt
def modifypro( request ):
    id = request.session.get("id")
    dto = Member.objects.get(id=id)
    
    genpref = request.POST.getlist("pg")
    gen = [False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    
    for i in genpref :
        i = int(i)
        
        gen[i-1] = True
  
    dto.pg_romance = gen[0]
    dto.pg_horror = gen[1]
    dto.pg_thriller=gen[2]
    dto.pg_noir=gen[3]
    dto.pg_action=gen[4]
    dto.pg_sf=gen[5]
    dto.pg_fantasy=gen[6]
    dto.pg_teen=gen[7]
    dto.pg_anime=gen[8]
    dto.pg_history=gen[9]
    dto.pg_sports=gen[10]
    dto.pg_music=gen[11]
    dto.pg_comedy=gen[12]
    dto.pg_war=gen[13]
    dto.save()
    
    return redirect("userinfo")

@csrf_exempt
def editnickpro(request):
    id = request.session.get('id')
    nickname = request.POST["nickname"]
    dto = Member.objects.get(id=id)
    
    if dto.nickname != nickname :
        dto.nickname = nickname
        dto.save()
        
        return redirect("userinfo")
        
@csrf_exempt
def editpasswd(request):
    id = request.session.get('id')
    dto = Member.objects.get(id=id)
    
    
    template = loader.get_template( "editpasswd.html" )
    context = {
        
        }
    return HttpResponse( template.render( context, request ) )

@csrf_exempt    
def editpasswdpro( request ) :
    id = request.session.get("id")
    passwd1 = request.POST["passwd1"]
    passwd2 = request.POST["passwd2"]
    passwd3 = request.POST["passwd3"]
    msg = ""
   
    
    dto = Member.objects.get(id=id)
    if passwd2 != passwd3:
        msg = "비밀번호를 다시 확인 해주세요"
        template = loader.get_template( "editpasswd.html" )   
        context = {
            "msg" : msg
        }   
        return HttpResponse( template.render( context, request ) )
    elif passwd1 == passwd2:
        msg = "비밀번호 다시 확인해 주세요"
        template = loader.get_template( "editpasswd.html" )   
        context = {
            "msg" : msg
        }   
        return HttpResponse( template.render( context, request ) )
    elif passwd1 == dto.passwd :
        # 비밀번호가 같다
        if passwd1 != passwd2 :
            if passwd2 == passwd3 :
                dto.passwd = passwd2
                dto.save()
                return redirect( "userinfo" )        
    else :
        # 비밀번호가 다르다
        msg = "잘못된 비밀번호 입니다."      
        template = loader.get_template( "editpasswd.html" )   
        context = {
            "msg" : msg
        }   
        return HttpResponse( template.render( context, request ) )
    
@csrf_exempt
def idverify(request):
    id = request.POST["id"]
    dtos = Member.objects.all()
    check = False
    for dto in dtos :
        if id==dto.id :
            check= True
            break;
        
    if check : 
        return HttpResponse("중복되는 아이디 입니다.")
    else :
        return HttpResponse("사용가능한 아이디입니다.")
    
@csrf_exempt
def nickverify(request):
    nickname = request.POST["nickname"]
    dtos = Member.objects.all()
    check = False
    for dto in dtos :
        if nickname==dto.nickname :
            check= True
            break;
        
    if check : 
        return HttpResponse("중복되는 닉네임 입니다.")
    else :
        return HttpResponse("사용가능한 닉네임입니다.")

@csrf_exempt
def editnickname(request):
    id = request.session.get('id')
    dto = Member.objects.get(id=id)
    
    template = loader.get_template( "editnickname.html" )
    context = {
        "dto":dto
        }
    return HttpResponse( template.render( context, request ) )
