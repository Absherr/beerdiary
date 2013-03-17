from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect, HttpResponse
from beerdiary.models import *
from beerdiary.settings import MEDIA_ROOT
from messages.models import Message
from moderators_panel.forms import beer_form, brewery_form, country_form
from beerdiary.utils import *

def not_in_moderator_group(user):
    if user.groups.filter(name="moderators").count()>0 or user.is_superuser:
            return True
    return False

def moderator_view(request):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")
    return my_render_to_response('moderator_view.html',{},request)

def save_file(file_, path=''):
    filename = file_._get_name()
    file_path = '%s/%s' % (MEDIA_ROOT, str(path) + str(filename))
    fd = open(file_path, 'wb')
    for chunk in file_.chunks():
        fd.write(chunk)
    fd.close()
    im = Image.open(file_path)
    im.thumbnail((128,128), Image.ANTIALIAS)
    im.save(file_path)
    return file_path

def beer_edit(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    if id=="":
        return HttpResponseRedirect("/moderator")

    beer = Beer.objects.filter(id=id)[0]

    form = beer_form.Beer_form(instance=beer)
    if request.POST:
        form = beer_form.Beer_form(request.POST, instance = beer)
        if form.is_valid() and form.is_multipart():
            b = form.save(commit=False)
            if request.FILES and 'image' in request.FILES:
                path = save_file(request.FILES['image'])
                b.image = path[path.index("/"):]
            b.save()
            form.save_m2m()
            return HttpResponseRedirect("/beer/")
    return my_render_to_response("moderator_beer_edit.html",{'beer':beer,'form':form}, request)

def beer_delete(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    if id=="":
        return HttpResponseRedirect("/beer")
    b = Beer.objects.filter(id=id)[0]
    b.delete()
    return HttpResponseRedirect("/beer")

def beer_add(request, id=""): # id of brewery
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    init ={}
    if id!="":
        init['brewery'] = Brewery.objects.filter(id=id)[0]

    form = beer_form.Beer_form(initial=init)
    if request.POST:
        form = beer_form.Beer_form(request.POST)
        if form.is_valid() and form.is_multipart():
            b = form.save(commit=False)
            if request.FILES and 'image' in request.FILES:
                path = save_file(request.FILES['image'])
                b.image = path[path.index("/"):]
            b.save()
            form.save_m2m()
            return HttpResponseRedirect("/beer/")

    return my_render_to_response("moderator_beer_add.html",{'form':form}, request)

def brewery_edit(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    if id=="":
        return HttpResponseRedirect("/moderator")

    brewery = Brewery.objects.filter(id=id)[0]

    form = brewery_form.Brewery_form(instance=brewery)
    if request.POST:
        form = brewery_form.Brewery_form(request.POST, instance = brewery)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/brewery/")
    return my_render_to_response("moderator_brewery_edit.html",{'brewery':brewery,'form':form}, request)

def brewery_delete(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    if id=="":
        return HttpResponseRedirect("/brewery")
    b = Brewery.objects.filter(id=id)[0]
    b.delete()
    return HttpResponseRedirect("/brewery")

def brewery_add(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    init ={}
    if id!="":
        init['country'] = Country.objects.filter(id=id)[0]


    form = brewery_form.Brewery_form(initial=init)
    if request.POST:
        form = brewery_form.Brewery_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/brewery/")


    return my_render_to_response("moderator_brewery_add.html",{'form':form}, request)

def country_edit(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    if id=="":
        return HttpResponseRedirect("/country")

    country = Country.objects.filter(id=id)[0]

    form = country_form.Country_form(instance=country)
    if request.POST:
        form = country_form.Country_form(request.POST, instance = country)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/beer/")
    return my_render_to_response("moderator_beer_edit.html",{'country':country,'form':form}, request)

def country_delete(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    if id=="":
        return HttpResponseRedirect("/country")
    c = Country.objects.filter(id=id)[0]
    c.delete()
    return HttpResponseRedirect("/country")

def country_add(request):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    form = country_form.Country_form()
    if request.POST:
        form = country_form.Country_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/country/")

    return my_render_to_response("moderator_country_add.html",{'form':form}, request)


def message_view(request):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    messages = Message.objects.all()
    return my_render_to_response('moderator_message_view.html',{'list':messages}, request)

def delete_message(request, id=""):
    if not_in_moderator_group(request.user)==False:
        return HttpResponseRedirect("/access_denied")

    if id=="":
        return HttpResponseRedirect("/moderator/message")
    m = Message.objects.filter(id=id)[0]
    m.delete()

    return HttpResponseRedirect("/moderator/message")

def access_denied(request):
    return my_render_to_response('access_denied.html',{},request)