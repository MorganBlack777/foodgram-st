from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from core.models import Subscription
from .serializers import (
    UserSerializer,
    SetAvatarSerializer,
    SetPasswordSerializer,
    UserWithRecipesSerializer,
)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in [
            "retrieve",
        ]:
            return [AllowAny()]
        return super().get_permissions()

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["put", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def avatar(self, request):
        if request.method == "DELETE":
            user = request.user
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if "avatar" not in request.data or not request.data["avatar"]:
            return Response(
                {"avatar": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SetAvatarSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        subscribed_users = User.objects.filter(subscribers__user=request.user)
        page = self.paginate_queryset(subscribed_users)

        if page:
            serializer = UserWithRecipesSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)

        serializer = UserWithRecipesSerializer(
            subscribed_users, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["post", "delete"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == "POST":
            if user == author:
                return Response(
                    {"errors": "You cannot subscribe to yourself"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscription, created = Subscription.objects.get_or_create(
                user=user, subscribed_to=author
            )

            if not created:
                return Response(
                    {"errors": "You are already subscribed to this user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = UserWithRecipesSerializer(
                author, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # DELETE method
        if subscription := Subscription.objects.filter(
            user=user, subscribed_to=author
        ):
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"errors": "You are not subscribed to this user"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserAvatarView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        if "avatar" not in request.data or not request.data["avatar"]:
            return Response(
                {"avatar": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SetAvatarSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.avatar = None
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
