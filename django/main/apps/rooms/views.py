from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from main.apps.rooms.models import Room
from main.apps.rooms.serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.order_by('id')
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser]
