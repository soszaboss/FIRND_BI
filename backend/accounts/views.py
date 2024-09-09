from rest_framework import generics
from rest_framework.response import Response
from .models import Diplome, Institution, Admin, Account
from .serializers import DiplomeUserSerializer, AdminUserSerializer, InstitutionUserSerializer, CreateUserSerializer


class DiplomeUserList(generics.ListCreateAPIView):

    queryset = Diplome.objects.all()
    serializer_class = DiplomeUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DiplomeUserSerializer(queryset, many=True)
        return Response(serializer.data)

class InstitutionUserList(generics.ListCreateAPIView):

    queryset = Institution.objects.all()
    serializer_class = DiplomeUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = InstitutionUserSerializer(queryset, many=True)
        return Response(serializer.data)

class AdminUserList(generics.ListCreateAPIView):

    queryset = Admin.objects.all()
    serializer_class = DiplomeUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = AdminUserSerializer(queryset, many=True)
        return Response(serializer.data)

class UsersList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = CreateUserSerializer
