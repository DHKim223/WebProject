from django.db import models
from igobazoweb.choice import GENDER_CHOICE
# Create your models here.

class Member(models.Model):
    id = models.CharField(max_length=30, verbose_name="id", primary_key=True)  # 아이디
    nickname = models.CharField(max_length=50, verbose_name="nickname", null=False)  # 닉네임
    passwd = models.CharField(max_length=30, verbose_name="passwd", null=False)  # 비밀번호
    gender = models.CharField(choices=GENDER_CHOICE, max_length=20, \
                                  verbose_name="gender", null=False)  # 성별
    age = models.IntegerField(verbose_name="age", null=False)  # 나이 
    pg_romance = models.BooleanField(default=False)  # 로맨스
    pg_thriller = models.BooleanField(default=False)  # 스릴러
    pg_horror = models.BooleanField(default=False)  # 공포
    pg_noir = models.BooleanField(default=False)  # 느와르
    pg_action = models.BooleanField(default=False)  # 액션
    pg_sf = models.BooleanField(default=False)  # 공상과학
    pg_fantasy = models.BooleanField(default=False)  # 판타지
    pg_teen = models.BooleanField(default=False)  # 하이틴
    pg_anime = models.BooleanField(default=False)  # 애니메이션
    pg_history = models.BooleanField(default=False)  # 역사
    pg_sports = models.BooleanField(default=False)  # 스포츠
    pg_music = models.BooleanField(default=False)  # 음악
    pg_comedy = models.BooleanField(default=False)  # 코미디
    pg_war = models.BooleanField(default=False)  # 전쟁 
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    join_date = models.DateTimeField(auto_now_add=True, verbose_name="join_date", \
                                     null=False, blank=True)  # 가입일

#######################################################################

class Review(models.Model):
    num = models.IntegerField(verbose_name="num", null=False, unique=True)  # 글번호
    media_type = models.CharField(verbose_name="media_type", null=False, max_length=30)
    contentCd = models.IntegerField(verbose_name="contentCd", null=False)  # 컨텐츠 코드
    title = models.CharField(verbose_name="title", null=False, max_length=100)  # 컨텐츠이름
    writer = models.CharField(verbose_name="writer", null=False, max_length=30)  # 글쓴이
    subject = models.CharField(verbose_name="subject", null=False, max_length=100)  # 글제목
    content = models.CharField(verbose_name="content", null=False, max_length=2000)  # 내용
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    sympathy = models.IntegerField(verbose_name="sympathy", default=0)  # 공감
    readcount = models.IntegerField(verbose_name="readcount", default=0)  # 조회
    ip = models.CharField(verbose_name="IP", max_length=20)
    passwd2 = models.CharField(max_length=30, verbose_name="passwd2", null=False, default='')  # 비밀번호
    
class Album(models.Model):
    no = models.AutoField(verbose_name='no', primary_key=True)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    contentCd = models.IntegerField(verbose_name='contentCd', null=False)
    writer = models.CharField(verbose_name='writer', max_length=30, null=True)  # <- 닉네임
    subject = models.CharField(verbose_name='subject', max_length=255)
    note = models.CharField(verbose_name='note', max_length=1024)
    image = models.CharField(verbose_name='image', max_length=1024)
    count = models.IntegerField(verbose_name='count', default=0)
    update_time = models.DateTimeField(auto_now=True, verbose_name="수정일", blank=True)
    regdate = models.DateTimeField(auto_now_add=True, verbose_name="regdate", blank=True)
    usage = models.CharField(verbose_name='usage', max_length=10)

#######################################################################

