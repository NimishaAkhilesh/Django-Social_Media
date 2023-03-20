from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("",views.IndexView.as_view(),name='home'),
    path("profile/add",views.ProfileCreateView.as_view(),name="profile-add"),
    path("profile",views.MyProfileView.as_view(),name="myprofile"),
    path('profile/<int:pk>/edit',views.ProfileEditView.as_view(),name="editprofile"),
    path('post/<int:pk>/comment/add',views.AddCommentView.as_view(),name="comment-add"),
    path('post/<int:pk>/like/',views.AddLikeView.as_view(),name='like-add'),
    path('users/<int:pk>/following/add',views.following_view,name='follow'),
    path('users/<int:pk>/following/remove',views.following_remove,name='remove-friend'),
   

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
