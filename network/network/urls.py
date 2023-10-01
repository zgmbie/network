
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path("unfollow", views.unfollow, name="unfollow"),   
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),   
    path("edit/<int:post_id>" , views.edit , name="edit") ,
    path("adding_Like/<int:post_id>" , views.adding_Like , name="adding_Like") ,
    path("removing_Like/<int:post_id>" , views.removing_Like , name="removing_Like")
    # path("addLike/<int:postID>" , views.addLike , name="addLike") ,
    # path("removeLike/<int:postID>" , views.removeLike , name="removeLike")
    
]
