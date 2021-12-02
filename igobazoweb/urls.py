
from django.urls import path
from igobazoweb import views, views_page, views_review, views_like
from django.views.generic.base import TemplateView

urlpatterns = [
    # Login & Register
    
    path( "register", TemplateView.as_view( template_name="register.html") ),
    path( "login", TemplateView.as_view( template_name="login.html") ),
    path("registerpro", views.registerpro, name="registerpro"),
    path("registers", views.registers, name="registers"),
    path( "nickcheck", views.nickcheck, name="nickcheck" ),
    path( "idcheck", views.idcheck, name="idcheck" ),
    path( "loginpro", views.loginpro, name="loginpro" ),
    path( "logout", views.logout, name="logout" ),
    path( "userinfo",views.userinfo,name = "userinfo"),
    path( "stat",views.stat,name = "stat"),
    path( "modifyview",views.modifyview,name = "modifyview"),
    path( "delete",views.delete,name = "delete"),
    path("deletepro",views.deletepro,name="deletepro"),
    path("modifypro",views.modifypro,name="modifypro"),
    path("editpasswd",views.editpasswd,name="editpasswd"),
    path("editpasswdpro",views.editpasswdpro,name="editpasswdpro"),
    path("idverify",views.idverify,name="idverify"),
    path("nickverify",views.nickverify,name="nickverify"),
    path("editnickname",views.editnickname,name="editnickname"),
    path("editnickpro",views.editnickpro,name="editnickpro"),
    
    # Index Page
    path("index", views_page.index, name="index"),
    path("searchpro", views_page.searchpro, name="searchpro"),
    path("searchmore", views_page.searchmore, name="searchmore"),
    path("detailpage",views_page.detailpage, name="detailpage"),
    
    # Review Page
    path("review", views_review.review, name="review"),
    path( "detail", views_review.detail, name="detail" ),
    # path("detailsymp", views_review.detailsymp, name="detailsymp"),
    
    path("writeprohong", views_review.writeprohong, name="writeprohong"),
    
    path( "modifyviewhong", views_review.modifyviewhong, name="modifyviewhong" ),
    path("modifyprohong", views_review.modifyprohong, name="modifyprohong"),
    
    path("deleteprohong",views_review.deleteprohong,name="deleteprohong"),
    
    path("detailstarp", views_review.detailstarp, name="detailstarp"),
    path("reviewsymp", views_review.reviewsymp, name="reviewsymp"),
    
    # Album
    path("album",views_review.album,name="album"),
    path("album_write",views_review.album_write,name="album_write"),
    path("album_insert",views_review.album_insert,name="album_insert"),
    path("album_view",views_review.album_view,name="album_view"),
    path("album_edit",views_review.album_edit,name="album_edit"),
    path("album_update",views_review.album_update,name="album_update"),
    path("album_delete",views_review.album_delete,name="album_delete"),
    
    #Like
    path("addwishlist", views_like.addwishlist, name="addwishlist"),
    path("rmwishlist", views_like.rmwishlist, name="rmwishlist"),
    

]