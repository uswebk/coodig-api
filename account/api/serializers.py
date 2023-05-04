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
    password = serializers.CharField()

    class Meta:
        model = Account
        fields = ['email', 'password']

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Passwords must be at least 6 characters long.")
        return value


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
    otp = serializers.CharField()


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ['password', 'password2', 'uid']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        if len(password) < 6:
            raise serializers.ValidationError("Password six more")
        return attrs
