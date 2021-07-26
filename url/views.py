from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from url.models import Url
from url.serializers import urlsSerializer


# Create your views here.
class Home(CreateView):
    model = Url
    fields = ['long_url']
    template_name = 'url/home.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'pk' : self.object.pk})


class Detail(DetailView):
    model = Url
    template_name = 'url/detail.html'


# Create your API Views here
class UrlList(APIView):
    def get(self, request):
        urls = Url.objects.all()
        serializer = urlsSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {
            'long_url': request.data.get('long_url'),
        }
        serializer = urlsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UrlDetail(APIView):
    def get_object(self, url_id):
        try:
            return Url.objects.get(id=url_id)
        except Url.DoesNotExist:
            return None

    def get(self, request, url_id):
        url_instance = self.get_object(url_id)
        if not url_instance:
            return Response(
                {"res": "Object with url id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = urlsSerializer(url_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, url_id):
        url_instance = self.get_object(url_id)
        if not url_instance:
            return Response(
                {"res": "Object with url id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'long_url': request.data.get('long_url'),
        }
        serializer = urlsSerializer(instance=url_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, url_id):
        url_instance = self.get_object(url_id)
        if not url_instance:
            return Response(
                {"res": "Object with url id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        url_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
