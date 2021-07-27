from rest_framework import serializers
from url.models import Url


class urlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('__all__')