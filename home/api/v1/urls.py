from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    RegisterViewSet,
    LoginViewSet, ItemModelViewSet, GetItemUser
)

router = DefaultRouter()

router.register('register', RegisterViewSet, basename='register')
router.register('login', LoginViewSet, basename='login')
router.register('item', ItemModelViewSet, basename='item')
router.register('get_item_users', GetItemUser, basename='get_item_users')

urlpatterns = [
    path('', include(router.urls)),
]
