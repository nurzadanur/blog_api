from django.urls import path
from . import views


urlpatterns = [
    path('', views.post_list_api_view),
    path('<int:id>/', views.post_detail_api_view),
    path('<int:id>/comments/', views.comment_list_api_view),
]
