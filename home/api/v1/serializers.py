from allauth.utils import email_address_exists
from django.http import HttpRequest
from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_settings
from django.utils.translation import ugettext_lazy as _

from home.models import Item

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_active', 'username')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email


class ItemSerializer(serializers.Serializer):
    items = serializers.JSONField(required=True)


class ItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('updated_at', 'user')
