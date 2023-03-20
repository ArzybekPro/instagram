
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.posts.views import index,post_detail,post_delete,search,update_post,create_post,chats
from apps.users.views import register,user_login,profile,account_settings,followers,follows
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('register/',register,name='register'),
    path('logout/', LogoutView.as_view(next_page=user_login) ,name='logout'),
    path('login/',user_login,name='login'),
    path('my_account/<str:username>',profile,name='account'),
    path('post_detail/<int:id>',post_detail,name='post_detail'),
    path('account_settings/<str:username>',account_settings ,name='account_settings'),
    path('post_delete/<int:id>/',post_delete,name='post_delete'),
    path('search/',search,name='search'),
    path('update_post/<int:id>/',update_post,name='update_post'),
    path('create_post/<int:id>/',create_post,name= 'create_post'),
    path('my_account/followers/<int:id>/' , followers ,name = 'followers'),
    path('my_account/follows/<int:id>/',follows,name ='follows'),
    path('chats/<int:id>/',chats,name='chats'),


]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)