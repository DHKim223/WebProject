from django.db import models
from igobazoweb.choice import GENDER_CHOICE
# Create your models here.

class Review(models.Model):
    num = models.IntegerField( verbose_name="num", null=False, unique=True)             #글번호
    media_type = models.CharField(verbose_name="media_type", null=False, max_length=30)
    contentCd = models.IntegerField( verbose_name="contentCd", null=False)                    #컨텐츠 코드
    title = models.CharField( verbose_name="title", null=False, max_length=100)    # 컨텐츠제목
    writer = models.CharField( verbose_name="writer", null=False, max_length=30)           # 글쓴이
    subject = models.CharField( verbose_name="subject", null=False, max_length=100)          # 제목
    content = models.CharField( verbose_name="content", null=False, max_length=2000)        # 내용
    regdate = models.DateTimeField( auto_now_add=True, verbose_name="regdate", blank=True)  #작성일 
    sympathy = models.IntegerField( verbose_name="sympathy", default=0)                            # 공감
    readcount = models.IntegerField( verbose_name="readcount", default=0)                          # 조회
    ip = models.CharField( verbose_name="IP", max_length=20)                                    # ip
    passwd2 = models.CharField(max_length=30, verbose_name="passwd2", null=False, default='')        # 비밀번호
    

class Member(models.Model):
    id = models.CharField(max_length=30, verbose_name="id", primary_key=True)        # 아이디
    nickname = models.CharField(max_length=50, verbose_name="nickname", null=False)        # 닉네임
    passwd = models.CharField(max_length=30, verbose_name="passwd", null=False)        # 비밀번호
    gender = models.CharField(choices=GENDER_CHOICE, max_length=20, \
                                  verbose_name="gender", null=False)                                             # 성별
    age = models.IntegerField(verbose_name="age", null=False)                                     # 나이 
    pg_romance = models.BooleanField(default=False)                                                  # 로맨스
    pg_thriller = models.BooleanField(default=False)                                                     # 스릴러
    pg_horror = models.BooleanField(default=False)                                                     # 공포
    pg_noir = models.BooleanField(default=False)                                                        # 느와르
    pg_action = models.BooleanField(default=False)                                                    # 액션
    pg_sf = models.BooleanField(default=False)                                                           # 공상과학
    pg_fantasy = models.BooleanField(default=False)                                                    # 판타지
    pg_teen = models.BooleanField(default=False)                                                    # 하이틴
    pg_anime = models.BooleanField(default=False)                                                    # 애니메이션
    pg_history = models.BooleanField(default=False)                                                    # 역사
    pg_sports = models.BooleanField(default=False)                                                    # 스포츠
    pg_music = models.BooleanField(default=False)                                                       # 음악
    pg_comedy = models.BooleanField(default=False)                                                    # 코미디
    pg_war = models.BooleanField(default=False)                                                         # 전쟁 
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="가입일", \
                                     null=False, blank=True)                                                       # 가입일
    
class Album(models.Model):
    no = models.AutoField(verbose_name='no', primary_key=True)
    media_type = models.CharField(verbose_name='media_type', max_length=50)
    contentCd = models.IntegerField(verbose_name='contentCd', null=False)
    writer = models.CharField(verbose_name='writer', max_length=30, null=True)    # <- 닉네임
    subject = models.CharField(verbose_name='subject', max_length=255)
    note = models.CharField(verbose_name='note', max_length=1024)
    image = models.CharField(verbose_name='image', max_length=1024)
    count = models.IntegerField(verbose_name='count', default=0)
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="regdate", blank=True )
    usage = models.CharField(verbose_name='usage', max_length=10)

class MovieLike(models.Model):
    mlnum = models.IntegerField( verbose_name="번호", null=False, unique=True)
    mlid = models.CharField(max_length=30, verbose_name="아이디",null=False)        # 아이디
    contentCd = models.IntegerField( verbose_name="영화코드", default=0)                        #영화 코드
    modmvldate = models.DateTimeField( auto_now_add=True, verbose_name="작성일", blank=True)#수정일
    
class ActorLike(models.Model):
    alnum = models.IntegerField( verbose_name="번호", null=False, unique=True )
    alid = models.CharField(max_length=30, verbose_name="아이디",null=False)        # 아이디
    peopleCd = models.CharField( verbose_name="배우", null=False, max_length=30)                  # 배우
    modacldate = models.DateTimeField( auto_now_add=True, verbose_name="작성일", blank=True)#수정일
    
class DirectorLike(models.Model): 
    dlnum = models.IntegerField( verbose_name="번호", null=False, unique=True )           
    dlid = models.CharField(max_length=30, verbose_name="아이디",null=False)        # 아이디
    peopleCd = models.CharField( verbose_name="감독", null=False, max_length=30)           # 감독
    moddrldate = models.DateTimeField( auto_now_add=True, verbose_name="작성일", blank=True)#수정일    
    




# class content(models.Model):
#     num = models.IntegerField(verbose_name="영화번호", null=False, unique=True)                #영화번호
#     subject = models.CharField(verbose_name="영화", null=False, max_length=100)               #영화제목
#     genre = models.CharField(verbose_name="장르", null=False, max_length=30)                   #장르
#     release_date = models.IntegerField( verbose_name="개봉일", null=False)                         #개봉일
#     actor1 = models.CharField(verbose_name="주연1", null=False, max_length=100)              #주연배우1
#     actor2 = models.CharField(verbose_name="주연2", null=False, max_length=100)              #주연배우2
#     actor3 = models.CharField(verbose_name="주연3", null=False, max_length=100)              #주연배우3
#     reservation_rate = models.FloatField(verbose_name="예매율", null=False)                        #예매율
#     total_audience = models.IntegerField(verbose_name="누적관객", null=False)                     #누적관객
#     production = models.CharField(verbose_name="제작사", null=False, max_length=100)        #제작사
#     country = models.CharField(verbose_name="제작국", null=False, max_length=10)              #제작국가
#     director = models.CharField(verbose_name="감독이름", null=False, max_length=100)          #감독
#     playtime = models.IntegerField(verbose_name="영상길이", null=False)                              #영상길이
    
# class Preference(models.Model):
#     name = models.CharField(verbose_name="선호장르", max_length=30)
#     time_stamp = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")
    
    