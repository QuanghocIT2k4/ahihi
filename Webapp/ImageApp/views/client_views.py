from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated # Yêu cầu user phải login mới được truy cập vào API

# JWT
from rest_framework_simplejwt.tokens import AccessToken

# Dùng cho API cấp lại mk random
from django.utils.crypto import get_random_string

from ..models import User
from ..serializers import UserSerializer

# API Đăng ký
class ClientRegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Lưu mật khẩu trực tiếp, không mã hóa
            serializer.save()
            return Response(
                {"message": "Đăng ký thành công!", "user": serializer.data}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API Đăng nhập
class ClientLoginUserAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password_hash = request.data.get('password_hash')

        user = User.objects.filter(email=email).first()

        # So sánh mật khẩu trực tiếp
        if user and user.password_hash == password_hash:
            access_token = AccessToken.for_user(user)
            serializer = UserSerializer(user)
            
            return Response(
                {
                    "access_token": str(access_token),
                    "user_info": serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# API Cấp lại mật khẩu qua gmail
class ClientResetPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = get_random_string(length=12)

            # Cập nhật mật khẩu mới mà không mã hóa
            user.password_hash = new_password
            user.save()

            # Trả mật khẩu mới trong response
            return Response({
                'message': 'New password has been generated!',
                'new_password': new_password
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Email not found!'}, status=status.HTTP_404_NOT_FOUND)

# API Xem thông tin người dùng
class ClientViewUserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Kiểm tra access token hợp lệ

    def post(self, request):
        user = request.user  # Lấy người dùng từ access token đã xác thực
        
        # Kiểm tra xem người dùng có tồn tại không
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)

        # Trả về thông tin người dùng: tên và email
        return Response(
            {
                "name": serializer.data['name'],
                "email": serializer.data['email']
            },
            status=status.HTTP_200_OK
        )
