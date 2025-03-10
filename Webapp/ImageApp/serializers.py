from rest_framework import serializers
from ImageApp.models import User

class UserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(min_length=6) # write_only=True thì sẽ ẩn password khi POST API

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password_hash', 'created_at']  # Đúng theo bảng SQL
        read_only_fields = ['created_at']

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            password_hash=validated_data['password_hash']  # Đổi 'password' thành 'password_hash'
        )
        return user
