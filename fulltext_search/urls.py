from django.conf.urls import url
from fulltext_search import views

urlpatterns = [
    url(r'^full_search/',views.full_search),
]