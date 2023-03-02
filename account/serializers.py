from rest_framework import serializers

from account.models import Account, Otp


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        if len(password) < 6:
            raise serializers.ValidationError("Password six more")
        return attrs

    def create(self, validate_data):
        return Account.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = Account
        fields = ['email', 'password']


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'email', 'email_verified_at']


class OtpSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)

    class Meta:
        model = Otp
        fields = '__all__'


class VerifyAccountSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField()
    otp = serializers.CharField()
