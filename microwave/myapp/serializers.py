from rest_framework import serializers
from .models import MicrowaveStatus


class MicrowaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MicrowaveStatus
        fields = ("On", "TTL", "Power")