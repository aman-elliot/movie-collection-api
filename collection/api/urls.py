from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
urlpatterns = [
    path('register/', views.userRegistration, name='registration'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('movies/', views.listMovies, name='listMovies'),
    path('collection/', views.listCollections, name='listCollections'),
    path('collection/<str:collection_uuid>/', views.manipulate, name='manipulate'),
    path('request-count/', views.updateRequestCount, name='updaterequestCount'),
    path('request-count/reset/', views.resetRequestCount, name='resetrequestCount')
]