from django.contrib.auth.models import Group
from rest_framework import serializers, validators

from main.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'groups')
        extra_kwargs = {
            'username': {
                'validators': [
                    validators.UniqueValidator(queryset=User.objects.all())
                ]
            },
            'email': {
                'validators': [
                    validators.UniqueValidator(queryset=User.objects.all())
                ]
            },
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        group_data = validated_data.pop('groups')
        user = User.objects.create_user(**validated_data)
        if len(group_data) > 1:
            raise serializers.ValidationError({'detail': 'Selecting multiple Roles is not allowed.'})
        user.groups.add(group_data[0].id)
        return user
