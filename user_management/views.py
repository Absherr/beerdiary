from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from beerdiary.utils import my_render_to_response

from user_management.forms.create_user_form import Create_user_form
from user_management.forms.change_password_form import Change_password_form
from user_management.forms.edit_info_form import Edit_info_form

from beerdiary.models import *

def login_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    state = ""
    username = password = ''
    if request.POST:
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                state = "Your account is not active, please contact admin."
        else:
            state = "Your username and/or password were incorrect."
    return my_render_to_response('login_form.html', {'state':state, 'username': username},request)


def logout_user(request):
    if request.user.is_authenticated():
        logout(request)
    return HttpResponseRedirect("/")

def create_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    state = []

    if request.POST:
        form = Create_user_form(request.POST)
        if form.is_valid():
            user = User()
            if User.objects.filter(username = form.cleaned_data['username']):
                state.append("This username is already used!")
            else:
                user.username=form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            if User.objects.filter(email = form.cleaned_data['email']):
                state.append("This email address is already used!")
            else:
                user.email=form.cleaned_data['email']
            if len(state)==0:
                user.save()

                user_profile = User_profile()
                user_profile.age=form.cleaned_data['age']
                user_profile.city=form.cleaned_data['city']
                user_profile.user = user
                user_profile.save()
                return HttpResponseRedirect("/create_done")
        return my_render_to_response('create_user_form.html',{'state' : state, 'form': form}, request)

    form = Create_user_form()
    return my_render_to_response('create_user_form.html',{'form': form}, request)

def create_user_done(request):
    return my_render_to_response("create_user_okay.html", {}, request)

def user_profile(request):
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/")
    user = User.objects.filter(username=request.user)[0]
    user_profile = User_profile.objects.filter(user=user)[0]

    comments = Comment.objects.filter(author=user_profile).order_by('-date','-time')[:5]
    reviews = Review.objects.filter(author=user_profile).order_by('-date','-time')[:5]

    state = []
    if request.POST:
        form = Change_password_form(request.POST)
        if form.is_valid():
            if user.check_password(form.cleaned_data['old_pass']):
                if form.cleaned_data['new_pass'] == form.cleaned_data['new_pass_repeat']:
                    user.set_password(form.cleaned_data['new_pass'])
                    user.save()
                    return HttpResponseRedirect("/profile")
                else:
                    state.append("You have to repeat new password twice")
            else:
                state.append("You have to type correct current password")
        return my_render_to_response('profile.html',{'user':user,'user_profile':user_profile,'state' : state, 'form': form, 'comments':comments,'reviews':reviews} ,request)

    form = Change_password_form()
    return my_render_to_response('profile.html',{'user':user,'user_profile':user_profile,'state': state, 'form': form, 'comments':comments,'reviews':reviews}, request)

def user_profile_edit(request):
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/")
    user = User.objects.filter(username=request.user)[0]
    user_profile = User_profile.objects.filter(user=user)[0]

    if request.POST:
        form = Edit_info_form(request.POST)
        if form.is_valid():
            user_profile.age = form.cleaned_data['age']
            user_profile.city = form.cleaned_data['city']
            user_profile.save()
            return HttpResponseRedirect("/profile")
        return render_to_response('profile_edit.html',{'form':form,'user':request.user}, context_instance=RequestContext(request))

    form = Edit_info_form(initial={'age': user_profile.age,'city':user_profile.city})

    return my_render_to_response('profile_edit.html',{'form': form,'user':request.user}, request)



