from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["name", "email", "password"]
        extra_kwargs = {'password' : {'write_only': True},}

    def create(self, validated_data):
        member = User.objects.create_user(name=validated_data['name'],email=validated_data['email'],password=validated_data['password'])
        member.save()
        return member

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": {"message":"Bad Request","errors":"No active account found with the given credentials"}
    }
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_id']=str(self.user.user_id)
        return data