from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from home.api.v1.serializers import (
    SignupSerializer, ItemModelSerializer, ItemSerializer
)
from django.utils.translation import ugettext_lazy as _

from home.models import Item, ItemCount
import json

from users.permissions import AdminPermission

User = get_user_model()


class RegisterViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User(
                email=serializer.validated_data.get('email'),
                username=serializer.validated_data.get('username'),
                is_active=True
            )
            user.set_password(serializer.validated_data.get('password'))
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'id': user.id,
                'email': user.email,
                'access_token': token.key,

            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    permission_classes = [AllowAny, ]

    def create(self, request):
        context = {
            "non_field_errors": [
                _('Unable to log in with provided credentials.')
            ]
        }
        email = request.data.get('email')
        password = request.data.get('password')
        kwargs = {'email': email}
        try:
            user = User.objects.get(**kwargs)
            if not user.is_active:
                context = {
                    'is_active': user.is_active,
                    "non_field_errors": [
                        _('I have sent you email. Please verify your email address')
                    ]
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            if user.check_password(password):

                token, created = Token.objects.get_or_create(user=user)

                return Response({
                    'id': user.id,
                    'email': user.email,
                    'is_active': user.is_active,
                    'access_token': token.key,

                }, status=status.HTTP_200_OK)

            else:
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist as e:
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ItemModelViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = ItemModelSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_object(self):
        return Item.objects.get(id=self.kwargs['pk'], user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:

            serializer = ItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            items = serializer.validated_data['items']['data']
            user = request.user
            item_count = ItemCount.objects.get_or_create(user=user)[0]
            total_count = item_count.item_count
            if total_count >= 10:
                return Response({'error': 'item limits exceed 10'}, status=status.HTTP_400_BAD_REQUEST)

            is_item_add = False
            for item in items:
                if total_count > 10:
                    total_count -= 1
                    break
                Item.objects.create(**item, item_count=item_count)
                is_item_add = True
                total_count += 1


            if is_item_add:
                user.entered = True
                user.save()
            item_count.item_count = total_count
            item_count.save()


            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)


class GetItemUser(ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AdminPermission, )
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(entered=True)

