from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from beerdiary.models import News, Beer, Review, Comment, User_profile, Brewery, Country
from taggit.models import Tag
from beerdiary.utils import my_render_to_response, get_breweries_list_with_marks, get_list_of_breweries_from_country_with_marks
from forms import comment_form, review_form
from recommendation.models import Marked_tag
from user_management.forms import login_form

def home(request):
    news = News.objects.order_by("-date", "-time")[:5]
    form = login_form.Login_form()

    bbc = []
    beers = Beer.objects.order_by("-added")[:5]
    breweries = Brewery.objects.order_by("-added")[:5]
    countries = Country.objects.order_by("-added")[:5]

    users = User.objects.order_by("-date_joined")[:5]

    rc = []
    comments = Comment.objects.order_by("-time").order_by("-date")[:5]
    reviews = Review.objects.order_by("-time").order_by("-date")[:5]

    for i in range(len(beers)):
        bbc.append((beers[i],'beer'))
    for i in range(len(breweries)):
        bbc.append((breweries[i],'brewery'))
    for i in range(len(countries)):
        bbc.append((countries[i],'country'))
    for i in range(len(comments)):
        rc.append((comments[i],'comment'))
    for i in range(len(reviews)):
        rc.append((reviews[i],'review'))

    bbc = sorted(bbc, key=lambda i: i[0].added, reverse=True)
    rc = sorted(rc,key=lambda i: i[0].date, reverse=True)


    return my_render_to_response("home.html",{'news':news,'bbc':bbc,'rc':rc,'users':users, 'form':form}, request)

def beer_view(request, beer_id=""):
    if beer_id == "": # lista wszystkich piw
        list = Beer.objects.all()
        return my_render_to_response("beer_browsing_list.html",{'list': list}, request)

    else: # konkretne piwo
        beer = Beer.objects.filter(id=beer_id)[0]
        comments = Comment.objects.filter(beer=beer).order_by('-date','-time')
        reviews = Review.objects.filter(beer=beer).order_by('-date','-time')

        if len(reviews)>0:
            avg = beer.community_mark
        else:
            avg = 'This beer doesn\'t have any reviews yet'

        if request.POST and 'comment' in request.POST:
            comment = Comment(author = User_profile.objects.filter(user = request.user)[0],
                beer=beer,
                description=request.POST['comment']
                )
            comment.save()
        list = []
        for r in reviews:
            list.append((r,'r'))
        for c in comments:
            list.append((c,'c'))
        list = sorted(list,key=lambda c: c[0].time)
        list = sorted(list,key=lambda c: c[0].date)

        form = comment_form.Comment_form()
        return my_render_to_response("beer.html",{'list':list, 'beer':beer, 'avg':avg ,'form':form}, request)

def brewery_view(request, brewery_id=""):
    if brewery_id == "":
        breweries_list = get_breweries_list_with_marks()
        return my_render_to_response("brewery_browsing_list.html",{'list': breweries_list},request)
    else:
        brewery = Brewery.objects.filter(id=brewery_id)[0]
        list = Beer.objects.filter(brewery=brewery)
        return my_render_to_response("brewery.html",{'brewery':brewery,'list':list}, request)

def country_view(request, country_id=""):
    if country_id == "":
        list = Country.objects.all()

        return my_render_to_response("country_browsing_list.html",{'list': list},request)
    else:
        list, country = get_list_of_breweries_from_country_with_marks(country_id)

        return my_render_to_response("country.html",{'country':country, 'list':list},request)

def add_review(request, beer_id):
    if request.user.is_authenticated() == False:
        return HttpResponseRedirect("/beer/"+beer_id)

    beer = Beer.objects.filter(id=beer_id)[0]
    user = request.user

    form = review_form.Review_form()

    if request.POST:
        form = review_form.Review_form(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = User_profile.objects.filter(user = user)[0]
            review.beer = beer

            weights = {'flavour':10,'aroma':10,'palate':7,'appearance':3}
            review.averaged_mark = "{0:.2f}".format(float((weights['flavour']*float(review.flavour_mark)+weights['aroma']*float(review.aroma_mark)+weights['palate']*float(review.palate_mark)+weights['appearance']*float(review.appearance_mark))/30))
            review.save()

            cm = beer.community_mark * beer.amount_of_marks
            beer.amount_of_marks+=1
            cm+=float(review.averaged_mark)
            beer.community_mark = "{0:.2f}".format(cm/beer.amount_of_marks)
            beer.save()
            
            for tag in beer.tags.all():
                mt = Marked_tag.objects.filter(user=request.user).filter(tag = tag)
                if mt:
                    mt=mt[0]
                    sum = mt.mark * mt.amount
                    sum+=float(review.averaged_mark)
                    mt.amount+=1
                    sum="{0:.2f}".format(sum/mt.amount)
                    mt.mark = sum
                    mt.save()
                else:
                    mt=Marked_tag(tag=tag,user=request.user, amount=1,mark=review.averaged_mark)
                    mt.save()

            return HttpResponseRedirect('/beer/'+beer_id)

    return my_render_to_response('add_review.html',{'beer':beer,'form':form}, request)

def tag_view(request, tag_name=""):
    if tag_name=="":
        tags = Tag.objects.all().order_by("name")

        return my_render_to_response("tag_browsing_list.html",{'user':request.user,'tags':tags},request)

    beer_list = Beer.objects.filter(tags__name__in=(tag_name,))
    return my_render_to_response("tag.html",{'tag':tag_name, 'list':beer_list},request)

def news_view(request):
    list = News.objects.order_by("-date", "-time")[:]
    return my_render_to_response('news_view.html',{'list':list},request)

def search_view(request):
    query = ""
    category = ""
    result = {'beers':0,'beers_by_tag':0,'breweries':0,'countries':0,'tags':0}

    if request.GET and request.GET['q']:
        query = request.GET['q']
        category = request.GET['category']
        if category == "everywhere":
            result["beers"] = Beer.objects.filter(name__icontains=query).order_by("name")
            result["beers_by_tag"] = Beer.objects.filter(tags__name__icontains=query).distinct().order_by("name")
            result["breweries"] = Brewery.objects.filter(name__icontains=query).order_by("name")
            result["countries"] = Country.objects.filter(name__icontains=query).order_by("name")
            result["tags"] = Tag.objects.filter(name__icontains=query).order_by("name")
        elif category == "beers":
            result["beers"] = Beer.objects.filter(name__icontains=query).order_by("name")
            result["beers_by_tag"] = Beer.objects.filter(tags__name__icontains=query).order_by("name")
        elif category == "breweries":
            result["breweries"] = Brewery.objects.filter(name__icontains=query).order_by("name")
        elif category=="countries":
            result["breweries"] = Country.objects.filter(name__icontains=query).order_by("name")
        elif category == "tags":
            result["tags"] = Tag.objects.filter(name__icontains=query).order_by("name")

    return my_render_to_response("search.html",{'query':query,'category':category, 'result':result}, request)