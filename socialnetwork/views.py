import imghdr
import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm
from django.urls import reverse
from socialnetwork.models import Post, Profile, Comments


def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    form = LoginForm(request.POST)
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', {'form': form})

    new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('global_stream'))


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))


def register_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    form = RegisterForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
    login(request, new_user)
    return redirect(reverse('global_stream'))


@login_required
def follower_action(request):
    if request.method == 'GET':
        return render(request, 'socialnetwork/follower_stream.html')


@login_required
def follow(request, id):
    errors = []
    context = {}

    entry = get_object_or_404(Profile, created_by=request.user)
    new_user = get_object_or_404(User, id=id)
    entry.followers.add(new_user)
    entry.save()
    context['errors'] = errors
    context['user'] = new_user
    userprof = Profile.objects.get(created_by=new_user)
    context['entry'] = userprof
    context['master'] = entry
    return render(request, 'socialnetwork/otherprofile.html', context)


@login_required
def unfollow(request, id):
    errors = []
    context = {}

    entry = get_object_or_404(Profile, created_by=request.user)
    new_user = get_object_or_404(User, id=id)
    entry.followers.remove(new_user)
    entry.save()
    context['errors'] = errors
    items = Post.objects.filter(user=new_user)
    context['items'] = items
    context['user'] = new_user
    userprof = Profile.objects.get(created_by=new_user)
    context['entry'] = userprof
    context['master'] = entry
    return render(request, 'socialnetwork/otherprofile.html', context)


# @login_required
# def profile_action(request):
#     if request.method == "GET":
#         return render(request, 'socialnetwork/profile.html')


@login_required
def other_profile_action(request):
    if request.method == 'GET':
        return render(request, 'socialnetwork/otherprofile.html')


# @login_required
# def follower_action(request):
#     try:
#         entry = get_object_or_404(Profile, created_by=request.user)
#     except:
#         entry = Profile(picture="xzkb.jpg", created_by=request.user, last_name=request.user.last_name,
#                         first_name=request.user.first_name, bio="")
#         entry.save()
#     item0 = Post.objects.filter(user=entry.followers.first())
#
#     for en in entry.followers.all():
#         items = Post.objects.filter(user=en)
#         item0 = item0.union(items)
#     item0 = item0.order_by("timestamp").reverse()
#     for a in item0:
#         a.timestamp = timezone.localtime(a.timestamp).strftime("%m/%d/%Y %I:%M %p")
#
#     return render(request, 'socialnetwork/follower_stream.html', {'items': item0})


@login_required
def create_post_action(request):
    if request.method == 'GET':
        if Post.objects.count() == 0:
            return render(request, 'socialnetwork/global_stream.html')
        else:
            items = Post.objects.order_by("timestamp").reverse()
            for a in items:
                a.timestamp = timezone.localtime(a.timestamp).strftime("%m/%d/%Y %I:%M %p")
            return render(request, 'socialnetwork/global_stream.html', {'items': items})
    # entry = Profile.objects.get(created_by=request.user)
    context = {'items': Post.objects.all()}
    if 'post' not in request.POST or not request.POST['post']:
        context['error'] = 'You must enter an post.'
        return render(request, 'socialnetwork/global_stream.html', context)

    new_post = Post(user=request.user, text=request.POST['post'], timestamp=datetime.now())
    new_post.save()

    items = Post.objects.order_by("timestamp").reverse()
    for a in items:
        a.timestamp = timezone.localtime(a.timestamp).strftime("%m/%d/%Y %I:%M %p")

    get_global(request)
    return render(request, 'socialnetwork/global_stream.html', {'items': items})


@login_required
def edit_profile_action(request):
    if request.method == "GET":
        try:
            entry = Profile.objects.get(created_by=request.user)
        except:
            entry = Profile(picture="xzkb.jpg", created_by=request.user, last_name=request.user.last_name,
                            first_name=request.user.first_name, bio="")
            entry.save()

        context = {'form': entry}
        return render(request, 'socialnetwork/profile.html', context)
    try:
        upload_pic = request.FILES['choosefile']
        entry = Profile.objects.get(created_by=request.user)
        entry.picture = upload_pic
    except:
        entry = Profile.objects.get(created_by=request.user)
    finally:
        entry.bio = request.POST['bio_input']
        entry.save()
        context = {'form': entry}
        return render(request, 'socialnetwork/profile.html', context)


