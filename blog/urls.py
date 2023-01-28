from django.urls import path

from blog import feeds
from . import views

urlpatterns = [
    path('',views.PostListView.as_view(),name='post-list'),
    path('post/new/',views.PostCreateView.as_view(), name='post-form'),
    path('post/<int:pk>/',views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/edit/',views.PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/remove/',views.PostDeleteView.as_view(), name='post-remove'),
    path('post/<int:pk>/star',views.star_post,name='star-post'),
    path('post/<int:pk>/unstar',views.unstar_post,name='unstar-post'), 
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add-comment'),
    path('comment/<int:pk>/remove/',views.remove_comment,name='remove-comment'),
    path('post/<int:pk>/publish',views.publish_post,name='post-publish') ,
    path('my-stories/',views.stories,name='stories'),
    # feeds
    path('latest-posts/',feeds.LatestPostsFeed()),
    #  reply
    path('comment/<int:pk>/reply/',views.add_reply,name='add-reply')
    
    

]
