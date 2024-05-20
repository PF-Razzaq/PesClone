from rest_framework import serializers
from .models import User,PesEvents


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password','otpCode']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    otpCode = serializers.CharField(required=True)

    def validate_password(self, value):
        # Implement any password validation logic here
        return value
    

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PesEvents
        fields = '__all__'