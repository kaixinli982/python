from django.conf.urls import url
import views as test_gadget_views

urlpatterns = [
    url(r'^$',test_gadget_views.index,name="index"),
    url(r'idcard/$', test_gadget_views.idcard_index, name='idcard'),
    url(r'generateidcard/?.*$', test_gadget_views.generate_idcard, name='generateidcard'),
    url(r'city/?.*$', test_gadget_views.city_get ,name='city'),
    url(r'area/?.*$', test_gadget_views.area_get, name='area'),
    url(r'bankcard/$', test_gadget_views.bankcard_index , name='bankcard'),
    url(r'generatebankcard/?.*$', test_gadget_views.banckcard_generate, name='generatebankcard'),
    url(r'idcheckindex/$', test_gadget_views.id_check_index, name='idcheckindex'),
    url(r'id_check/?.*$', test_gadget_views.id_check, name='idcheck'),
    url(r'useraccount_index/$', test_gadget_views.useraccount_index, name='useraccount_index'),
    url(r'user_account/?.*$', test_gadget_views.user_account, name='user_account'),
    url(r'servertime_index/$', test_gadget_views.servertime_index, name='servertime_index'),
    url(r'server_time/?.*$', test_gadget_views.servertime, name='server_time'),

]