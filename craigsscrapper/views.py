from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def search(request):
    search_text = request.POST.get('search')
    print(search_text)
    return render(request, 'search_list.html')