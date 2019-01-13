from django.urls import path
from games import views

urlpatterns = [
path('games/', views.game_list),
path('games/<int:id>', views.game_detail)
]