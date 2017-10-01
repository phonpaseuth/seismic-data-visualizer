__author__ = 'Lei Huang'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data_id/(?P<req_data_id>[A-Za-z0-9_]+)/dim/(?P<dim>[ixz])/num/(?P<num>[0-9]+)/$', views.data, name='data'),
    #url(r'^data_id/(?P<req_data_id>[A-Za-z0-9_]+)/dim/(?P<dim>[ixz])/num/(?P<num>[0-9]+)/$', views.dataDetail.as_view(), name='data'),
    #url(r'^id/(?P<id>[0-9]+)/dim/(?P<dim>[ixz])/num/(?P<num>[0-9]+)/$', views.data, name='data'),
    #url(r'^heatmap/(?P<data_id>[0-9]+)/$', views.heatmap, name='heatmap'),
    url(r'^heatmap/data_id/(?P<req_data_id>[A-Za-z0-9_]+)/dim/(?P<dim>[ixz])/num/(?P<num>[0-9]+)/$', views.heatmap, name='heatmap'),

    url(r'^heatmap/data_id/(?P<req_data_id>[A-Za-z0-9_]+)/dim/(?P<dim>[ixz])/num/(?P<num>[0-9]+)/dim2/(?P<dim2>[ixz])/$', views.heatmap, name='heatmap'),

    url(r'^heatmap/data_id/(?P<req_data_id>[A-Za-z0-9_]+)/dim/(?P<dim>[ixz])/num/(?P<num>[0-9]+)/dim2/(?P<dim2>[ixz])/dim3/(?P<dim3>[ixz])/$', views.heatmap, name='heatmap'),

    url(r'^log/$', views.log, name='log'),
]