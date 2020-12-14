import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

# Create your views here.

#base url of craigslist website
BASE_SITE_URL = 'https://newyork.craigslist.org/search/?query={}'

#base url of craigslist post image
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):
    return render(request, 'index.html')

def search(request):
    search_text = request.POST.get('search')
    minPrice = request.POST.get('minPrice')
    maxPrice = request.POST.get('maxPrice')
    sortBy = request.POST.get('sortBy')
    #storing search text in database
    models.Search.objects.create(search = search_text) 
    final_url = BASE_SITE_URL.format(quote_plus(search_text))
    print(final_url)
    print(search_text, minPrice, maxPrice, sortBy)
    s = ""
    if len(minPrice) > 0 and len(maxPrice) > 0:
        s += "&min_price="+minPrice+"&max_price="+maxPrice
    if len(sortBy) > 0:
        s += "&sort="+sortBy
    print(s)
    final_url += s
    print(final_url)
    #connecting with craigsList with a search key
    response = requests.get(final_url)
    #getting search results in html format
    site_data = response.text

    soup = BeautifulSoup(site_data, features='html.parser')
    #getting all the search result posts
    posts = soup.find_all('li', {'class' : 'result-row'})

    final_posts = []

    for post in posts:
        post_time = post.find(class_ = 'result-date')
        post_title = post.find(class_ = 'result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_ = 'result-price'):
            post_price = post.find(class_ = 'result-price').text
        else :
            post_price = 'N/A'
        

        if post.find(class_ = 'result-image').get('data-ids'):
            post_image_id = post.find(class_ = 'result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_path = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_path = 'https://craigslist.org/images/peace.jpg'

        final_posts.append((post_title, post_url, post_price, post_image_path))

    #print(soup.find('a', {'class' : 'result-title'}).text) 

    frontend_stuff = {
        'search' : search_text,
        'final_posts' : final_posts,
    }
    #print(frontend_stuff)

    return render(request, 'search_list.html', frontend_stuff)