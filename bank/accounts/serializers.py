from rest_framework import serializers
from .models import Account
from rest_framework.validators import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'owner', 'balance', 'creation_date')


    def validate(self, data):
        balance = data['balance']
        if balance == 0:
            raise ValidationError('Valor do balance não pode ser 0')