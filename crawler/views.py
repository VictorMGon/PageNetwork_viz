from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import localtime
from django.db.models import F
from .forms import url_form
from .models import Page, Link
from crawler.tasks import run_spider

# Create your views here.


def index(request):
    if request.method == "POST":
        if request.POST['action'] == "start_scrapper":
            run_spider.delay()
    pages_list = Page.objects.all()
    return render(request,"crawler\index.html", {"pages_list":pages_list, "url_form":url_form})

def start_url(request):
    if request.method == "POST":
        form = url_form(request.POST)
        if form.is_valid():
            p = Page()
            p.url = form.cleaned_data['url']
            p.scrapped = False
            p.date_scrapped = localtime()
            p.save()
    request.method = "GET"
    return index(request)

def get_pages(request):
    data = Page.objects.all().values()
    return JsonResponse(list(data),safe=False)

def get_links(request):
    data = Link.objects.all().annotate(source=F('source_page'),target=F('target_page')).values()
    return JsonResponse(list(data),safe=False)

def show_graph(request):
    return render(request,"crawler\graph.html")