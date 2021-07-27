from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, View

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from url.models import Url
from url.serializers import urlsSerializer
from ratelimit.decorators import ratelimit


# Create your views here.
@method_decorator(ratelimit(key='ip', rate='10/d', method='POST', block=True), name='dispatch')
class Home(CreateView):
    model = Url
    fields = ['long_url']
    template_name = 'url/home.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        try:
            object_available = Url.objects.get(long_url=self.object.long_url)
            return HttpResponseRedirect(reverse('detail', kwargs={'pk' : object_available.pk}))
        except:
            return super(Home, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={'pk' : self.object.pk})


class Detail(DetailView):
    model = Url
    template_name = 'url/detail.html'


class Short(View):
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        url = Url.objects.get(token=token)
        return HttpResponseRedirect(url.long_url)


# Create your API Views here
@method_decorator(ratelimit(key='ip', rate='10/d', method='POST', block=True), name='dispatch')
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


@method_decorator(ratelimit(key='ip', rate='10/d', method='PUT', block=True), name='dispatch')
@method_decorator(ratelimit(key='ip', rate='10/d', method='DELETE', block=True), name='dispatch')
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
