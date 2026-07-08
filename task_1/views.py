from django.shortcuts import render, get_object_or_404, redirect
from .core import master_func, uuid_func, hash_url, generate_qr
from  .forms import UrlForm
from .models import Url_record
import redis
import os
from dotenv import load_dotenv


load_dotenv()

base_url_comp="http://127.0.0.1:8000/t1/shrt/"

upstash_url=os.getenv("UPSTASH_URL")
r=redis.Redis.from_url(upstash_url)
val1=r.get("mike")
print(val1)
def return_string(request):

    context={}
    input_string=""

    #form for taking input

    
    
    context["shorturl"]=None
    context["qr"]=None

    #LOGIC TO CHECK IF INPUT STRING(URL) already exists in db


    #create new short url
    

    if request.method=="POST":
        #get a new id number for base 62 encoding
        form=UrlForm(request.POST)

        if form.is_valid():

            long_url=form.cleaned_data["longurl"]
            qr_required=form.cleaned_data["qr_required"]

            hashed_url=hash_url(long_url)
            cache_fetch=r.get(f"{hashed_url}")
            if cache_fetch:
                short_url=cache_fetch.decode()
                print("cache used")
            else:
                print(long_url)
                qlist=Url_record.objects.filter(longurl=long_url)
                if qlist:
                    obj=qlist[0]
                    print(obj.shorturl)
                    short_url=obj.shorturl
                    r.set(f"{hashed_url}",f"{short_url}")
                    r.set(f"{short_url}", f"{long_url}")


                else:

                    num,s=uuid_func()
                    id=num
                    encoded_char=master_func(id)

                    short_url= base_url_comp + encoded_char

                    Url_record.objects.create(longurl=long_url, shorturl=short_url, uuid_field=s)
                    r.set(f"{hashed_url}",f"{short_url}")
                    r.set(f"{short_url}", f"{long_url}")

            if qr_required:
                qr_html_element=generate_qr(short_url)
                context["qr"]=qr_html_element
            context["shorturl"]=short_url
    else:
        form=UrlForm()

    context["form"]=form
    return render(request, "home.html", context)


def redirect_to_longurl(request,shortlink):
    print(shortlink)
    short_url=base_url_comp+shortlink
    # obj1=Url_record.objects.filter(shorturl=shortlink).first()
    # print(obj1.longurl)

    cache_fetch=r.get(f"{short_url}")
    if cache_fetch:
        print("cache hit on redirect")
        redirect_link=cache_fetch.decode()
    else:
        obj=get_object_or_404(Url_record,shorturl=short_url)
        print(obj)
        redirect_link=obj.longurl
        hashed_url=hash_url(redirect_link)
        r.set(f"{hashed_url}", f"{short_url}")
        r.set(f"{short_url}", f"{redirect_link}")
    print(redirect_link)
    return redirect(redirect_link)








# Create your views here.
