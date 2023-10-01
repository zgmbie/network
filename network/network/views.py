from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User , Post ,Follow ,Like


def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()

    paginator  = Paginator (all_posts , 10)
    page_num = request.GET.get('page')
    post_page = paginator.get_page(page_num)


    likes = Like.objects.all()
    person_you_liked = []
    try:
        for l in likes:
            if (l.user.id == request.user.id) :
                person_you_liked.append(l.post.id)
    except:
        person_you_liked = []

    # allLikes = Like.objects.all()
    # liked_Posts = []
    # try:
    #     for lik in allLikes:
    #         if (lik.user_like.id == request.user.id):
    #             liked_Posts.append(lik.likedPost.id)
    # except:
    #     liked_Posts = []


    return render(request, "network/index.html",{
        "all_posts":all_posts,
        "post_page":post_page,
        "person_you_liked":person_you_liked
        # "likedPost":liked_Posts
    })



def edit(request , post_id ):
    if request.method == "POST":
            new_content = json.loads(request.body)
            editing_required_post = Post.objects.get(pk=post_id)
            editing_required_post.content =  new_content['content']
            editing_required_post.save()
            return JsonResponse({"message":"the changes are saved successfuly." , "data": new_content['content']})
        

def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content , user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))

def profile(request,user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by("id").reverse()

    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    try:
        check_follow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False


    paginator  = Paginator (all_posts , 10)
    page_num = request.GET.get('page')
    post_page = paginator.get_page(page_num)

    return render(request, "network/profile.html",{
        "all_posts":all_posts,
        "post_page":post_page,
        "username":user.username,
        "following":following,
        "followers":followers,
        "is_following":is_following,
        "user_profile":user,
    })

def follow(request):
    userfollow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=userfollow)
    f = Follow(user=current_user,user_follower=user_follow_data)
    f.save()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile , kwargs={"user_id":user_id}))

def unfollow(request):
    userfollow = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_follow_data = User.objects.get(username=userfollow)
    f = Follow.objects.get(user=current_user,user_follower=user_follow_data)
    f.delete()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile , kwargs={"user_id":user_id}))


def following(request):
    current_user =User.objects.get(pk=request.user.id)
    following_users = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('id').reverse()
    following_post = []
    for p in all_posts:
        for f in following_users:
            if f.user_follower == p.user:
                following_post.append(p)
    
    paginator  = Paginator (following_post , 10)
    page_num = request.GET.get('page')
    post_page = paginator.get_page(page_num)

    return render(request, "network/following.html",{
        "post_page":post_page,

    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




def adding_Like(request,post_id):
    post = Post.objects.get(pk=post_id) 
    user = User.objects.get(pk=request.user.id)
    add_like = Like(user = user , post = post )
    add_like.save()
    return JsonResponse({"message":"like is added "})

def removing_Like(request,post_id):
    post = Post.objects.get(pk=post_id) 
    user = User.objects.get(pk=request.user.id) 
    remove_like = Like.objects.filter(user = user , post = post )
    remove_like.delete()
    return JsonResponse({"message":"like is removed"})



# def addLike(request,postID):
#     post = posts.objects.get(pk=postID) 
#     user = User.objects.get(pk=request.user.id)
#     new_like = Like(user = user , post = post )
#     new_like.save()
#     return JsonResponse({"message":"liked"})

# def removeLike(request,postID):
#     post = posts.objects.get(pk=postID) 
#     user = User.objects.get(pk=request.user.id) 
#     removeLike = Like.objects.filter(user = user , post = post )
#     removeLike.delete()
#     return JsonResponse({"message":"like is removed"})

