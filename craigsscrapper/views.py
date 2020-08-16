import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus

# Create your views here.

BASE_SITE_URL = 'https://newyork.craigslist.org/search/?query={}'

def home(request):
    return render(request, 'index.html')

def search(request):
    search_text = request.POST.get('search')
    final_url = BASE_SITE_URL.format(quote_plus(search_text))
    print(final_url)
    response = requests.get(final_url)
    site_data = response.text
    
    return render(request, 'search_list.html')