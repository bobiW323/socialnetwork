from django.urls import path
from socialnetwork import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('login', views.login_action, name='login'),
    # path('', views.global_stream_action, name='home'),
    path('global_stream', views.create_post_action, name='global_stream'),
    path('create_post', views.create_post_action, name='create_post'),
    path('logout', views.logout_action, name='logout'),
    path('register', views.register_action, name='register'),
    path('follow/<int:id>', views.follow, name='follow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('profile', views.edit_profile_action, name='profile'),
    path('edit_profile', views.edit_profile_action, name='edit_profile'),
    path('view_profile/<int:id>', views.view_profile_action, name='view_profile'),
    path('follower_stream', views.follower_action, name='follower_stream'),
    path('otherprofile', views.other_profile_action, name='otherprofile'),
    path('get_photo/<int:id>', views.get_photo, name='get_photo'),
    path('get-global', views.get_global, name="get-global"),
    path('get-follower', views.get_follower, name="get-follower"),
    path('add-comment/<int:id>', views.add_comment, name="add-comment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
