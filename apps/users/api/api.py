from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.api.serializers import UserSerializer

class UserAPIView(APIView):
    
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many = True)
        return Response(user_serializer.data)