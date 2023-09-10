from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.apps.orders.choices import OrderStatus
from main.apps.orders.models import Order
from main.apps.orders.serializers import OrderSerializer
from main.apps.users.choices import EmployeeGroup


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=['POST'])
    def cancel(self, request, pk=None):
        user = request.user
        instance: Order = self.get_object()
        is_guest = bool(user.groups.first().name == EmployeeGroup.GUEST)
        instance.order_status = OrderStatus.CANCEL_BY_GUEST if is_guest else OrderStatus.CANCEL
        instance.save()
        return Response(data={'message': f'Cancel order {instance.memo_number} successfully'},
                        status=status.HTTP_200_OK)
