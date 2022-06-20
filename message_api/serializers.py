from email.headerregistry import Group
from rest_framework import serializers
from .models import Account,Audience
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["pk", "user_id","group"]

class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ["pk", "name"]