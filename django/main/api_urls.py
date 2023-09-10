from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from main.apps.authentication.views import MyTokenObtainPairView
from main.apps.common.views import ChatGPTView
from main.apps.orders.views import OrderViewSet
from main.apps.rooms.views import RoomViewSet
from main.apps.users.views import UserViewSet

router = DefaultRouter()
app_name = 'api_urls'

# Register your API router here. It should be sorted by alphabet.
router.register('users', UserViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('token-auth/', MyTokenObtainPairView.as_view(), name='token-auth'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('chatgpt/', ChatGPTView.as_view(), name='chatgpt')
]

urlpatterns += router.urls
