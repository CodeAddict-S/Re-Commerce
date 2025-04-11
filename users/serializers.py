from rest_framework.serializers import ModelSerializer
from users.models import User, Merchant, MerchantApplication

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'activation_token']

class MerchantSerializer(ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'

class MerchantApplicationSerializer(ModelSerializer):
    class Meta:
        model = MerchantApplication
        fields = '__all__'