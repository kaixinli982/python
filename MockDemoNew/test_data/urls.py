from django.conf.urls import url
import views as test_data_views

urlpatterns=[
url(r'^$',test_data_views.index,name="index"),
url(r'borrow/$',test_data_views.borrow_index,name="borrow_index"),
url(r'borrow_auto/?.*$',test_data_views.borrow_auto,name="borrow_auto"),
]