from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        Class personnalisé pour ajouter des claims supplémentaire tel que
        le role de l'utilisateur.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id
        token['user_role'] = user.role

        return token


