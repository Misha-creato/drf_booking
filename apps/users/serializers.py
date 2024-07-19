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


class DetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'nickname',
            'email_confirmed',
        ]


class UpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        max_length=128,
        required=False,
    )
    new_password = serializers.CharField(
        max_length=128,
        required=False,
    )
    confirm_password = serializers.CharField(
        max_length=128,
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = [
            'nickname',
            'old_password',
            'new_password',
            'confirm_password',
        ]
        extra_kwargs = {
            'nickname': {'required': False},
        }

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        passwords = [old_password, new_password, confirm_password]

        if all(password is None for password in passwords):
            return attrs

        if not all(passwords):
            raise serializers.ValidationError(
                "Для смены пароля нужны old_password, new_password, confirm_password"
            )
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError(
                "Старый пароль неверный"
            )
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "Пароли не совпадают"
            )
        return attrs


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = serializers.DictField(child=serializers.CharField())