class MovieLike(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    id = models.CharField(max_length=30, verbose_name="id", null=False)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class TvLike(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    id = models.CharField(max_length=30, verbose_name="id", null=False)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class PeopleLike(models.Model): 
    num = models.AutoField(verbose_name="number", primary_key=True)
    id = models.CharField(max_length=30, verbose_name="id", null=False)
    peopleCd = models.IntegerField(verbose_name="people_code", null=False)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class DetailStar(models.Model): 
    num = models.AutoField(verbose_name="number", primary_key=True)
    id = models.CharField(max_length=30, verbose_name="id", null=False)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    starpoint = models.DecimalField(verbose_name="starpoint", max_digits = 3, decimal_places = 1, default=0)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)

class ReviewSymp(models.Model): 
    num = models.AutoField(verbose_name="number", primary_key=True)
    id = models.CharField(max_length=30, verbose_name="id", null=False)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    reviewnum = models.IntegerField(verbose_name="reviewnum", null=False)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
#######################################################################

class Movie(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False, unique=True)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    contentNm = models.CharField(verbose_name="content_name", max_length=300)
    originalNm = models.CharField(verbose_name="original_name", max_length=300)
    status = models.CharField(verbose_name="status", max_length=50)
    release_date = models.CharField(verbose_name="release_date", max_length=50)
    runtime =  models.IntegerField(verbose_name='runtime')
    tagline = models.TextField(verbose_name="tagline")
    overview = models.TextField(verbose_name="overview")
    poster = models.CharField(verbose_name='poster', max_length=1024)
    backdrop = models.CharField(verbose_name='backdrop', max_length=1024)
    homepage = models.CharField(verbose_name='homepage', max_length=1024)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class Tv(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False, unique=True)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    contentNm = models.CharField(verbose_name="content_name", max_length=300)
    originalNm = models.CharField(verbose_name="original_name", max_length=300)
    status = models.CharField(verbose_name="status", max_length=50)
    number_of_seasons = models.IntegerField(verbose_name="numer_of_seasons")
    number_of_episodes = models.IntegerField(verbose_name="number_of_episodes")
    release_date = models.CharField(verbose_name="release_date", max_length=50)
    tagline = models.TextField(verbose_name="tagline")
    overview = models.TextField(verbose_name="overview")
    poster = models.CharField(verbose_name='poster', max_length=1024)
    backdrop = models.CharField(verbose_name='backdrop', max_length=1024)
    homepage = models.CharField(verbose_name='homepage', max_length=1024)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class People(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    peopleCd = models.IntegerField(verbose_name="people_code", null=False, unique=True)
    peopleNm = models.CharField(verbose_name="people_name", max_length=100)
    gender = models.CharField(verbose_name="gender", max_length=20)
    birthday = models.CharField(verbose_name="birthday", max_length=50)
    deathday = models.CharField(verbose_name="deathday", max_length=50)
    birth_place = models.CharField(verbose_name="birth_place", max_length=100)
    department = models.CharField(verbose_name="department", null=False, max_length=30)
    profile = models.CharField(verbose_name='profile', max_length=1024)
    homepage = models.CharField(verbose_name='homepage', max_length=1024)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)

#######################################################################

class ctGenre(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    genre = models.CharField(verbose_name='genre', max_length=30)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class ctCompany(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    company = models.CharField(verbose_name='company', max_length=300)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)

class ctCountry(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    country = models.CharField(verbose_name='country', max_length=50)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class mvSeries(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    seriesCd = models.IntegerField(verbose_name="series_code", null=False)
    seriesNm = models.CharField(verbose_name="content_name", max_length=300)
    poster = models.CharField(verbose_name='series_poster', max_length=1024)
    backdrop = models.CharField(verbose_name='series_backdrop', max_length=1024)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class tvNetworks(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    networkCd = models.IntegerField(verbose_name="series_code", null=False)
    networkNm = models.CharField(verbose_name="content_name", max_length=300)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)

class ctCast(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    peopleCd = models.IntegerField(verbose_name="people_code", null=False)
    peopleNm = models.CharField(verbose_name="people_name", max_length=100)
    character = models.CharField(verbose_name="character", max_length=100)
    poster = models.CharField(verbose_name='poster', max_length=1024)
    profile = models.CharField(verbose_name='profile', max_length=1024)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
class ctCrew(models.Model):
    num = models.AutoField(verbose_name="number", primary_key=True)
    contentCd = models.IntegerField(verbose_name="content_code", null=False)
    media_type = models.CharField(verbose_name='media_type', max_length=30, null=False)
    peopleCd = models.IntegerField(verbose_name="people_code", null=False)
    peopleNm = models.CharField(verbose_name="people_name", max_length=100)
    department = models.CharField(verbose_name="department", null=False, max_length=30)
    job = models.CharField(verbose_name="job", null=False, max_length=30)
    poster = models.CharField(verbose_name='poster', max_length=1024)
    profile = models.CharField(verbose_name='profile', max_length=1024)
    update_time = models.DateTimeField(auto_now=True, verbose_name="update_time", blank=True)
    regdate  = models.DateTimeField(auto_now_add=True, verbose_name="regist_date", blank=True)
    
