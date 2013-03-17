import Image
import ImageDraw
import ImageFont
from random import choice
from django.shortcuts import render_to_response
from django.template import RequestContext
from beerdiary.models import Brewery, Beer, Country

def my_render_to_response(template_name, dictionary, request):
    dictionary['user']=request.user
    if request.user.groups.filter(name="moderators").count()>0 or request.user.is_superuser:
        dictionary['moderator']='moderator'

    return render_to_response(template_name,dictionary, context_instance=RequestContext(request))


def get_breweries_list_with_marks():
    list = Brewery.objects.all()
    ans = []
    for item in list:
        beers = Beer.objects.filter(brewery=item)
        sum = 0
        amount = 0
        for beer in beers:
            if beer.community_mark != 0:
                sum += beer.community_mark
                amount += 1
        if amount == 0:
            ans.append((item, 0))
        else:
            ans.append((item, sum / amount))
    return ans

def get_list_of_breweries_from_country_with_marks(country_id):
    country = Country.objects.filter(id=country_id)[0]
    list = Brewery.objects.filter(country=country_id)
    ans = []
    for item in list:
        beers = Beer.objects.filter(brewery=item)
        sum = 0
        amount = 0
        for beer in beers:
            if beer.community_mark != 0:
                sum += beer.community_mark
                amount += 1
        if amount == 0:
            ans.append((item, 0))
        else:
            ans.append((item, sum / amount))
    return ans, country


def make_image_for_captcha(img_text, hash):
    im=Image.open('beerdiary/site_media/img/bg.jpg')
    draw=ImageDraw.Draw(im)
    font=ImageFont.truetype('beerdiary/site_media/Cassannet.otf', 35)

    draw.text((10,0),img_text, font=font, fill=(100,100,50))
    im.save('beerdiary/site_media/img/captche/'+hash+'.jpg',"JPEG")

def make_captcha():
    from hashlib import md5
    img_text = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(5)])
    m = md5()
    m.update(img_text)
    hash=m.hexdigest()
    make_image_for_captcha(img_text, hash)

    return hash