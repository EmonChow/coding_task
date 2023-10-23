from rest_framework import serializers
from django_currentuser.middleware import get_current_authenticated_user

from .models import *


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = todo
        fields = '__all__'
    
    def create(self, validated_data):
        modelObject = super().create(validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.created_by = user
        modelObject.save()
        return modelObject
    
    def update(self, instance, validated_data):
        modelObject = super().update(instance=instance, validated_data=validated_data)
        user = get_current_authenticated_user()
        if user is not None:
            modelObject.updated_by = user
        modelObject.save()
        return modelObject
