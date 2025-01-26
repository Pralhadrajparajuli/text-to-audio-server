from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework import status
from utils.custom_response import custom_response
from django.forms.models import model_to_dict
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")

        # Validate passwords
        if password != password2:
            return custom_response(
                status_bool=False,
                message="Passwords do not match.",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        # Validate username and email
        if CustomUser.objects.filter(username=username).exists():
            return custom_response(
                status_bool=False,
                message="Username already exists.",
                http_status=status.HTTP_400_BAD_REQUEST
            )
        if CustomUser.objects.filter(email=email).exists():
            return custom_response(
                status_bool=False,
                message="Email already exists.",
                http_status=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user_data = model_to_dict(user)

        return custom_response(
            status_bool=True,
            message="User registered successfully.",
            data=user_data,
            http_status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            return custom_response(
                status_bool=False,
                message="Invalid credentials.",
                http_status=status.HTTP_401_UNAUTHORIZED
            )

        # Successful login
        user_data = model_to_dict(user)

        # Generate JWT Token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Add the token to the response
        user_data["access_token"] = str(access_token)

        return custom_response(
            status_bool=True,
            message="Login successful.",
            data=user_data,
            http_status=status.HTTP_200_OK
        )