from account.filters import UserFilter
from account.models import RoomPayment
from account.models import User
from account.models import UserAdditionalDetail
from account.serializers import GroupsSerializer
from account.serializers import PermissionSerializer
from account.serializers import RoomPaymentSerializer
from account.serializers import SendPasswordResetEmailSerializer
from account.serializers import SimpleUserAccountSerializer
from account.serializers import UserAccountSerializer
from account.serializers import UserAdditionalDetailcSerializer
from account.serializers import UserChangePasswordSerializer
from account.serializers import UserLoginSerializer
from account.serializers import UserPasswordResetSerializer
from account.service import find_matching_users
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import serializers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Permission.objects.exclude(name__icontains="custom permission").order_by(
        "content_type"
    )

    serializer_class = PermissionSerializer


class GroupsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.prefetch_related("permissions")
    serializer_class = GroupsSerializer


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


class UserAccountRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer

    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Set is_active to False instead of deleting the user
        instance.is_active = False
        instance.save()

        return Response(
            "User deactivated successfully", status=status.HTTP_204_NO_CONTENT
        )


class UserAccountListCreateView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        hostel = self.request.query_params.get("hostel")

        if not hostel:
            raise serializers.ValidationError({"hostel": "This parameter is required."})
        return queryset.filter(hostel=hostel)


class CreateAccountAPIView(CreateAPIView):
    serializer_class = UserAccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("password")
        user: User = serializer.save()
        user.set_password(password)
        user.save()

        user_serializer = SimpleUserAccountSerializer(user)

        return Response(
            {"user": user_serializer.data, "token": get_tokens_for_user(user)},
            status=status.HTTP_201_CREATED,
        )


class UserLoginView(CreateAPIView):
    """Login a user and generate a token."""

    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)
        existing_user = User.objects.filter(email=email).first()

        if user and existing_user:
            user_serializer = SimpleUserAccountSerializer(user)

            return Response(
                {"token": get_tokens_for_user(user), "user": user_serializer.data},
                status=status.HTTP_200_OK,
            )

        if existing_user and not existing_user.is_active:
            return Response(
                "User account is not active", status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            "Email or Password is not valid", status=status.HTTP_401_UNAUTHORIZED
        )


class SendPasswordResetEmailView(CreateAPIView):
    """SEND PASSWORD RESET LINK VIA EMAIL"""

    serializer_class = SendPasswordResetEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            "Password Reset link sent. Please check your Email",
            status=status.HTTP_200_OK,
        )


class UserChangePasswordView(CreateAPIView):
    """CHANGE USER PASSWORD"""

    permission_classes = [IsAuthenticated]
    serializer_class = UserChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        return Response("Password Changed Successfully", status=status.HTTP_200_OK)


class UserPasswordResetView(CreateAPIView):
    serializer_class = UserPasswordResetSerializer

    def create(self, request, *args, **kwargs):
        uid = request.query_params.get("uid", None)
        token = request.query_params.get("token", None)
        serializer = self.get_serializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response("Password Reset Successfully", status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    def get(
        self,
        request,
    ):
        # get userId from params
        userId = request.query_params.get("user_id", None)
        user = get_user_model().objects.filter(id=userId).first()
        if user is not None:
            # activate user
            user.is_active = True
            user.save()

            # permanent redirect to frontend login page

            return redirect(settings.FRONTEND_URL, permanent=True)
        # send the user to front end 404  page if user not found
        front_end_404 = f"{settings.FRONTEND_URL}/404"
        return redirect(front_end_404)


class UserAdditionalDetailView(viewsets.ModelViewSet):
    serializer_class = UserAdditionalDetailcSerializer
    queryset = UserAdditionalDetail.objects.order_by("-updated_at")


class ListMatchingUsersView(APIView):
    def get(self, request, *args, **kwargs):
        matching_users_dict = find_matching_users()
        serialized_data = []

        for _, data in matching_users_dict.items():
            serialized_user = SimpleUserAccountSerializer(data["user"]).data
            serialized_matches = SimpleUserAccountSerializer(
                data["matches"], many=True
            ).data
            serialized_user["matches"] = serialized_matches
            serialized_data.append(serialized_user)

        return Response(serialized_data, status=status.HTTP_200_OK)


class RoomPaymentApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RoomPaymentSerializer
    queryset = RoomPayment.objects.order_by("updated_at")
