from rest_framework import serializers, validators

from main.apps.rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""

    class Meta:
        model = Room
        fields = ('name',)
        extra_kwargs = {
            'name': {
                'validators': [
                    validators.UniqueValidator(queryset=Room.objects.all())
                ]
            },
        }
