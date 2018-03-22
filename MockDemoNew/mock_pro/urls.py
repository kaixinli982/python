from django.conf.urls import url
import views as mock_pro_views

urlpatterns = [
    url(r'^$',mock_pro_views.index,name="index"),
    url(r'^indexPost/$',mock_pro_views.indexPost,name="d1"),
    url(r'^indexXXD/$',mock_pro_views.indexXXD,name="d1"),
    url(r'^indexPatch/$',mock_pro_views.indexPatch,name="d5"),
    url(r'^indexPut/$', mock_pro_views.indexPut, name="d6"),
    url(r'^indexGet/$',mock_pro_views.indexGet,name="d2"),
    url(r'^indexDelete/$', mock_pro_views.indexDelete, name="d7"),
    url(r'^indexGetBatch/$',mock_pro_views.indexGetBatch,name="d3"),
    url(r'^indexPostBatch/$',mock_pro_views.indexPostBatch,name="d4"),


    #url(r'^(?P<mock_pro_id>\d+)/$',mock_pro_views.vote,name='vote'),
    url(r'^post/(?P<mock_pro_id>\d+)/$',mock_pro_views.post_ready,name='post_ready'),
    url(r'^post_batch/(?P<mock_pro_id>\d+)/$',mock_pro_views.post_batch_ready,name='post_batch_ready'),

#xxd requests post
    #post
    # url(r'^xxd_post/(?P<mock_pro_id>\d+)/$',mock_pro_views.post_ready,name='post_ready'),
    url(r'^post/(?P<mock_pro_id>\d+)/$',mock_pro_views.xxd_request_ready,name='post_ready'),
    url(r'^post/(?P<mock_pro_id>\d+)/(?P<req_type>\POST)/rep/$',mock_pro_views.xxd_request_vessel,name='xxd_post_ok'),#(?P<req_type>\"POST")

    #put
    # url(r'^xxd_post/(?P<mock_pro_id>\d+)/$',mock_pro_views.post_ready,name='post_ready'),
    # url(r'^xxd_post/(?P<mock_pro_id>\d+)/(?P<req_type>\POST)/rep/$',mock_pro_views.xxd_request,name='xxd_post_ok'),
    url(r'^put/(?P<mock_pro_id>\d+)/$', mock_pro_views.post_ready, name='put_ready'),
    url(r'^put/(?P<mock_pro_id>\d+)/(?P<req_type>\PUT)/rep/$', mock_pro_views.xxd_request_vessel,name='xxd_put_ok'),
    # patch
    # url(r'^xxd_post/(?P<mock_pro_id>\d+)/$',mock_pro_views.post_ready,name='post_ready'),
    # url(r'^xxd_post/(?P<mock_pro_id>\d+)/(?P<req_type>\w+)/rep/$',mock_pro_views.xxd_request,name='xxd_post_ok'),#(?P<req_type>\"POST")
    url(r'^patch/(?P<mock_pro_id>\d+)/$',mock_pro_views.post_ready,name='patch_ready'),
    url(r'^patch/(?P<mock_pro_id>\d+)/(?P<req_type>\PATCH)/rep/$',mock_pro_views.xxd_request_vessel,name='xxd_patch_ok'),
    #delete
    url(r'^delete/(?P<mock_pro_id>\d+)/$', mock_pro_views.delete_ready, name='delete_ready'),
    url(r'^delete/(?P<mock_pro_id>\d+)/(?P<req_type>\DELETE)/rep/$', mock_pro_views.xxd_request_vessel,name='xxd_delete_ok'),



    url(r'^post/(?P<mock_pro_id>\d+)/rep/$',mock_pro_views.post_ok,name='post_ok'),
    url(r'^post_batch/(?P<mock_pro_id>\d+)/rep/$',mock_pro_views.post_batch_ok,name='post_batch_ok'),

    url(r'^get/(?P<mock_pro_id>\d+)/$',mock_pro_views.get_ready,name='get_ready'),
    url(r'^get_batch/(?P<mock_pro_id>\d+)/$',mock_pro_views.get_batch_ready,name='get_batch_ready'),
    url(r'^get_batch/(?P<mock_pro_id>\d+)/rep/$',mock_pro_views.get_batch_ok,name='get_batch_ok'),


    ]