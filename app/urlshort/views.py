from django.shortcuts import render
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import datetime
import random, string

# Predefined constant
DOMAIN_NAME = 'http://127.0.0.1:8000/'

# Create your views here.

def home(request):
    return render(request, 'home.html')

def createShortURL(request):
    '''
    create short url if 
        request type :
            POST: if already exists given url
                  return already exist short url
            other:
                   return a form context
    '''
    
    if request.method == 'POST':
        form = CreateNewShortURL(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data['original_url']
            original_website_exists = ShortURL.objects.filter(original_url=original_website)
            if len(original_website_exists)>0:
                print("Already created...")
                shorted_url = DOMAIN_NAME + original_website_exists[0].short_url
                return render(request, 'urlcreated.html', {'shorted_url': shorted_url})

            random_chars = generate_hash()
            while len(ShortURL.objects.filter(short_url=random_chars)) !=0:
                random_chars = generate_hash()
            shorted_url = DOMAIN_NAME + random_chars
            s = ShortURL(original_url=original_website, short_url=shorted_url, time_date_created=datetime.now())
            s.save()
            return render(request, 'urlcreated.html', {'shorted_url': s.short_url})
    form = CreateNewShortURL()
    context = {'form': form}
    return render(request, 'create.html', context)

def redirect(request, url):
    '''
    Redirect to given url if short url created
    '''
    # Later if want to change in hash generation
    # Modify this function only

    current_url = ShortURL.objects.filter(short_url=url)
    if len(current_url) <=0:
        return render(request, 'pagenotfound.html')
    context = {'obj':current_url[0]}
    return render(request, 'redirect.html', context)

def generate_hash():
    '''
    Genreate 6 character hash code
    '''

    random_char_lst = list(string.ascii_letters + string.digits)
    random_chars = ''
    for i in range(6):
        random_chars += random.choice(random_char_lst)
    return random_chars