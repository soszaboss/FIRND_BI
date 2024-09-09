from django.urls import path
from .views import AdminUserList, DiplomeUserList, InstitutionUserList, UsersList

urlpatterns = [
    path('admins/', AdminUserList.as_view(), name='admin-user-list'),
    path('diplomés/', DiplomeUserList.as_view(), name='diplomé-user-list'),
    path('institutions/', InstitutionUserList.as_view(), name='institution-user-list'),
    path('', UsersList.as_view(), name='user-list'),
]
