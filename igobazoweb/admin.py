from django.contrib import admin
from igobazoweb.models import Member, Review, Album, \
    Movie, Tv, People, TvLike, MovieLike, PeopleLike,\
    ctGenre, ctCompany, ctCountry, ctCast, ctCrew, mvSeries, tvNetworks,\
    DetailStar, ReviewSymp


# Register your models here.
class MemberAdmin( admin.ModelAdmin):
    list_display = ("id","nickname","gender","age","pg_romance",\
                    "pg_thriller","pg_horror","pg_noir","pg_action","pg_sf","pg_fantasy","pg_teen",\
                    "pg_anime","pg_history","pg_sports","pg_music","pg_comedy","pg_war","update_time","join_date")
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("num","media_type","contentCd","title","subject","writer","content","update_time","regdate",\
                   "sympathy","readcount","ip")
    
class  AlbumAdmin(admin.ModelAdmin):
    list_display = ("no","media_type","contentCd","writer","subject","note","image","count","update_time","regdate","usage")

#######################################################################

class  MovieLikeAdmin(admin.ModelAdmin):
    list_display = ("id","contentCd", "media_type", "regdate")
    
class  TvLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "contentCd", "media_type", "regdate")
  
class  PeopleLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "peopleCd", "regdate")
    
class  DetailStarAdmin(admin.ModelAdmin):
    list_display = ("id", "contentCd", "media_type", "starpoint", "regdate")
    
class  ReviewSympAdmin(admin.ModelAdmin):
    list_display = ("id", "contentCd", "media_type", "reviewnum", "regdate")

#######################################################################
        
class MovieAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "media_type", "contentNm", "originalNm", "status", "release_date", "runtime",\
                    "tagline", "overview", "poster", "backdrop", "homepage", "update_time")

class TvAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "media_type", "contentNm", "originalNm", "status", "number_of_seasons","number_of_episodes" ,\
                    "release_date", "tagline", "overview", "poster", "backdrop", "homepage", "update_time")

class PeopleAdmin(admin.ModelAdmin):
    list_display = ("peopleCd", "peopleNm", "gender", "birthday", "deathday", "birth_place",\
                    "department", "profile", "homepage", "update_time")
    

#######################################################################

class ctGenreAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "media_type", "genre", "update_time")
    
class ctCompanyAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "media_type", "company", "update_time")
    
class ctCountryAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "media_type", "country", "update_time")
    
class ctCastAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "media_type", "peopleCd", "peopleNm", "character", "poster", "profile", "update_time")
    
class ctCrewAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "media_type", "peopleCd", "peopleNm","department", "job", "poster", "profile", "update_time")
    
class mvSeriesAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "seriesCd", "seriesNm","poster","backdrop" , "update_time")
    
class tvNetworksAdmin(admin.ModelAdmin):
    list_display = ("contentCd", "networkCd", "networkNm", "update_time")
    
#######################################################################
    
admin.site.register(Member, MemberAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(MovieLike, MovieLikeAdmin)
admin.site.register(TvLike, TvLikeAdmin)
admin.site.register(PeopleLike, PeopleLikeAdmin)
# admin.site.register(DirectorLike, DirectorLikeAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Tv, TvAdmin)
admin.site.register(People, PeopleAdmin)
admin.site.register(ctGenre, ctGenreAdmin)
admin.site.register(ctCompany, ctCompanyAdmin)
admin.site.register(ctCountry, ctCountryAdmin)
admin.site.register(ctCast, ctCastAdmin)
admin.site.register(ctCrew, ctCrewAdmin)
admin.site.register(mvSeries, mvSeriesAdmin)
admin.site.register(tvNetworks, tvNetworksAdmin)
admin.site.register(DetailStar, DetailStarAdmin)
admin.site.register(ReviewSymp, ReviewSympAdmin)

















