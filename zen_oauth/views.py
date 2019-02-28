from django.contrib.auth.models import User
from rest_framework import generics

from zen_oauth.serializers import UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
