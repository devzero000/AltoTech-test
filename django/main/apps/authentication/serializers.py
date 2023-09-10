from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.apps.users.serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for returning JWT token"""
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # add extra responses
        data['user'] = UserSerializer(self.user).data

        return data
