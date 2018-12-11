from django.conf.urls import url
from report import views

urlpatterns = [
    # url(r'^xadmin/', site.urls),
    url(r'^index/', views.index),
    url(r'^search/', views.search),
    url(r'^sucai/', views.sucai),
    url(r'^collection/', views.collection),
    url(r'^mould/', views.mould),
    url(r'^edit/', views.sucai_edit),
    url(r'^delete/', views.delete),
    url(r'^lot_delete/', views.lot_delete),
    url(r'^del_all/', views.del_all),

]
