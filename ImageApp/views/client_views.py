# JWT
import jwt
import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings 
from django.core.mail import send_mail
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

        if user and user.password_hash == password_hash:
            # Tạo access token thủ công, không dùng Django Auth
            payload = {
                "user_id": user.id,
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
                "iat": datetime.datetime.now(datetime.timezone.utc)

            }
            access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            serializer = UserSerializer(user)
            return Response(
                {
                    "access_token": access_token,
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

            # Gửi email qua Mailtrap
            subject = "Your New Password"
            message = f"Hello {user.name},\n\nYour new password is: {new_password}\n\nPlease change it after logging in."
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Dùng email từ settings.py
                [email],
                fail_silently=False,  # Nếu lỗi sẽ báo
            )

            return Response({'message': 'New password has been sent to your email!'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'Email not found!'}, status=status.HTTP_404_NOT_FOUND)

# API Xem thông tin người dùng
class ClientViewUserInfoAPIView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        token_str = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token_str, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response(
                {
                    "name": serializer.data['name'],
                    "email": serializer.data['email']
                },
                status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError:
            return Response({"detail": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)



# API Đổi mật khẩu
class ClientChangePasswordAPIView(APIView):
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        token_str = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token_str, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")

            if not old_password or not new_password:
                return Response({"error": "Vui lòng nhập đầy đủ thông tin"}, status=status.HTTP_400_BAD_REQUEST)

            if user.password_hash != old_password:
                return Response({"error": "Mật khẩu cũ không chính xác"}, status=status.HTTP_400_BAD_REQUEST)

            user.password_hash = new_password
            user.save()

            return Response({"message": "Đổi mật khẩu thành công!"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"detail": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"detail": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
