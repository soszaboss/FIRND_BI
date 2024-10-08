from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to add additional claims such as the user's role.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_role'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add role to the access token payload
        data['role'] = self.user.role
        
        return data

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField(help_text="OTP code received by the user")
    email = serializers.EmailField(help_text="Email of the user")

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Email of the user")
    password = serializers.CharField(help_text="Password of the user", style={'input_type': 'password'})
