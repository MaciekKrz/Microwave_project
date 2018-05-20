from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.views import View
from django.http import Http404
from rest_framework.views import APIView
from .models import MicrowaveStatus
from .serializers import MicrowaveSerializer
from rest_framework import generics
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.utils.deprecation import MiddlewareMixin


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

key = 'product'
with cache.lock(key, expire=60):
     ttl = cache.ttl(key)
     cache.ttl(key, ttl+10)


class StartView(View):
    def get(self, request):
        return render(request,
                      template_name="base.html")


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

    # def get(self, request):
        # status = MicrowaveStatus.objects.all()
        # serializer = MicrowaveSerializer(status, many=True, context={"request": request})
        # return Response(serializer.data)


##########################MICROWAVE/EVENT#############################################
class TestView(APIView):

    def get_object(self, movie_id):
        try:
            return MicrowaveStatus.objects.get(id=movie_id)
        except MicrowaveStatus.DoesNotExist:
            raise Http404

    def get(self, request, movie_id=1, format=None):
        microwave_status = self.get_object(movie_id)
        serializer = MicrowaveSerializer(microwave_status, context={"request": request})
        return Response(serializer.data)

    def put(self, request, movie_id=1, format=None):
        microwave_status = self.get_object(movie_id)
        serializer = MicrowaveSerializer(microwave_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = MicrowaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TestView(generics.ListCreateAPIView):
#     """This class defines the create behavior of our rest api."""
#     queryset = MicrowaveStatus.objects.all()
#     serializer_class = MicrowaveSerializer
#
#     def perform_create(self, serializer):
#         """Save the post data when creating a new data."""
#         serializer.save()

@csrf_exempt
@api_view(['GET', 'PUT'])
def viewProduct(request, pk=1):
        permission_classes = (AllowAny,)
        """
        Retrieve, update or delete a snippet instance.
        """
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


    # products = MicrowaveStatus.objects.all()
    # results = [product.to_json() for product in products]
    # return Response(results, status=status.HTTP_201_CREATED)




@api_view(['GET', 'POST', 'PUT'])
def view_cached_product(request):
    if 'product' in cache:
        # get results from cache
        products = cache.get('product')
        return Response(products, status=status.HTTP_201_CREATED)

    else:
        products = MicrowaveStatus.objects.all()
        results = products[0].to_json()
        # store data in cache
        cache.set('product', results, timeout=CACHE_TTL)
        return Response(results, status=status.HTTP_201_CREATED)