from django.conf.urls import url
import views as md5_views

urlpatterns = [
    url(r'^$',md5_views.index,name="index"),
    url(r'md5/$', md5_views.test2, name='idcard'),

]