from rest_framework import serializers
from rest_framework.validators import ValidationError

from utils.user_types import UserType
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "user_type"]

    def validate(self, attrs):
        email_exist = User.objects.filter(email=attrs["email"]).exists()

        if email_exist:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def validate_user_type(self, value):
        if value not in [user_type.value for user_type in UserType]:
            raise serializers.ValidationError(
                "User_type can only be 'COMPANY' or 'CLIENT'."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user
