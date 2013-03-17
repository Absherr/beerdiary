import os
from django.http import HttpResponseRedirect
from beerdiary.utils import my_render_to_response, make_captcha
from messages.models import *

def message_view(request):
    if request.POST:
        if 'hash' in request.POST:
            try:
                os.remove("beerdiary/img/captche/"+request.POST['hash']+".jpg")
            except Exception:
                pass

        sent_form = MessageForm(request.POST)
        if sent_form.is_valid():
            from hashlib import md5
            m = md5()
            m.update(sent_form.cleaned_data['captcha'])
            hash=m.hexdigest()

            if hash == sent_form.cleaned_data['hash']:
                message = sent_form.save(commit=False)
                if request.user.is_authenticated():
                    up = User_profile.objects.filter(user=request.user)[0]
                    message.author = up
                message.save()
                return HttpResponseRedirect("/contact/sent/")
            else:
                hash = make_captcha()
                m = sent_form.save(commit=False)
                form = MessageForm(initial={"hash":hash,"captcha":"",'reason':m.reason,'content':m.content})
        else:
            hash = make_captcha()
            sent_form.instance.hash = hash
            form = sent_form
    else:
        hash = make_captcha()
        form = MessageForm(initial={'hash':hash})
    return my_render_to_response("message.html",{'form':form, 'captcha': hash },request)

def message_sent_view(request):
    return my_render_to_response('message_sent_view.html',{}, request)


def report(request, id=""):
    if id=="":
        return HttpResponseRedirect("/")

    m = Message(author=User_profile.objects.filter(user=request.user)[0],reason="report", content="bad comment/review")
    m.save()
    return HttpResponseRedirect("/beer")