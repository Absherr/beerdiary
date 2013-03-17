# Create your views here.
from django.shortcuts import render_to_response
from beerdiary.models import Beer
from beerdiary.utils import my_render_to_response
from recommendation.models import Marked_tag

def get_recommendation(request):
    beers = Beer.objects.all()
    user = request.user
    mt = Marked_tag.objects.filter(user=user)

    checked = []
    for beer in beers:
        mark = 0
        for tag in beer.tags.all():
            this_marked_tag = mt.filter(tag=tag)
            if this_marked_tag.count()==0:
                continue
            mark+=this_marked_tag[0].mark
        checked.append((beer,mark))
    checked = sorted(checked, key= lambda b: b[1], reverse=True)[:10]
    return my_render_to_response('get_recommendation.html',{'list':checked},request)