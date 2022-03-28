from extensions.code_generator import otp_generator
from permissions import IsSuperUser
from user.send_otp import send_otp
from core.models import PhoneOtp
from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import (
    UsersListSerializer,
    AuthenticationSerializer,
    OtpSerializer
)


class UserRegisterApiView(APIView):
    """Register user with phone number"""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Send mobile number for register"""

        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get('phone')

            user_otp, _ = PhoneOtp.objects.get_or_create(phone=phone)
            if user_otp.count >= 5:
                return Response(
                    {'Many Request': 'You requested too much.'},
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

            user_is_exists: bool = get_user_model().objects.filter(
                phone=phone
            ).values('phone').exists()

            if user_is_exists:
                return Response(
                    {"User exists": "Please enter a different phone number."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            code = otp_generator()
            user_otp.otp = code
            cache.set(phone, code, 300)
            send_otp(phone=phone, otp=code)
            user_otp.count += 1
            user_otp.save(update_fields=['otp', 'count'])

            context = {
                "code sent": "The code has been sent to the phone number."
            }

            return Response(
                context,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginApiView(APIView):
    """Login user with phone number"""

    permission_classes = [
        AllowAny,
    ]

    def post(self, request):
        serializer = AuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.data.get("phone")

            user_otp, _ = PhoneOtp.objects.get_or_create(
                phone=phone,
            )
            if user_otp.count >= 5:
                return Response(
                    {
                        "Many Request": "You requested too much.",
                    },
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                )

            user_is_exists: bool = get_user_model().objects.filter(
                phone=phone
            ).values("phone").exists()

            if not user_is_exists:
                return Response(
                    {
                        "No User exists": "Please enter another phone number.",
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            code = otp_generator()
            user_otp.otp = code
            cache.set(phone, code, 300)
            send_otp(phone=phone, otp=code)
            user_otp.count += 1
            user_otp.save(update_fields=["otp", "count"])

            context = {
                "code sent": "The code has been sent to the phone number.",
            }
            return Response(
                context,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyOtpApiView(APIView):
    """Verify otp code and register user"""

    permission_classes = (AllowAny,)
    confirm_for_authentication = False

    def post(self, request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            received_code = serializer.data.get('code')
            query = PhoneOtp.objects.filter(otp=received_code)

            if not query.exists():
                return Response(
                    {'Incorrect code": "The code entered is incorrect.'},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )

            object = query.first()
            code_in_cache = cache.get(object.phone)

            if code_in_cache is not None:
                if code_in_cache == received_code:
                    user, created = get_user_model().objects.get_or_create(
                        phone=object.phone
                    )
                    if user.two_step_password:
                        password = serializer.data.get('password')
                        check_password = user.check_password(password)
                        if check_password:
                            self.confirm_for_authentication = True
                        else:
                            return Response(
                                {
                                    'Incorrect password": "Password is incorrect.'
                                },
                                status=status.HTTP_406_NOT_ACCEPTABLE,
                            )
                    else:
                        self.confirm_for_authentication = True

                    if self.confirm_for_authentication:
                        refresh = RefreshToken.for_user(user)
                        cache.delete(object.phone)
                        object.verify, object.count = True, 0
                        object.save(update_fields=['verify', 'count'])
                        context = {
                            'created': created,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
                        return Response(
                            context,
                            status=status.HTTP_200_OK,
                        )
                else:
                    return Response(
                        {'Incorrect code': 'The code entered is incorrect.'},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
            else:
                return Response(
                    {'Code expired': 'The entered code has expired.'},
                    status=status.HTTP_408_REQUEST_TIMEOUT,
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UsersListApiView(ListAPIView):
    """Returns a list of all existing users"""

    serializer_class = UsersListSerializer
    permission_classes = (IsSuperUser,)
    filterset_fields = ('author',)
    search_fields = ('phone', 'first_name', 'last_name')
    ordering_fields = ('id', 'author')
    queryset = get_user_model().objects.all()
