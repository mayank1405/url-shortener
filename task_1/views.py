from django.shortcuts import render
from .core import master_func, uuid_func
from  .forms import UrlForm
from .models import Url_record


def return_string(request):

    context={}
    input_string=""

    #form for taking input

    
    
    context["shorturl"]=None

    #LOGIC TO CHECK IF INPUT STRING(URL) already exists in db


    #create new short url
    base_url_comp="http://127.0.0.1:8000/"

    if request.method=="POST":
        #get a new id number for base 62 encoding
        form=UrlForm(request.POST)

        if form.is_valid():

            long_url=form.cleaned_data["longurl"]
            print(long_url)
            
            num,s=uuid_func()
            id=num
            print(num)
            print(s)
            encoded_char=master_func(id)

            short_url= base_url_comp + encoded_char
            context["shorturl"]=short_url
    else:
        form=UrlForm()

    context["form"]=form
    return render(request, "home.html", context)










# Create your views here.