@login_required
def view_profile_action(request, id):
    if id == request.user.id:
        try:
            entry = get_object_or_404(Profile, created_by=request.user)
        except:
            entry = Profile(picture="xzkb.jpg", created_by=request.user, last_name=request.user.last_name,
                            first_name=request.user.first_name, bio="")
            entry.save()

        context = {'form': entry}
        return render(request, 'socialnetwork/profile.html', context)
    errors = []
    context = {}
    context['errors'] = errors
    target = get_object_or_404(User, id=id)
    entry = get_object_or_404(Profile, created_by=target)
    # loginuser = Profile.objects.get_or_create(created_by=request.user)
    try:
        loginuser = get_object_or_404(Profile, created_by=request.user)
    except:
        loginuser = Profile(picture="xzkb.jpg", created_by=request.user, last_name=request.user.last_name,
                            first_name=request.user.first_name, bio="")
        loginuser.save()
    context['entry'] = entry
    context['user'] = target
    context['master'] = loginuser
    return render(request, 'socialnetwork/otherprofile.html', context)


def get_photo(request, id):
    target = get_object_or_404(User, id=id)
    item = get_object_or_404(Profile, created_by=target)
    type = "image/" + imghdr.what(item.picture)
    # Probably don't need this check as form validation requires a picture be uploaded.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=type)


def get_global(request):
    global_list = []
    items = Post.objects.all()
    for item in items.all():
        comment_list = []
        for co in item.comments.all():
            com_item = {
                'comment': co.comment,
                'firstName': co.user.first_name,
                'lastName': co.user.last_name,
                'time': timezone.localtime(co.timestamp).strftime("%m/%d/%Y %I:%M %p"),
                'id': co.id,
                'userid': co.user.id
            }
            comment_list.append(com_item)
        post_item = {
            'post': item.text,
            'firstname': item.user.first_name,
            'lastname': item.user.last_name,
            'timestamp': timezone.localtime(item.timestamp).strftime("%m/%d/%Y %I:%M %p"),
            'comments': comment_list,
            'id': item.id,
            'userid': item.user.id
        }
        global_list.append(post_item)
    global_list = sorted(global_list, key=lambda i: i['timestamp'], reverse=True)
    global_post_text = json.dumps(global_list)
    return HttpResponse(global_post_text, content_type='application/json')


@login_required
def get_follower(request):
    try:
        entry = get_object_or_404(Profile, created_by=request.user)
    except:
        entry = Profile(picture="xzkb.jpg", created_by=request.user, last_name=request.user.last_name,
                        first_name=request.user.first_name, bio="")
        entry.save()
    follow_list = []
    for en in entry.followers.all():
        items = Post.objects.filter(user=en)
        for item in items.all():
            comment_list = []
            for co in item.comments.all():
                com_item = {
                    'comment': co.comment,
                    'firstName': co.user.first_name,
                    'lastName': co.user.last_name,
                    'time': timezone.localtime(co.timestamp).strftime("%m/%d/%Y %I:%M %p"),
                    'id': co.id,
                    'userid': co.user.id
                }
                comment_list.append(com_item)
            post_item = {
                'post': item.text,
                'firstname': item.user.first_name,
                'lastname': item.user.last_name,
                'timestamp': timezone.localtime(item.timestamp).strftime("%m/%d/%Y %I:%M %p"),
                'comments': comment_list,
                'id': item.id,
                'userid': item.user.id
            }
            follow_list.append(post_item)
    follow_list = sorted(follow_list, key=lambda i: i['timestamp'], reverse=True)
    follower_post_text = json.dumps(follow_list)
    return HttpResponse(follower_post_text, content_type='application/json')


def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)


def add_comment(request, id):
    if not request.user.id:
        return _my_json_error_response("Not logged in", status=401)
    if request.method != 'POST':
        return _my_json_error_response("Not a POST request", status=405)
    if not 'comment' in request.POST or not request.POST['comment']:
        return _my_json_error_response("You must enter a comment to add.", status=400)
    new_comment = Comments(comment=request.POST['comment'], user=request.user, timestamp=datetime.now(), postid=id)
    new_comment.save()
    post = get_object_or_404(Post, id=id)
    post.comments.add(new_comment)
    comment_data = []
    # for item in post.comments.all():
        # comment = item
        # user = get_object_or_404(User, username=comment.user.username)
    comment_item = {
        'comments': new_comment.comment,
        'user': new_comment.user.username,
        'timestamp': timezone.localtime(new_comment.timestamp).strftime("%m/%d/%Y %I:%M %p"),
        'id': new_comment.id,
        'user_id': request.user.id,
        'first_name': new_comment.user.first_name,
        'last_name': new_comment.user.last_name
    }
        # comment_data.append(comment_item)
    comment_text = json.dumps(comment_item)
    return HttpResponse(comment_text, content_type='application/json')
