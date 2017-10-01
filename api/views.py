from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404, HttpResponseForbidden
from . import ReadSlice 
from api.models import *
from django.utils import timezone
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.permissions import *
from django.core.exceptions import PermissionDenied

from bokeh.resources import CDN
from bokeh.embed import components

from bokeh.layouts import gridplot
from bokeh.io import output_file, show

def index(request):
    return HttpResponse("Welcome to data server")

class dataDetail(APIView):
    #permission_classes = (IsOwnerOrShared,permissions.IsAdminUser,)
    queryset = DataInfo.objects.all()

    def get_object(self, req_data_id):
        try:
            return DataInfo.objects.get(data_id = req_data_id)
        except DataInfo.DoesNotExist:
            raise Http404

    def get(self, request, req_data_id, dim, num, format = None ):
        d = self.get_object(req_data_id)
        print (request.user.username, d.owner)
        if d.owner == request.user.username and request.user.is_authenticated():
            return HttpResponse(readSliceToJson(d.data_location, dim, int(num)), content_type="application/json")
        else:
            raise PermissionDenied

def data(request, req_data_id, dim, num):
    l = Log(data_id=req_data_id, access_date=timezone.now(), action='GET', user_id='unknown', command='Get '+req_data_id + ' dim ' + dim + num )
    l.save()
    # Get the file name
    try:
        d = DataInfo.objects.get(data_id = req_data_id)
    except DataInfo.DoesNotExist:
        raise Http404
    return HttpResponse(ReadSlice.readSliceToJson(d.data_location, dim, int(num)), content_type="application/json")

def heatmap(request, req_data_id, dim, num, dim2=None, dim3=None):
    l = Log(data_id=req_data_id, access_date=timezone.now(), action='GET', user_id='unknown', command='Get '+req_data_id + ' dim ' + dim + num )
    l.save()
    d = DataInfo.objects.get(data_id = req_data_id)

    p1 = ReadSlice.readSliceBokeh(d.data_location, dim, int(num), req_data_id)
    script, div = components(p1, CDN)
    
    context = {
    'id': req_data_id,
    'dim': dim,
    'num': num,
    'the_script': script,
    'the_div': div,
    }

    if dim2 != None:
        p2 = ReadSlice.readSliceBokeh(d.data_location, dim2, int(num), req_data_id)
        script2, div2 = components(p2, CDN)
        context2 = {
        'the_script2': script2,
        'the_div2': div2,
        }
        context.update(context2)


    if dim3 != None:
        p3 = ReadSlice.readSliceBokeh(d.data_location, dim3, int(num), req_data_id)
        script3, div3 = components(p3, CDN)
        context3 = {
        'the_script3': script3,
        'the_div3': div3,
        }
        context.update(context3)

    return render(request, 'data/heatmapjs.html', context)

def log(request):
    permission_classes = (permissions.IsAuthenticated,)
    latest_log_list = Log.objects.order_by('-access_date')
    context = {'log_list': latest_log_list}
    return render(request, 'data/log.html', context)