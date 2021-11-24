from django.contrib import admin
from igobazoweb.models import Member, Review, Album, MovieLike, ActorLike, DirectorLike


# Register your models here.
class MemberAdmin( admin.ModelAdmin):
    list_display = ("id","nickname","gender","age","pg_romance",\
                    "pg_thriller","pg_horror","pg_noir","pg_action","pg_sf","pg_fantasy","pg_teen",\
                    "pg_anime","pg_history","pg_sports","pg_music","pg_comedy","pg_war","join_date")
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("num","media_type","contentCd","title","subject","writer","content","regdate",\
                   "sympathy","readcount","ip")
    
class  AlbumAdmin(admin.ModelAdmin):
    list_display = ("no","media_type","contentCd","writer","subject","note","image","count","regdate","usage")

class  MovieLikeAdmin(admin.ModelAdmin):
    list_display = ("mlnum","mlid","contentCd","modmvldate")
    
class  ActorLikeAdmin(admin.ModelAdmin):
    list_display = ("alnum","alid","peopleCd","modacldate")
    
class  DirectorLikeAdmin(admin.ModelAdmin):
    list_display = ("dlnum","dlid","peopleCd","moddrldate")
        
# class MovieAdmin(admin.ModelAdmin):
#     list_display = ("num","subject","genre","release_date","actor1","actor2","actor3","reservation_rate",\
#                     "total_audience","production","country","director","playtime")
    
admin.site.register(Member, MemberAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(MovieLike, MovieLikeAdmin)
admin.site.register(ActorLike, ActorLikeAdmin)
admin.site.register(DirectorLike, DirectorLikeAdmin)

# admin.site.register(Movie, MovieAdmin)