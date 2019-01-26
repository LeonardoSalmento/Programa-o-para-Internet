from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Account
from accounts.serializers import AccountSerializer


# Create your views here.

@api_view(['GET', 'POST'])
def account_list(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        accounts_serializer = AccountSerializer(accounts, many=True)
        return Response(accounts_serializer.data)

    elif request.method == 'POST':
        account_serializer = AccountSerializer(data=request.data)
        if account_serializer.is_valid():
            if account_serializer.validated_data['balance'] <= 0:
                return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            account_serializer.save()
            return Response(account_serializer.data, status=status.HTTP_201_CREATED)

    return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def account_detail(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        account_serializer = AccountSerializer(account)
        return Response(account_serializer.data)

    elif request.method == 'PUT':
        
        account_serializer = AccountSerializer(account, data=request.data)
        
        if account_serializer.is_valid():
            account_serializer.save()
            return Response(account_serializer.data)
        return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':            
            
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    