from rest_framework import generics
from . import serializers


class ContactView(generics.ListCreateAPIView):
    serializer_class = serializers.ContactSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            user = None
        return serializer.save(user=user)
