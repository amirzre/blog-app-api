from django.contrib.auth import get_user_model

from rest_framework import serializers


class AuthenticationSerializer(serializers.Serializer):
    """validate user phone number for authentication"""

    phone = serializers.CharField(max_length=12, min_length=12)

    def validate_phone(self, value):
        from re import match

        regex_phone = "^989\d{2}\s*?\d{3}\s*?\d{4}$"
        if not match(regex_phone, value):
            raise serializers.ValidationError("Invalid phone number!")
        return value


class OtpSerializer(serializers.Serializer):
    """Create and validate otp code"""

    code = serializers.CharField(max_length=6, min_length=6)
    password = serializers.CharField(max_length=20, required=False)

    def validate_code(self, value):
        from string import ascii_letters as char

        for _ in value:
            if _ in char:
                raise serializers.ValidationError("Invalid Code!")
        return value


class UsersListSerializer(serializers.ModelSerializer):
    """List all users in database"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'phone', 'first_name', 'last_name', 'author')
