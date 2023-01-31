from django.urls import path, include
from blog.views import Home, CreatePost, PostDetail, EditPost, uploadImage, uploadLinkView,home
from django.views.decorators.csrf import csrf_exempt

app_name = "blog"
urlpatterns = [
    path('',Home.as_view(),name = 'home'),
    # path('',home,name="home"),
    path('<int:id>/',PostDetail.as_view(),name = 'postDetail'),
    path('create/',CreatePost.as_view(),name = 'postCreate'),
    path('edit/<int:id>/', EditPost.as_view(),name = 'postEdit'),
    path('uploadImage/',csrf_exempt(uploadImage), name = 'uploadImage'),
    path('linkfetching/',uploadLinkView),

]
