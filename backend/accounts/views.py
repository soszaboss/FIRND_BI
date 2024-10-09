from rest_framework import generics, status
from rest_framework.response import Response
from .models import Diplome, Institution, Admin, Account, Employe
from .serializers import DiplomeUserSerializer, AdminUserSerializer, InstitutionUserSerializer, CreateUserSerializer, \
    EmployeUserSerializer


# class based view pour lister tous les utilisateurs
class UsersList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = CreateUserSerializer

# class based view pour lister les utilisateurs et créer un utilisateur en fonction de son role

class DiplomeUserList(generics.ListCreateAPIView):

    queryset = Diplome.objects.all()
    serializer_class = DiplomeUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DiplomeUserSerializer(queryset, many=True)
        return Response(serializer.data)

class InstitutionUserList(generics.ListCreateAPIView):

    queryset = Institution.objects.all()
    serializer_class = InstitutionUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = InstitutionUserSerializer(queryset, many=True)
        return Response(serializer.data)

class AdminUserList(generics.ListCreateAPIView):

    queryset = Admin.objects.all()
    serializer_class = AdminUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = AdminUserSerializer(queryset, many=True)
        return Response(serializer.data)

class EmployeUserList(generics.ListCreateAPIView):

    queryset = Employe.objects.all()
    serializer_class = EmployeUserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = EmployeUserSerializer(queryset, many=True)
        return Response(serializer.data)