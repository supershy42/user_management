from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, EmailVerificationCode
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    email_verification_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'nickname', 'email_verification_code']

    def validate_email_verification_code(self, code):
        try:
            verification_code = EmailVerificationCode.objects.get(
                code=code,
                user__email=self.initial_data['email'],
                is_used=False
            )
            if (timezone.now() - verification_code.created_at).seconds > 300:  # 5분 유효
                raise ValidationError("Verification code expired.")
            return code
        except EmailVerificationCode.DoesNotExist:
            raise ValidationError("Invalid verification code.")

    def create(self, validated_data):
        validated_data.pop('email_verification_code', None)  # 이미 검증한 코드 제거
        user = User.objects.create_user(**validated_data) # 새로운 사용자 생성
        user.is_active = True # 사용자 활성화 (이메일 인증 완료)
        user.save()

        EmailVerificationCode.objects.filter( # 이메일 인증 코드 사용 처리
            user=user,
            code=self.initial_data['email_verification_code']
        ).update(is_used=True)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials or account not activated.")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'nickname', 'avatar', 'date_joined']


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'is_online']


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
