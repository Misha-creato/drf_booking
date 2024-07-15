from rest_framework import serializers

from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    confirm_password = serializers.CharField(
        max_length=128,
    )

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password',
            'confirm_password',
        ]

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
    )


class RefreshAndLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class PasswordRestoreRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordRestoreSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        max_length=128,
    )
    confirm_password = serializers.CharField(
        max_length=128,
    )

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                "Пароли не совпадают"
            )
        return attrs