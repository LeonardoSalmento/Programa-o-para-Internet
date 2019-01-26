"""
Book: Building RESTful Python Web Services
Chapter 2: Working with class based views and hyperlinked APIs in Django
Author: Gaston C. Hillar - Twitter.com/gastonhillar
Publisher: Packt Publishing Ltd. - http://www.packtpub.com
"""
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Game
from games.serializers import GameSerializer




@api_view(['GET', 'POST'])
def game_list(request):
    if request.method == 'GET':
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)

    elif request.method == 'POST':
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            if Game.objects.filter(name=game_serializer.validated_data['name']).exists():
                return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            game_serializer.save()
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)

    return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE' ])
def game_detail(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)

    elif request.method == 'PUT':
        game_serializer = GameSerializer(game, data=request.data)
        
        if game_serializer.is_valid():
            jogos_mesmo_nome = Game.objects.filter(name=game_serializer.validated_data['name'])
            

            if len(jogos_mesmo_nome) > 1 or jogos_mesmo_nome.exists() and jogos_mesmo_nome[0].release_date == game_serializer.validated_data['release_date'] and jogos_mesmo_nome[0].game_category == game_serializer.validated_data['game_category']:
                return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':            

        if game.pode_ser_excluido():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)