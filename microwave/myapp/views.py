from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.views import View
from django.http import Http404
from rest_framework.views import APIView
from .models import MicrowaveStatus
from .serializers import MicrowaveSerializer
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.cache import cache_page
from django.http import HttpResponse
from django.core.cache import cache
from django.shortcuts import redirect


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

#############################################################3

import json


class StartView(View):
    def get(self, request):
        return render(request,
                      template_name="base.html")


########################## MICROWAVE STATUS #############################################
class StatusView(APIView, MiddlewareMixin):
    def get_object(self, pk=1):
        try:
            return MicrowaveStatus.objects.get(pk=pk)
        except MicrowaveStatus.DoesNotExist:
            raise Http404

    def get(self, request, id=1, format=None):
        status = self.get_object(id)
        serializer = MicrowaveSerializer(status, context={"request": request})
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, id=1, format=None):
        microwave_status = self.get_object(id)
        _data = request.POST.copy()
        _data['TTL'] = str(int(_data['TTL']) - 1)
        serializer = MicrowaveSerializer(microwave_status, data=_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


########################## MICROWAVE EVENT #############################################
@csrf_exempt
@api_view(['GET', 'PUT'])
def microwave_event(request, pk=1):

        try:
            snippet = MicrowaveStatus.objects.get(pk=pk)
        except MicrowaveStatus.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = MicrowaveSerializer(snippet)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = MicrowaveSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                print("**", serializer.data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################## CACHE #####################################
@cache_page(CACHE_TTL)
@api_view(['GET', 'POST', 'PUT'])
def view_cached_product(request):
    if 'product' in cache:
        power = cache.get('product')
        return Response(power, status=status.HTTP_200_OK)
    else:
        cache.set('product', {'power': 100}, timeout=CACHE_TTL)
        power = cache.get('product')
        return Response(power, status=status.HTTP_201_CREATED)


############################################# REDIS ###############################################
def status(request):
    microwave_status = cache.get("status")
    if microwave_status is None:
        cache.set("status", '{"power":100}', timeout=10)
    microwave_object = json.loads(microwave_status)
    return HttpResponse("""
    Power: {}<br/>
    Timer: {}<br/>
    Buttons:<br/><a href="/T+">T+</a> <br/> <a href="/T-">T-</a></br>
            <a href="/P+">P+</a> <br/> <a href="/P-">P-</a></br>
    Stop microwave: <a href="/stop">Stop</a>
    """.format(microwave_object['power'], cache.ttl("status")))


def timer_plus(request):
    microwave_status = cache.get("status")
    if microwave_status is None:
        cache.set("status", '{"power":100}', timeout=1)
    if cache.ttl("status") >= 99:
        return HttpResponse("This is maximal time")
    microwave_status = cache.get("status")
    microwave_object = json.loads(microwave_status)
    if cache.ttl("status") >= 91 and cache.ttl("status") <= 99 :
        cache.set("status", json.dumps(microwave_object), timeout=99)
    microwave_status = cache.get("status")
    microwave_object = json.loads(microwave_status)
    cache.set("status", json.dumps(microwave_object), timeout=cache.ttl("status")+10)
    return redirect('/')


def timer_minus(request):
    microwave_status = cache.get("status")
    if microwave_status is None:
        return HttpResponse("Time can't be negative")
    microwave_status = cache.get("status")
    if cache.ttl("status") >= 1 and cache.ttl("status") <= 9:
        cache.delete("status")
    microwave_object = json.loads(microwave_status)
    cache.set("status", json.dumps(microwave_object), timeout=cache.ttl("status")-10)
    return redirect('/')


def power_plus(request):
    microwave_status = cache.get("status")
    if microwave_status is None:
        return HttpResponse("Power can't be changed when microwave is off")
    microwave_object = json.loads(microwave_status)
    if microwave_object['power'] >= 1000:
        return HttpResponse("This is maximal power")
    microwave_object = json.loads(microwave_status)
    microwave_object['power'] += 100
    cache.set("status", json.dumps(microwave_object), timeout=cache.ttl("status"))
    return redirect('/')


def power_minus(request):
    microwave_status = cache.get("status")
    if microwave_status is None:
        return HttpResponse("Power can't be changed when microwave is off")
    microwave_object = json.loads(microwave_status)
    if microwave_object['power'] == 100:
         return HttpResponse ("This is minimal power")
    microwave_object = json.loads(microwave_status)
    microwave_object['power'] -= 100
    cache.set("status", json.dumps(microwave_object), timeout=cache.ttl("status"))
    return redirect('/')


def clean_status(request):
    cache.delete("status")
    return redirect('/')