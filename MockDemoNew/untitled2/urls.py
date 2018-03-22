from django.conf.urls import include, url
from django.contrib import admin
from manage_app import views as manage_views
# from mock_pro import

urlpatterns = [
    # Examples:
    # url(r'^$', 'untitled2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^mock_pro/', include("mock_pro.urls")),
    url(r'^stress_testing/', include("stress_testing.urls")),
    url(r'^test_gadget/', include("test_gadget.urls")),
    url(r'^md5/', include("md5.urls")),
    url(r'^test_data/',include("test_data.urls")),
    url(r'^$',manage_views.index),


]
