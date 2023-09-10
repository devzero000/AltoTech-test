from rest_framework import serializers

from main.apps.orders.choices import OrderTypes
from main.apps.orders.models import Order
from main.apps.rooms.models import Room
from main.apps.users.choices import EmployeeGroup


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    room = serializers.CharField()
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    @staticmethod
    def _get_valid_permissions():
        return {
            OrderTypes.CLEANING: [EmployeeGroup.MAID_SUPERVISOR],
            OrderTypes.MAID_REQUEST: [EmployeeGroup.MAID_SUPERVISOR],
            OrderTypes.TECHNICIAN_REQUEST: [EmployeeGroup.SUPERVISOR, EmployeeGroup.GUEST],
            OrderTypes.AMENITY_REQUEST: [EmployeeGroup.GUEST]
        }

    @staticmethod
    def clean_order_fields(order_type, attrs):
        if order_type != OrderTypes.TECHNICIAN_REQUEST and 'problem' in attrs:
            attrs.pop('problem')
        elif order_type != OrderTypes.AMENITY_REQUEST and all(
                key in attrs for key in ['amenity_name', 'amenity_count']
        ):
            attrs.pop('amenity_name')
            attrs.pop('amenity_count')

        return attrs

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        role = user.groups.first()

        if not role and not user.is_superuser:
            raise serializers.ValidationError(
                {'detail': 'User does not belong to any group.'}, code='invalid'
            )

        valid_perm = self._get_valid_permissions()

        if not user.is_superuser and role.name not in valid_perm.get(attrs.get('order_type'), []):
            raise serializers.ValidationError(
                {'detail': 'You do not have permission to create this order.'}, code='permission_denied'
            )

        attrs = self.clean_order_fields(attrs.get('order_type'), attrs)

        room_name = attrs.get('room', '')
        try:
            attrs['room'] = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'The provided room does not exist.'}, code='not_found'
            )

        if attrs.get('finished_at') < attrs.get('started_at'):
            raise serializers.ValidationError(
                {'detail': 'Finished date cannot be less than Started date.'}, code='invalid_date'
            )

        attrs['created_by'] = user

        return attrs
