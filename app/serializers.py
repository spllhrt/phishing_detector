from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class PhishingRequestSerializer(serializers.Serializer):
    sender = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=255, required=True)
    content = serializers.CharField(required=True)
