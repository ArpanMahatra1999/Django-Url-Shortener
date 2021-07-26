from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView

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


class UrlList(APIView):
    def get(self, request):
        urls = Url.objects.all()
        serializer = urlsSerializer(urls, many=True)
        return Response(serializer.data)

    def post(self):
        pass
