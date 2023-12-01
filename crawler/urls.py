from .views import index,start_url,get_pages,get_links,show_graph
from django.urls import path


urlpatterns = [
    path("",index,name="index"),
    path("start_url/",start_url,name="start_url"),
    path("get_pages/",get_pages,name="get_pages"),
    path("get_links/",get_links,name="get_links"),
    path("graph/",show_graph,name="graph")
]