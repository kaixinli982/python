from django.conf.urls import url
import views as stress_test_views

urlpatterns = [
    url(r'^$',stress_test_views.index,name="index"),
    # url(r'^stress_testing/.*', stress_test_views.single_interface, name='single_interface_index'),
    url(r'interface/$', stress_test_views.single_interface, name='single_interface_index'),
    url(r'interface/detail/$', stress_test_views.stress_testing, name='stress'),

    # url(r'^post/(?P<mock_pro_id>\d+)/(?P<req_type>\POST)/rep/$', mock_pro_views.xxd_request_vessel, name='xxd_post_ok'),



]